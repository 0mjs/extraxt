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
        logging.info(
            f"[ZEPHYR EXTRAXT] Initialized Formatter module with fields {', '.join(fields.keys())}..."
        )

    def format(self, content):
        data = {}
        for section, keys in self.fields.items():
            data[section] = {key: content.get(key, None) for key in keys}
        return data

    def apply(self, data, output, filter=None):
        logging.info(f"[ZEPHYR EXTRAXT] Sanitising data...")
        for category, keys in self.fields.items():
            category_data = data.get(category, {})
            output_category = output.setdefault(category.lower(), {})
            for key in keys:
                if key in category_data:
                    item = category_data[key]
                    value = self.basic(item.strip() if isinstance(item, str) else item)
                    if value != filter:
                        output_category[key] = value

    def basic(self, value):
        return {"No": False, "Yes": True, "Unknown": "unknown", "": None}.get(
            value, value
        )
