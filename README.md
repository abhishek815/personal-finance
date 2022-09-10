# Personal Finance Sheet Creator

**NOTE: This repo is not complete, still work in progress.**

## Prerequisite
- [Intuit Mint Account](https://mint.intuit.com/)
- IMAP Enabled on the email account associated with your Mint Account (currently only compatible with gmail)
- Enviornment variables:
```
export MINT_EMAIL=XXX@gmail.com
export MINT_PWD=XXX
export EMAIL_PWD=XXX
```
## Usage: Python

```
pip install -r requirements.txt
PYTHONPATH=${PYTHONPATH}:${PWD}
python personal_finance/run.py -y 2022
```

The -y flag is the year you would like to generate data for and -f is the file directory you would like to store the data in. These values are defaulted to year=`2022` and file_dir=`./personal_finance/data`
