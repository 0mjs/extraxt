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


class Formatter:
    def __init__(self, fields):
        self.fields = fields
        logging.info(f"Initialized Formatter service with fields {fields.keys()}...")

    def format(self, content):
        data = {}
        for section, keys in self.fields.items():
            data[section] = {key: content.get(key, None) for key in keys}
        return data

    def apply(self, data, output, filter=None):
        logging.info(f"Applying basic formatting to data...")
        for category, keys in self.fields.items():
            for key in keys:
                if key in data.get(category, {}):
                    item = data[category][key]
                    if isinstance(item, str):
                        item_key = item.strip()
                        value = self.basic(item_key)
                    else:
                        value = self.basic(item)
                    if value != filter:
                        output[category.lower()][key] = value

    def basic(self, value):
        return {"No": False, "Yes": True, "Unknown": "unknown", "": None}.get(
            value, value
        )
