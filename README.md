# Quart-Compress

[![Build Status](https://dev.azure.com/fdahlitz/quart-compress/_apis/build/status/DahlitzFlorian.quart-compress?branchName=master)](https://dev.azure.com/fdahlitz/quart-compress/_build/latest?definitionId=6&branchName=master)
[![codecov](https://codecov.io/gh/DahlitzFlorian/quart-compress/branch/master/graph/badge.svg)](https://codecov.io/gh/DahlitzFlorian/quart-compress)
[![PyPI version](https://badge.fury.io/py/quart-compress2.svg)](https://badge.fury.io/py/quart-compress2)
[![Python Support](https://img.shields.io/badge/Python-3.7%20|%203.8-blue)](https://img.shields.io/badge/Python-3.7%20|%203.8-blue)
![black](https://img.shields.io/badge/code%20style-black-000000.svg)

## Description

> Quart is a Python ASGI web microframework.
> It is intended to provide the easiest way to use asyncio functionality in a web context, especially with existing Flask apps.
> This is possible as the Quart API is a superset of the Flask API.

-- [Quart Project](https://github.com/pgjones/quart)

As I wanted to seamlessly migrate from Flask to Quart and noticed, that there are a few issues in using [Flask-Compress](https://github.com/shengulong/flask-compress) together with Quart, I decided to create my own Quart-Compress packages, which is based on the Flask-Compress project.


## Installation

Installing the package is as easy as:

```bash
$ pip install quart-compress2
```


## Usage

To compress your Quart responses, you only need to compress your Quart object at the beginning using the `Compress` class:

```python
from quart import Quart
from quart_compress import Compress

app = Quart(__name__)
Compress(app)
```
