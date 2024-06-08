import json
import io
from pkg.service.ocr import OCRService
from pkg.service.formatter import FormatService


class Extraxt:
    def read(self, stream, type="pdf", fields=None, indent=4):
        if isinstance(stream, (bytes, bytearray)):
            stream = io.BytesIO(stream)

        ocr = OCRService(type=type)
        formatter = FormatService(fields=fields)

        dataframe = ocr.read(stream)
        content = dataframe.to_dict(orient="records")[0] if not dataframe.empty else {}
        data = formatter.format(content)
        output = {section.lower(): {} for section in fields.keys()}
        formatter.apply(data, output)

        return json.dumps(output, indent=indent)
