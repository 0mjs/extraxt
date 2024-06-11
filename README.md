# Extraxt
Extraxt is a Python-based MuPDF library to parse and extract data from PDF documents.

### Core Functionality

- **Nested JSON Output**: Constructs nested JSON objects reflecting the document's content.
- **Subtitle and Field Matching**: Define subtitles and corresponding data fields in snake_case (e.g. `first_name`, `address_line_one`, `income_(secondary)`).
- **Sensitive Data Configuration**: Enables sensitive data controls and configuration via the API.

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
- Extraxt `fields` are in the format of `my_key_subtitle_1`, where the value is a JSON array of the fields you wish to match. These fields must match the exact format of the text content in the PDF you are analysing.
- Matching something like `phone_(secondary)` will require the usage of parenthesis as of `0.11`. _This will soon be optional and parse out the parenthesis_.
- As of `0.11`, sensitive data _is not_ configurable via the API.


### Read file from disk
Reading from a Buffer stream can be done using `with open` as is standard in Python. From there you can invoke `.read()` on the binary and pass your `fields` specification.

```python
from extraxt import Extraxt

extraxt = Extraxt()


def main():
    path = "file.pdf"
    with open(path, "rb") as buffer:
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
