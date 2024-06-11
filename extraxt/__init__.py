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

from extraxt.module.parser import Parser
from extraxt.module.formatter import Formatter


import json
import io
import logging

from extraxt.module.parser import Parser
from extraxt.module.formatter import Formatter

logging.basicConfig(
    level=logging.INFO, format="[Extraxt]: %(asctime)s - %(levelname)s - %(message)s"
)


class Extraxt:
    def read(self, stream, fields=None, indent=4):
        if isinstance(stream, (bytes, bytearray)):
            stream = io.BytesIO(stream)

        parser = Parser()
        formatter = Formatter(fields)
        dataframe = parser.read(stream)
        content = dataframe.to_dict(orient="records")[0] if not dataframe.empty else {}
        data = formatter.format(content)
        output = {section.lower(): {} for section in fields.keys()}
        formatter.apply(data, output)

        return json.dumps(output, indent=indent)
