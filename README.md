# Extraxt
Extraxt is a simple Python-based MuPDF library for parsing and extracting data from PDF documents.

## Introduction
Extract uses two powerful libraries to parse and extract data from documents.
- PyMuPDF: https://pymupdf.readthedocs.io/en/latest/
- Pandas: https://pandas.pydata.org/docs/user_guide/index.html

## Installation
### Install Extraxt
`pip install extraxt`

### Upgrade to new Extraxt version
`pip install --upgrade extraxt`

### Conda with Extraxt
`conda create --name [YOUR_ENV] python=3.11 -y`

`conda activate [YOUR_ENV]`

`pip install extraxt`

## Usage
Extraxt can read files directly from disk, or as a Buffer stream.

### Read file from disk

```python
import os
import sys

from extraxt import Extraxt
from fields import FIELDS

extraxt = Extraxt()


def main():
    path = "YOUR_TEST_FILE.pdf"
    if not os.path.exists(path):
        return print(f"File not found: {path}")

    with open(path, "rb") as stream:
        output = extraxt.read(
            stream=stream.read(),
            type="pdf",
            fields=FIELDS,
            indent=2,
        )
        print(f"Output: \n\n{output}\n\n")


if __name__ == "__main__":
    main()
```

### Advanced Usage
#### FastAPI
For cases using FastAPI, Extraxt is a synchronous package and _will block_ the main thread.
To perform non-blocking/asynchronous extraction, you will need to use `asyncio` and Futures.

```python
import traceback
import json

from fastapi import File, HTTPException, JSONResponse
from extraxt import Extraxt

from app.util import event_loop
from app.config.fields import FIELDS

extraxt = Extraxt()


async def process_file(file: File):
    try:
        content = await file.read()
        if not content:
            raise HTTPException(500, "Failed to read file.")
        content = await event_loop(extraxt.read, content, FIELDS)

    except Exception as e:
        tb = traceback.format_exc()
        raise HTTPException(500, f"Failed to triage file {tb}")

    return JSONResponse({
        "content": json.loads(content),
    })
```
