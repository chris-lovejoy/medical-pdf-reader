# Medical PDF Reader (Work In Progress)
An application to extract and query medical record PDFs

[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme) | [![run unit tests](https://github.com/chris-lovejoy/medical-pdf-reader/actions/workflows/run_pytests.yml/badge.svg)](https://github.com/chris-lovejoy/medical-pdf-reader/actions/workflows/run_pytests.yml)


## Table of Contents

- [About](#about)
- [Install](#setup)
- [Usage](#usage)



## About



## Setup


### 1. Add your OpenAI API Key to .env
Use the same format as [.env.example](.env.example).


### 2. Install the required dependencies

Create a virtual environment
```
python3 -m venv venv
```

Activate the virtual environment
```
source venv/bin/activate
```

Install the dependencies from [requirements.txt](./requirements.txt)
```python
pip install -r requirements.txt
```

### 3. Modify settings in [config.py](./src/config.py), as per preference




## Usage

- run python main.py
- or visualise in streamlit app
- (can run local testing with pytest)





