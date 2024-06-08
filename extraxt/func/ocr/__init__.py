from pandas import DataFrame
import re

import fitz

from extraxt.util import to_snake


class OCR:
    def __init__(self):
        print(f"Extraxt OCR: Initialized OCR service...")

    def read(self, stream):
        text = self.extract(stream)
        if text and text[0]:
            content = text[0].splitlines()
            data = self.parse(content)
            return DataFrame([data])
        else:
            return DataFrame()

    def doc(self, stream):
        stream.seek(0)
        content = stream.read()
        print(f"Extraxt OCR: Opening file with `fitz`...")
        doc = fitz.open(stream=content, filetype="pdf")
        return doc

    def text(self, doc):
        print(f"Extraxt OCR: Reading text content from file...")
        text = list(map(lambda page: page.get_text("text"), doc))
        return text

    def extract(self, stream):
        try:
            doc = self.doc(stream)
            text = self.text(doc)
            doc.close()
            return text
        except Exception as e:
            return []

    def parse(self, lines):
        print(f"Extraxt OCR: Parsing and sanitising text content...")
        data = {}
        key = None
        capture_age = False
        age_pattern = re.compile(r"Age:\s*(\d+)\s*years", re.IGNORECASE)

        for line in lines:
            clean_line = line.strip()
            lower_line = clean_line.lower()

            if "date of birth:" in lower_line:
                print(
                    f"Extraxt OCR: !!! Sensitive data found: [Date of birth]. This data will be parsed as [Age]..."
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
