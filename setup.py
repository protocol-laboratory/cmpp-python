from setuptools import setup, find_packages

setup(
    name="cmpp",
    version="0.0.1",
    author="shoothzj",
    author_email="shoothzj@gmail.com",
    description="A Python package implements CMPP protocol",
    long_description_content_type="text/markdown",
    url="https://github.com/protocol-laboratory/cmpp-python",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
