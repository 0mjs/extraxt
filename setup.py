from setuptools import setup, find_packages

setup(
    name="extraxt",
    version="0.0.14",
    description="Easily extract data from PDFs.",
    long_description="A Python PDF data extraction library with a simple interface.",
    long_description_content_type="text/markdown",
    author="Matt J. Stevenson",
    author_email="dev@mattjs.me",
    url="https://github.com/0mjs/extraxt",
    packages=find_packages(),
    install_requires=["pandas", "PyMuPDF"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
)
