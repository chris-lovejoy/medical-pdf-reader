# Medical PDF Reader (Work In Progress)
An application to extract and query medical record PDFs

[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme) | [![run unit tests](https://github.com/chris-lovejoy/medical-pdf-reader/actions/workflows/run_pytests.yml/badge.svg)](https://github.com/chris-lovejoy/medical-pdf-reader/actions/workflows/run_pytests.yml)


## Table of Contents

- [About](#about)
- [Setup](#setup)
- [Usage](#usage)


## About
The purpose of this app is to enable a user to upload a PDF of a medical record and perform two main tasks:
1. Extract the information from that PDF into a structured format
2. Execute queries (using large language models) from the information in that structured format.


## Setup

### Interactive Webapp
The easiest way to interact with the app is to visit the streamlit app at [this link](https://medical-pdf-reader.streamlit.app/).


### Running it locally
To run it locally, take the following steps:

#### 1. Install the required dependencies

Create a virtual environment. For example:
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


#### 2. Add your API keys to .env
The format is specified in [.env.example](.env.example).

(Note: if you don't add a hugging face API key, some of the unit tests will fail. You can prevent this by commenting out using the huggingface API import in [models.py](./src/models.py).)


#### 3. Modify models and parameters in [models.py](./src/models.py), as per preference

<!-- TODO: consider adding a new config.py file with other considerations -->


## Usage

- run python main.py
- or visualise in streamlit app
- (can run local testing with pytest)





