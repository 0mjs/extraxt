"""
Package: Extraxt
Developed by: Matt J. Stevenson
Organisation: Zephyr Software
Description: An OSS Python MuPDF package for extracting and parsing data from PDF files.

This software is part of the Extraxt package developed at Zephyr Software.
Licensed under the MIT License.

Author: Matt J. Stevenson
Date: 11/06/2024
"""

import logging
import re
from pandas import DataFrame
import fitz
from extraxt.util import to_snake


class Parser:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.logger.info("Initialized OCR service.")

    def read(self, stream):
        """Extract text from a PDF stream and parse it into a DataFrame."""
        text = self.extract(stream)
        if text:
            content = text[0].splitlines()
            data = self.parse(content)
            return DataFrame([data])
        return DataFrame()

    def doc(self, stream):
        """Open a PDF document from a stream."""
        stream.seek(0)
        content = stream.read()
        self.logger.info("Opening file...")
        try:
            return fitz.open(stream=content, filetype="pdf")
        except Exception as e:
            self.logger.error(f"Failed to open PDF document: {e}")
            raise

    def text(self, doc):
        """Extract text from all pages of a PDF document."""
        self.logger.info("Reading text content...")
        return [page.get_text("text") for page in doc]

    def extract(self, stream):
        """Extract text content from a PDF stream."""
        try:
            doc = self.doc(stream)
            text = self.text(doc)
            doc.close()
            return text
        except Exception as e:
            self.logger.error(f"Error extracting text: {e}")
            return []

    def parse(self, lines):
        """Parse lines of text to extract key-value pairs."""
        self.logger.info("Parsing/sanitising text content...")
        data = {}
        key = None
        capture_age = False
        age_pattern = re.compile(r"Age:\s*(\d+)\s*years", re.IGNORECASE)

        for line in lines:
            clean_line = line.strip()
            lower_line = clean_line.lower()

            if "date of birth:" in lower_line:
                self.logger.info(
                    "Sensitive data found: [Date of birth]. This data will be parsed as [age] as specified in your fields..."
                )
                key = "age"
                data[key] = ""
                capture_age = True
            elif ":" in clean_line and not capture_age:
                key, value = clean_line.split(":", 1)
                key = to_snake(key)
                data[key] = value.strip()
            elif key:
                if capture_age:
                    match = age_pattern.search(clean_line)
                    if match:
                        data[key] = match.group(1)
                        capture_age = False
                    else:
                        data[key] += (" " if data[key] else "") + clean_line
                else:
                    data[key] += f" {clean_line}"

        if "age" in data and (not data["age"].isdigit() or int(data["age"]) > 130):
            del data["age"]

        return data
