#  Export Cognito Users

This script exports users from AWS Cognito Pool into a CSV file

## Install Dependencies

In order to install the dependencies you should have Python 2 or Python 3 installed on your platform, run any of below command depend on python version installed
- Python 2: 

    `$ pip install -r requirements.txt`
- Python 3: 

    `$ pip3 install -r requirements.txt`

## Run Script

To start export process you shout run below command (__Note__: use `python` if you have Python 2 installed)
- `$ python3 export-cognito-users.py  --poolId 'eu-west-1_XXXXXXXXX' --region eu-west-1`
### Script Arguments

- `--poolId` [__Required__] - Provide user pool ID pf the user pool from which you want to export the users
- `--region` [_Optional_] - Provide AWS region in which the user pool is present _Default_: `eu-west-1`
###### Note:

If you want to use specific AWS profile you can use __AWS_PROFILE__ like below,

`$ AWS_PROFILE={profile-name} python3 export-cognito-users.py  --poolId 'eu-west-1_XXXXXXXXX' --region eu-west-1`