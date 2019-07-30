#!/usr/bin/env python
# -*- coding: utf-8 -*-

import boto3
import argparse
import json
from flask import Flask, abort, request, jsonify

#获取参数
parser = argparse.ArgumentParser(description='developer idp provider.')
parser.add_argument('--developer_provider_name', default='login.IoTDemo.dev',
            help='developer_provider_name')
parser.add_argument('--identityPoolId', required=True,
            help='identityPoolId')
parser.add_argument('--AccessKeyId', required=True,
            help='AccessKeyId')
parser.add_argument('--SecretAccessKey', required=True,
            help='SecretAccessKey')

args = parser.parse_args()
developer_provider_name = args.developer_provider_name
identityPoolId = args.identityPoolId
access_key_id = args.AccessKeyId
secret_access_key = args.SecretAccessKey

app = Flask(__name__)

region = 'cn-north-1'
tokenDuration = 3600

cognito_client = boto3.client('cognito-identity',region_name=region,aws_access_key_id=access_key_id,aws_secret_access_key=secret_access_key)
#cognito_client = boto3.client('cognito-identity',region_name=region)

@app.route('/login/', methods=['POST'])
def login():
    if not request.json or 'device_id' not in request.json:
        abort(400)

    device_id = request.json['device_id']

    try:
        response = cognito_client.get_open_id_token_for_developer_identity(IdentityPoolId=identityPoolId,Logins={developer_provider_name:device_id},TokenDuration=tokenDuration)
        token = response['Token']
        identityId = response['IdentityId']
        return jsonify({'result': 'success','identityId':identityId,'token':token})
    except Exception as e:
        return jsonify({'result': 'failed'})

if __name__ == "__main__":
    # 将host设置为0.0.0.0，则外网用户也可以访问到这个服务
    app.run(host="0.0.0.0", port=8383, debug=True)
