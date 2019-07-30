#!/usr/bin/env python
# -*- coding: utf-8 -*-

import boto3
import argparse
import json
import requests

#获取参数
parser = argparse.ArgumentParser(description='Send data to IoT Core')
parser.add_argument('--data', default="data from device_cognito_http",
            help='data to IoT')
parser.add_argument('--iot_policy_name', default="IoTPolicyForDeviceCognitohttp",
            help='iot policy name for device cognito http.')
parser.add_argument('--developer_provicer_endpoint', default="http://127.0.0.1:8383/login/",
            help='developer ID provider endpoint')

args = parser.parse_args()
data = args.data
policy_name = args.iot_policy_name
developer_provicer_endpoint = args.developer_provicer_endpoint

device_name = 'device_cognito_http'
region = 'cn-north-1'
topic = "IoTDemo/"+device_name

headers = {"Content-Type": "application/json"}
body = {"device_id":device_name}
r1 = requests.post(developer_provicer_endpoint, data=json.dumps(body), headers = headers)

token = json.loads(r1.text)['token']
identityId = json.loads(r1.text)['identityId']

cognito_client = boto3.client('cognito-identity', region_name=region)
response = cognito_client.get_credentials_for_identity(IdentityId=identityId, Logins={'cognito-identity.cn-north-1.amazonaws.com.cn':token})

sessionToken=response['Credentials']['SessionToken']
accessKeyId=response['Credentials']['AccessKeyId']
secretKey=response['Credentials']['SecretKey']

iot_client = boto3.client('iot',region_name=region,aws_access_key_id=accessKeyId,aws_secret_access_key=secretKey,aws_session_token=sessionToken)

response = iot_client.attach_policy(
    policyName=policy_name,
    target=identityId
)

iot_data_client = boto3.client('iot-data',region_name=region,aws_access_key_id=accessKeyId,aws_secret_access_key=secretKey,aws_session_token=sessionToken)

if data:
    response = iot_data_client.publish(
        topic=topic,
        qos=0,
        payload=json.dumps({"source":device_name, "data":data})
    )
    #print response

