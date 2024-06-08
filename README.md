# Extraxt
Extraxt is a simple Python-based MuPDF library for parsing and extracting data from PDF documents.

Example Usage:
`FastAPI`

```python
from asyncio import get_running_loop
from extraxt import Extraxt
from fastapi import HTTPException
from functools import partial
from .config import FIELDS

extract = Extract()

async def event_loop(func, *args, **kwargs):
    print(f"Executing {func.__qualname__} asynchronously in the Event Loop.")
    return await get_running_loop().run_in_executor(
        None, partial(func, *args, **kwargs)
    )

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
