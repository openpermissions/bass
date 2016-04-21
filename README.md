The Open Permissions Platform - Identity Library
==============================================

Table of Contents
=================

* [Introduction](#introduction)
* [Dependencies](#dependencies)
* [Running tests](#running-tests)
* [Installation](#installation)
* [Code Examples](#code-examples)
* [Documentation](#Documentation)

# Introduction

This is a Python library used for creating unique **hub keys** used within the Open Permissions Platform.

[Click here for the Open Permissions Platform home page](http://www.openpermissions/)

# Dependencies

This has been tested using

* Ubuntu 14.0.4
* Python 2.7.10

# Running tests

## Setup

Prior to running any test the python pip dependencies need to be installed.
Run the following command to do this
```bash
make requirements
```

## Unit tests

To run the unit tests run the following command
```bash
make test
```
Logs will be found at tests/unit/reports

## Behave tests

To run the behave tests run the following command
```bash
make behave
```
Logs will be found at tests/behave/reports

## Documentation

To generate documentation, run the following command:
```bash
make docs
```

# Installation

```
python setup.py install
```

## Generate a hub key

### Code

```Python
from bass.hubkey import create_hub_key

hub_key = generate_hub_key(
    resolver_id='copyrighthub.com',
    hub_id='hub1',
    repository_id='f8e3968eb99f48d6b9f84340efb64d47',
    entity_type="asset"
)

print hub_key
```

### Output

```Console
https://copyrighthub.com/s1/hub1/f8e3968eb99f48d6b9f84340efb64d47/asset/79fa0ce2e082467cad24703dcfdf7317
```

Documentation
--------------

Additional code documentation can be found at http://bass.readthedocs.org/en/stable/
