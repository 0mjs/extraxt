# Extraxt
Extraxt is a Python-based MuPDF library that enables parsing and extracting data from PDF documents.

### Core Functionality

- **Nested JSON Output**: Constructs nested JSON objects reflecting the document's content.
- **Subtitle and Field Matching**: Define subtitles and corresponding data fields in snake case (e.g. `first_name`, `address_line_one`, `income_(secondary)`).
- **Sensitive Data Configuration**: Enables sensitive data controls and configuration via the API (Coming soon).

Extraxt streamlines the extraction process, converting PDF content into structured JSON for easy data manipulation and integration.


## Installation
#### Install Extraxt
```
pip install extraxt
```

#### Upgrade to new version of Extraxt
```
pip install --upgrade extraxt
```

#### Using Conda with Extraxt
```
conda create --name [YOUR_ENV] python=3.11 -y
conda activate [YOUR_ENV]
pip install extraxt
```

## Usage
Extraxt is able to consume either an asynchronous byte stream or a buffer directly from disk.

_Before you begin_:
- Matching something like `Phone (Secondary) -> phone_(secondary)` will require the usage of parenthesis as of `0.11`. _This will soon be opt in, where by default the parenthesis will be redacted_.
- As of `0.11`, sensitive data _is not_ configurable via the API, and instead `"Date of birth"` is parsed as `"age"` only.


### Read file from disk
Reading from a Buffer stream can be done using `with open` as is standard in Python. From there you can invoke `.read()` on the binary and pass your `fields` specification. `fields` accepts an object of user-input `key`'s (`subtitles`), where the `value` is a series of matches (`snaked_cased`) to that of the exact PDF text content within your document.

```python
from extraxt import Extraxt

extraxt = Extraxt()


def main():
    with open("file.pdf", "rb") as buffer:
        output = extraxt.read(
            stream=buffer.read(),
            fields={
                "profile": [
                    "first_name",
                    "middle_names",
                    "last_name",
                ],
                "experience": [
                    "job_title",
                    "education"
                ]
            },
        )
        print(f"Output: \n\n{output}\n\n")


if __name__ == "__main__":
    main()
```

### Read file in asynchronous API
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
