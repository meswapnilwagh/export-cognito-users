import boto3
import time
import argparse
from datetime import date
from datetime import datetime

TODAY = date.today().strftime("%b-%d-%Y")
AWS_REGION = ''
COGNITO_USER_POOL_ID = ''
LIMIT = 60
MAX_RECORDS = 0 # 0 means ALL records 
EXPORT_ATTRIBUTES = ["UserCreateDate","UserStatus","Enabled","phone_number"]
EXPORT_FILE_NAME = 'Cognito-User-{0}.csv'.format(TODAY)

parser = argparse.ArgumentParser(description='', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--poolId', type=str, help="Provide User pool Id", required=True)
parser.add_argument('--region', type=str, default='eu-west-1', help="Provide region of user pool")
args = parser.parse_args()

if args.poolId:
    COGNITO_USER_POOL_ID = args.poolId
if args.region:
    AWS_REGION = args.region

client = boto3.client('cognito-idp', AWS_REGION)
newFileLine = {EXPORT_ATTRIBUTES[i]: '' for i in range(len(EXPORT_ATTRIBUTES))}
try:
    exportFile = open(EXPORT_FILE_NAME, 'w')
    exportFile.write(",".join(newFileLine.keys()) + '\n')
except Exception as err:
    error_message = repr(err)
    print("\tError Reason: " + error_message)
    exit()    

def get_list_cognito_users(cognitoClient, nextPaginationToken ='', Limit = LIMIT):
    return cognitoClient.list_users(
        UserPoolId = COGNITO_USER_POOL_ID,
        Limit = Limit,
        PaginationToken = nextPaginationToken
    ) if nextPaginationToken else cognitoClient.list_users(
        UserPoolId = COGNITO_USER_POOL_ID,
        Limit = Limit
    ) 

paginationCounter = 0
exportedCounter = 0
paginationToken = ""
while paginationToken is not None:
    fileLines = []
    try:
        userRecords = get_list_cognito_users(
            cognitoClient = client,
            nextPaginationToken = paginationToken,
            Limit = LIMIT if LIMIT < MAX_RECORDS else MAX_RECORDS
        )
    except client.exceptions.ClientError as err:
        error_message = err.response["Error"]["Message"]
        print("Please Check your Cognito User Pool configs")
        print("Error Reason: " + error_message)
        exportFile.close()
        exit()
    except:
        print("Something else went wrong")
        exportFile.close()
        exit()     

    if set(["PaginationToken","NextToken"]).intersection(set(userRecords)):
        paginationToken = userRecords['PaginationToken'] if "PaginationToken" in userRecords else userRecords['NextToken']
    else:
        paginationToken = None
    
    for user in userRecords['Users']:
        fileLine = newFileLine.copy()
        for attribute in EXPORT_ATTRIBUTES:
            fileLine[attribute] = ''
            if attribute in user.keys():
                fileLine[attribute] = str(user[attribute])
                continue
            for usr_attr in user['Attributes']:
                if usr_attr['Name'] == attribute:
                    fileLine[attribute] = str(usr_attr['Value'])
        
        fileLines.append(",".join(fileLine.values()) + '\n')       
    
    exportFile.writelines(fileLines)

    paginationCounter += 1
    exportedCounter += len(fileLines)
    print("Page: #{} \n Total Exported Records: #{} \n".format(str(paginationCounter), str(exportedCounter)))

    if MAX_RECORDS and exportedCounter >= MAX_RECORDS:
        print("INFO: Max Number of Exported Reached")
        break    

    if paginationToken is None:
        print("INFO: End of Cognito User Pool reached")

    time.sleep(0.15)

exportFile.close()        