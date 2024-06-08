import json
import io
import logging

from extraxt.func.ocr import OCR
from extraxt.func.fmt import Formatter

logging.basicConfig(
    level=logging.INFO, format="[Extraxt]: %(asctime)s - %(levelname)s - %(message)s"
)


class Extraxt:
    def read(self, stream, fields=None, indent=4):
        if isinstance(stream, (bytes, bytearray)):
            stream = io.BytesIO(stream)

        ocr = OCR()
        formatter = Formatter(fields=fields)

        dataframe = ocr.read(stream)
        content = dataframe.to_dict(orient="records")[0] if not dataframe.empty else {}
        data = formatter.format(content)
        output = {section.lower(): {} for section in fields.keys()}
        formatter.apply(data, output)

        return json.dumps(output, indent=indent)
