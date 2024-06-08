# Extraxt
Extraxt is a simple Python-based MuPDF library for parsing and extracting data from PDF documents.

Example Usage:

```python
from extraxt import Extraxt
from .config import FIELDS

async def process_file(file: File):
    try:
        content = await file.read()
        if not content:
            raise HTTPException(500, "Failed to read file.")
        content = await event_loop(extraxt.read, content, "pdf", FIELDS)

    except Exception as e:
        raise HTTPException(500, f"Failed to triage file")

    return {
        "content": json.loads(content),
    }
```
