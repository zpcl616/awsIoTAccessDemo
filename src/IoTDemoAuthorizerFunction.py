from __future__ import print_function

import json
import base64

def lambda_handler(event, context):
    try:
        
        token = json.loads(base64.b64decode(event['token']))
        device_id = token['device_id']

        policyDocuments = []
        policyDocument = {}
        policyDocument['Version'] = '2012-10-17'
        policyDocument['Statement'] = []
        statement0 = {}
        statement0['Action'] = 'iot:Publish'
        statement0['Effect'] = 'Allow'
        statement0['Resource'] = "arn:aws-cn:iot:cn-north-1:*:topic/IoTDemo/"+device_id
        policyDocument['Statement'].append(statement0)
        statement1 = {}
        statement1['Action'] = 'iot:Subscribe'
        statement1['Effect'] = 'Allow'
        statement1['Resource'] = "arn:aws-cn:iot:cn-north-1:*:topicfilter/IoTDemo/"+device_id
        policyDocument['Statement'].append(statement1)

        policyDocuments.append(policyDocument)
        authResponse = {}
        authResponse['isAuthenticated'] = True
        authResponse['principalId'] = device_id.replace('_','')
        authResponse['disconnectAfterInSeconds'] = 3600
        authResponse['refreshAfterInSeconds'] = 600
        authResponse['policyDocuments'] = policyDocuments
        print(str(authResponse))
        return authResponse
    except Exception as e:
        print(str(e))
        return {}

