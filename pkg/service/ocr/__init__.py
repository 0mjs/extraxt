from pandas import DataFrame

import fitz

from pkg.util import to_snake


class OCRService:
    def __init__(self, type="pdf"):
        self.type = type

    def read(self, stream):
        text = self.extract(stream)
        if text and text[0]:
            content = text[0].splitlines()
            data = self.lines(content)
            return DataFrame([data])
        else:
            return DataFrame()

    def doc(self, stream):
        stream.seek(0)
        content = stream.read()
        doc = fitz.open(stream=content, filetype=self.type)
        return doc

    def text(self, doc):
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

    def lines(self, lines):
        data = {}
        key = None

        for line in lines:
            clean_line = line.strip()

            if ":" in clean_line:
                key, value = clean_line.split(":", 1)
                key = to_snake(key)
                data[key] = value.strip()
            elif key:
                data[key] += f" {clean_line}"

        return data
