# Traffic Data Collector

This project creates a aws lambda function that reads every 5 minutes the traffic data from the google maps distance matrix api, the the responses are saved int a s3 bocket.

The porpuse of this is to create the data source used in a ETL process.

## Setup

```shell
# install pipenv if not already installed, python 3.7 required
pip install pipenv
# Install python dependencies
pipenv install
# Install node dependencies, nodejs 10+ with npm 6+ required
npm install
#deploy, you need to have your aws credentials configured 
npm run deploy -- --GOOGLE_MAPS_API_KEY <put_here_your_api_key>
```

## Test

```bash
pipenv shell
export GOOGLE_MAPS_API_KEY=<your_google_key>
python -m unittest
# ...
# ----------------------------------------------------------------------
# Ran 3 tests in 0.862s

# OK
```
