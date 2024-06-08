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

### Read file from disk

```python
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from extraxt import Extraxt

extraxt = Extraxt()


def main():
    path = "my_test_file.pdf"
    if not os.path.exists(path):
        return print(f"File not found: {path}")

    with open(path, "rb") as stream:
        output = extraxt.read(
            stream=stream.read(),
            type="pdf",
            fields={
                "introduction": {
                    "title": "Introduction",
                    "fields": ["title", "date", "patient", "examination", "history"],
                },
            },
            indent=2,
        )
        print(f"Output: \n\n{output}\n\n")


if __name__ == "__main__":
    main()
```

### Advanced Usage
#### FastAPI

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
        user, _ = auth
        content = await file.read()
        if not content:
            raise HTTPException(500, "Failed to read file.")
        content = await event_loop(extraxt.read, content, "pdf", FIELDS)

    except Exception as e:
        tb = traceback.format_exc()
        raise HTTPException(500, f"Failed to triage file {tb}")

    return JSONResponse({
        "content": json.loads(content),
    })
```
