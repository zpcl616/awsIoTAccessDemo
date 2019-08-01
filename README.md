# 如何把设备安全的接入AWS IoT

# 1. 简介

AWS IoT服务支持多种协议和认证授权的方式，且分别有其适用的场景。

# 2. AWS IoT支持的协议

设备要接入AWS IoT，首先要使用AWS IoT支持的协议来跟IoT平台交互。

## 2.1 http协议

http协议是互联网中最为常见的协议，http也支持后面提到所有的认证和授权的方式。但是在物联网的场景中，它也有着协议开销比较大的缺点，另外http只有请求响应的模式，不支持物联网场景中非常重要的订阅模式，不能支持下行消息的下发。
http协议可以使用各种语言的http库进行编码，AWS也通过AWS SDK对http协议提供了部分支持。

## 2.2 mqtt协议

mqtt协议是物联网场景中使用最为广泛的协议，具有协议开销小，支持发布订阅等所有模式的优点。它只支持X509证书的认证方式。
AWS通过AWS IoT SDK提供对mqtt协议的支持。

## 2.3 mqtt over websocket

mqtt over websocket是基于websocket上的mqtt协议，也具备mqtt协议的优点，另外它使用了443的端口，在网络环境可达性上比mqtt更有优势，但是也相对更为复杂一些。
AWS通过AWS IoT SDK提供对mqtt over websocket的支持。

# 3. AWS IoT支持的认证和授权

设备接入AWS IoT的时候，必须要进行认证，确认设备的合法身份。通过认证后，还需要对设备的请求进行鉴权，只有经过授权的请求才会被AWS IoT接受。不同的设备认证方式，其授权方式也可能会有所不同。

## 3.1 IAM Identities(user, group, role)

可以使用IAM提供的身份来认证设备。设备需要预置或者通过其他方式获取security credential，再通过SigV4的签名算法对与IoT交互的请求进行签名。AWS IoT服务通过SigV4的签名算法来认证设备的身份。通过认证后，再根据身份拥有的IAM policy来对请求进行鉴权，流程如下图所示：
[Image: image.png]
## 3.2 Cognito Identities

使用使用第三方的身份，如google，facebook，OIDC，SAML等，或者用户开发的自定义的身份，然后在Cognito身份池中交换得到Cognito身份，并使用这个身份来认证设备。Cognito身份的鉴权方式比较负责，首先Cognito身份池会为经过认证的身份配置一个role，进而使用role的policy对请求进行鉴权，另外，Cognito身份也会在IoT中绑定一个IoT Policy，这个IoT policy也会对请求进行鉴权。所以说，Cognito身份的最终权限是身份池role的IAM policy与Cognito身份的IoT policy的交集。由于IoT policy支持很多策略变量，通常的建议是，IAM policy可以给一个相对大的权限，然后在IoT policy中实现精细化的权限管理。
[Image: image.png]
## 3.3 X509证书

使用X509证书来认证设备。认证通过后，通过X509证书绑定的IoT policy对请求进行鉴权。
[Image: image.png]

## 3.4 Custom Authentication

使用自己定义的authorizer来认证设备，实际上是通过编写的lambda逻辑来对设备进行认证。认证通过后，lambda函数返回一个IoT policy，AWS IoT根据这个IoT policy来对请求进行鉴权。
[Image: image.png]
# 4. 准备工作

安装配置aws cli，安装jq

```
pip install awscli --user
pip install jq --user
```

下载代码

```
cd ~
git clone https://github.com/zpcl616/awsIoTAccessDemo.git
```

进入代码目录

```
cd awsIoTAccessDemo/src
```

下载AWS IoT的Root CA文件

```
wget https://www.amazontrust.com/repository/AmazonRootCA1.pem
```

依次登陆AWS控制台，打开服务—〉AWS IoT—〉测试—〉订阅主题—〉输入“IoTDemo/#”—〉点击订阅主题。
Demo过程中设备发送的消息可以在这里看到结果。

获取account id

```
account_id=`aws sts get-caller-identity | jq .Account|sed 's/"//g'`
```

获取AWS IoT的customer endpoint

```
endpoint_prefix=`aws iot describe-endpoint \
| jq .endpointAddress | sed 's/"//g'| awk -F . '{print $1}'`
```

> 注意，后续在每个新开的shell窗口都要执行这两步以获取account_id和endpoint_prefix。

# 5. 设备接入场景

## 5.1 IAM Identity认证方式

首先，创建一个IAM user，IoTDeviceUser。

```
aws iam create-user --user-name IoTDeviceUser
```

为IoTDeviceUser用户创建access key

```
aws iam create-access-key \
    --user-name IoTDeviceUser1 > /tmp/IoT_demo_access_key
```

记录下AccessKeyId和SecretAccessKey

```
AccessKeyId=`cat /tmp/IoT_demo_access_key| jq .AccessKey.AccessKeyId`
SecretAccessKey=`cat /tmp/IoT_demo_access_key| jq .AccessKey.SecretAccessKey`
```

### 5.1.1 http协议

为设备创建IAM policy

```
device_IAM_http_policy_arn=`aws iam create-policy \
--policy-name IoTDeviceIAMHttpPolicy \
--policy-document "{
    \"Version\": \"2012-10-17\",
    \"Statement\": [
        {
            \"Sid\": \"VisualEditor0\",
            \"Effect\": \"Allow\",
            \"Action\": \"iot:Publish\",
            \"Resource\": [
                \"arn:aws-cn:iot:cn-north-1:${account_id}:topic/IoTDemo/device_IAM_http\"
            ]
        }
    ]
}" | jq .Policy.Arn`
```

把policy绑定IAM user。

```
aws iam attach-user-policy --user-name IoTDeviceUser \
--policy-arn ${device_IAM_http_policy_arn}
```

运行设备模拟程序。

```
python device_IAM_http.py --data "data from device IAM http." \
--AccessKeyId ${AccessKeyId} --SecretAccessKey ${SecretAccessKey}
```

然后在第4章节打开的控制台中查看收到的消息（后面不再赘述）。

### 5.1.2 mqtt over websocket

为设备创建IAM policy

```
device_IAM_websocket_policy_arn=`aws iam create-policy \
--policy-name IoTDeviceIAMWebsocketPolicy \
--policy-document "{
    \"Version\": \"2012-10-17\",
    \"Statement\": [
        {
            \"Sid\": \"VisualEditor0\",
            \"Effect\": \"Allow\",
            \"Action\": [
                \"iot:Publish\",
                \"iot:Receive\"
            ],
            \"Resource\": \"arn:aws-cn:iot:cn-north-1:${account_id}:topic/IoTDemo/device_IAM_websocket\"
        },
        {
            \"Sid\": \"VisualEditor1\",
            \"Effect\": \"Allow\",
            \"Action\": \"iot:Connect\",
            \"Resource\": \"arn:aws-cn:iot:cn-north-1:${account_id}:client/device_IAM_websocket\"
        },
        {
            \"Sid\": \"VisualEditor2\",
            \"Effect\": \"Allow\",
            \"Action\": \"iot:Subscribe\",
            \"Resource\": \"arn:aws-cn:iot:cn-north-1:${account_id}:topicfilter/IoTDemo/device_IAM_websocket\"
        }
    ]
}" | jq .Policy.Arn`
```

把policy绑定IAM user。

```
aws iam attach-user-policy --user-name IoTDeviceUser \
--policy-arn ${device_IAM_websocket_policy_arn}
```

运行设备模拟程序

```
python device_IAM_websocket.py --endpoint_prefix ${endpoint_prefix} \
--AccessKeyId ${AccessKeyId} --SecretAccessKey ${SecretAccessKey}
```

设备模拟程序会一直运行，订阅自己的topic。在控制台输入要发送到AWS IoT的消息，“data from device IAM websocket.”，设备会接收到自己发送的这个消息。同时，在控制台中也可以看到此设备发送的消息。

执行ctrl+C停止程序，或者重新打开一个shell窗口。如果打开新的shell窗口，需要定位到awsIoTAccessDemo/src目录，同时获取变量account_id和endpoint_prefix。

```
cd ~/awsIoTAccessDemo/src
account_id=`aws sts ``get``-``caller``-``identity ``|`` jq ``.``Account``|``sed ``'s/"//g'`
endpoint_prefix=`aws iot describe-endpoint \
| jq .endpointAddress | sed 's/"//g'| awk -F . '{print $1}'`
```

## 5.2 Cognito Identities认证方式

首先，创建Cognito身份池

```
IdentityPoolId=`aws cognito-identity create-identity-pool \
--identity-pool-name IoTDevicesPool \
--no-allow-unauthenticated-identities \
--developer-provider-name login.IoTDemo.dev`
```


创建经过认证的Cognito Identity代入的role。

```
IoTDeviceRoleInCognitoArn=`aws iam create-role \
--role-name IoTDeviceRoleInCognito \
--assume-role-policy-document "{
  \"Version\": \"2012-10-17\",
  \"Statement\": [
    {
      \"Effect\": \"Allow\",
      \"Principal\": {
        \"Federated\": \"cognito-identity.amazonaws.com\"
      },
      \"Action\": \"sts:AssumeRoleWithWebIdentity\",
      \"Condition\": {
        \"StringEquals\": {
          \"cognito-identity.amazonaws.com:aud\": \"${IdentityPoolId}\"
        },
        \"ForAnyValue:StringLike\": {
          \"cognito-identity.amazonaws.com:amr\": \"authenticated\"
        }
      }
    }
  ]
}" | jq .Role.Arn`
```


绑定role到cognito身份池

```
aws cognito-identity set-identity-pool-roles \
--identity-pool-id ${IdentityPoolId} \
--roles authenticated=${IoTDeviceRoleInCognitoArn}
```

给role绑定可以attach policy的权限

> 设备在使用cognito身份接入IoT的时候，还需要为其attach一个IoT的policy。 通常情况下，考虑权限的安全，这一步需要在后端的服务来执行，这里为了简化，由设备来为自己attach policy，生产系统中应该禁止使用这种方法。

```
IoTPolicyManagerArn=`aws iam create-policy \
--policy-name IoTPolicyManager \
--policy-document "{
    \"Version\": \"2012-10-17\",
    \"Statement\": [
        {
            \"Sid\": \"VisualEditor0\",
            \"Effect\": \"Allow\",
            \"Action\": \"iot:AttachPolicy\",
            \"Resource\": \"arn:aws-cn:iot:cn-north-1:${account_id}:policy/*\"
        }
    ]
}" | jq .Policy.Arn`
```

把policy attach到role

```
aws iam attach-role-policy --role-name IoTDeviceRoleInCognito \
--policy-arn ${IoTPolicyManagerArn}
```

Cognito身份池支持多种身份认证的方式，这里使用了developer provider来获取身份并交换Cognito身份。
创建一个IAM user，developerIdpUser，用来获取developer provider的权限

```
aws iam create-user --user-name developerIdpUser
```

创建策略，并把策略attach到developerIdpUser

```
developerIdpPolicy_arn=`aws iam create-policy \
--policy-name developerIdpPolicy \
--policy-document "{
    \"Version\": \"2012-10-17\",
    \"Statement\": [
        {
        \"Sid\": \"VisualEditor0\",
        \"Effect\": \"Allow\",
        \"Action\": \"cognito-identity:GetOpenIdTokenForDeveloperIdentity\",
        \"Resource\": \"arn:aws-cn:cognito-identity:cn-north-1:${account_id}:identitypool/${IdentityPoolId}\"
        }
    ]
}" | jq .Policy.Arn`
```

```
aws iam attach-user-policy --user-name developerIdpUser \
--policy-arn ${developerIdpPolicy_arn}
```

为developerIdpUser用户创建access key

```
aws iam create-access-key \
    --user-name developerIdpUser > /tmp/IoT_demo_access_key2
```

记录下AccessKeyId和SecretAccessKey

```
AccessKeyId=`cat /tmp/IoT_demo_access_key2 | jq .AccessKey.AccessKeyId`
SecretAccessKey=`cat /tmp/IoT_demo_access_key2 | jq .AccessKey.SecretAccessKey`
```

运行developer_provider.py

```
python developer_provider.py --identityPoolId ${IdentityPoolId} \
--AccessKeyId ${AccessKeyId} --SecretAccessKey ${SecretAccessKey}
```

developer_provider.py会在在http://0.0.0.0:8383/ 接受请求，并返回Cognito身份池的身份信息。

### 5.2.1 http协议

打开一个新的shell窗口，定位到awsIoTAccessDemo/src目录，同时获取变量account_id和endpoint_prefix。

```
cd ~/awsIoTAccessDemo/src
account_id=`aws sts ``get``-``caller``-``identity ``|`` jq ``.``Account``|``sed ``'s/"//g'`
endpoint_prefix=`aws iot describe-endpoint \
| jq .endpointAddress | sed 's/"//g'| awk -F . '{print $1}'`
```

通过Cognito方式认证的设备，需要IAM policy和IoT policy同时授权。
为设备创建IAM policy，并将其attach到Cognito role

```
IoTDeviceCognitoHttpPolicyArn=`aws iam create-policy \
--policy-name IoTDeviceCognitoHttpPolicy \
--policy-document "{
    \"Version\": \"2012-10-17\",
    \"Statement\": [
        {
            \"Sid\": \"VisualEditor0\",
            \"Effect\": \"Allow\",
            \"Action\": \"iot:Publish\",
            \"Resource\": [
                \"arn:aws-cn:iot:cn-north-1:${account id}:topic/IoTDemo/device_cognito_http\"
            ]
        }
    ]
}" | jq .Policy.Arn`
```

```
aws iam attach-role-policy --role-name IoTDeviceRoleInCognito \
--policy-arn ${IoTDeviceCognitoHttpPolicyArn}
```

创建IoT policy

```
aws iot create-policy --policy-name IoTPolicyForDeviceCognitohttp \
 --policy-document "{
    \"Version\": \"2012-10-17\",
    \"Statement\": [
        {
        \"Effect\": \"Allow\",
        \"Action\": \"iot:Publish\",
        \"Resource\": [
                \"arn:aws-cn:iot:cn-north-1:${account_id}:topic/IoTDemo/device_cognito_http\"
            ]
        }
    ]
}"
```

运行设备模拟程序发送消息。

```
python device_cognito_http.py --data "data from device cognito http." \
--developer_provicer_endpoint "http://127.0.0.1:8383/login/" \
--iot_policy_name IoTPolicyForDeviceCognitohttp
```

在控制台查看接受到的消息。

### 5.2.2 mqtt over websocket协议

为设备创建IAM policy，并将其attach到Cognito role

```
IoTDeviceCognitoWebsocketPolicyArn=`aws iam create-policy \
--policy-name IoTDeviceCognitoWebsocketPolicy \
--policy-document "{
    \"Version\": \"2012-10-17\",
    \"Statement\": [
        {
            \"Sid\": \"VisualEditor0\",
            \"Effect\": \"Allow\",
            \"Action\": [
                \"iot:Publish\",
                \"iot:Receive\"
            ],
            \"Resource\": \"arn:aws-cn:iot:cn-north-1:${account_id}:topic/IoTDemo/device_cognito_websocket\"
        },
        {
            \"Sid\": \"VisualEditor1\",
            \"Effect\": \"Allow\",
            \"Action\": \"iot:Connect\",
            \"Resource\": \"arn:aws-cn:iot:cn-north-1:${account_id}:client/device_cognito_websocket\"
        },
        {
            \"Sid\": \"VisualEditor2\",
            \"Effect\": \"Allow\",
            \"Action\": \"iot:Subscribe\",
            \"Resource\": \"arn:aws-cn:iot:cn-north-1:${account_id}:topicfilter/IoTDemo/device_cognito_websocket\"
        }
    ]
} | jq .Policy.Arn`
```

```
aws iam attach-role-policy --role-name IoTDeviceRoleInCognito \
--policy-arn ${IoTDeviceCognitoWebsocketPolicyArn}
```

创建IoT policy

```
aws iot create-policy --policy-name IoTPolicyForDeviceCognitoWebsocket \
--policy-document "{
\"Version\": \"2012-10-17\",
    \"Statement\": [
        {
            \"Sid\": \"VisualEditor0\",
            \"Effect\": \"Allow\",
            \"Action\": [
                \"iot:Publish\",
                \"iot:Receive\"
            ],
            \"Resource\": \"arn:aws-cn:iot:cn-north-1:${account_id}:topic/IoTDemo/device_cognito_websocket\"
        },
        {
            \"Sid\": \"VisualEditor1\",
            \"Effect\": \"Allow\",
            \"Action\": \"iot:Connect\",
            \"Resource\": \"arn:aws-cn:iot:cn-north-1:${account_id}:client/device_cognito_websocket\"
        },
        {
            \"Sid\": \"VisualEditor2\",
            \"Effect\": \"Allow\",
            \"Action\": \"iot:Subscribe\",
            \"Resource\": \"arn:aws-cn:iot:cn-north-1:${account_id}:topicfilter/IoTDemo/device_cognito_websocket\"
        }
    ]
} 
```

运行设备模拟程序

```
python device_cognito_websocket.py \
--developer_provicer_endpoint "http://127.0.0.1:8383/login/" \
--iot_policy_name IoTPolicyForDeviceCognitoWebsocket \
--endpoint_prefix ${endpoint_prefix}
```

设备模拟程序会一直运行，订阅自己的topic。在控制台输入要发送到AWS IoT的消息，“data from device Cognito websocket.”，设备会接收到自己发送的这个消息。同时，在控制台中也可以看到此设备发送的消息。

执行ctrl+C停止程序，或者重新打开一个shell窗口。如果打开新的shell窗口，需要定位到awsIoTAccessDemo/src目录，同时获取变量account_id和endpoint_prefix。

```
cd ~/awsIoTAccessDemo/src
account_id=`aws sts ``get``-``caller``-``identity ``|`` jq ``.``Account``|``sed ``'s/"//g'`
endpoint_prefix=`aws iot describe-endpoint \
| jq .endpointAddress | sed 's/"//g'| awk -F . '{print $1}'`
```

## 5.3 X.509证书认证方式

### 5.3.1 http协议

为设备创建证书

```
device_x509_http_crt_arn=`aws iot create-keys-and-certificate \
--set-as-active --certificate-pem-outfile device_x509_http.crt \
--public-key-outfile device_x509_http.pem --private-key-outfile device_x509_http.key \
| jq .certificateArn`
```

为设备创建IoT policy

```
aws iot create-policy --policy name IoTPolicyForDeviceX509Http \
--policy-document "{
  \"Version\": \"2012-10-17\",
  \"Statement\": [
    {
      \"Effect\": \"Allow\",
      \"Action\": \"iot:Publish\",
      \"Resource\": [
        \"arn:aws-cn:iot:cn-north-1:${account_id}:topic/IoTDemo/device_x509_http\"
      ]
    }
  ]
}"
```

把IoT policy attach到设备证书

```
aws iot attach-policy --policy-name IoTPolicyForDeviceX509Http \
--target ${device_x509_http_crt_arn}
```

运行设备模拟程序

```
python device_x509_http.py --data "data from device x509 http."\
--endpoint_prefix ${endpoint_prefix} \
--client_cert ./device_x509_http.crt \
--client_key ./device_x509_http.key
```

在控制台上查看收到的消息。

### 5.3.2 mqtt协议

为设备创建证书

```
device_x509_mqtt_crt_arn=`aws iot create-keys-and-certificate \
--set-as-active --certificate-pem-outfile device_x509_mqtt.crt \
--public-key-outfile device_x509_mqtt.pem --private-key-outfile device_x509_mqtt.key \
| jq .certificateArn`
```

为设备创建IoT policy

```
aws iot create-policy --policy name IoTPolicyForDeviceX509Mqtt \
--policy-document "{
  \"Version\": \"2012-10-17\",
    \"Statement\": [
        {
            \"Sid\": \"VisualEditor0\",
            \"Effect\": \"Allow\",
            \"Action\": [
                \"iot:Publish\",
                \"iot:Receive\"
            ],
            \"Resource\": \"arn:aws-cn:iot:cn-north-1:${account_id}:topic/IoTDemo/device_x509_mqtt\"
        },
        {
            \"Sid\": \"VisualEditor1\",
            \"Effect\": \"Allow\",
            \"Action\": \"iot:Connect\",
            \"Resource\": \"arn:aws-cn:iot:cn-north-1:${account_id}:client/device_x509_mqtt\"
        },
        {
            \"Sid\": \"VisualEditor2\",
            \"Effect\": \"Allow\",
            \"Action\": \"iot:Subscribe\",
            \"Resource\": \"arn:aws-cn:iot:cn-north-1:${account_id}:topicfilter/IoTDemo/device_x509_mqtt\"
        }
    ]
} 
```

把IoT policy attach到设备证书

```
aws iot attach-policy --policy-name IoTPolicyForDeviceX509Mqtt \
--target ${device_x509_mqtt_crt_arn}
```

运行设备模拟程序

```
python device_x509_mqtt.py \
--endpoint_prefix ${endpoint_prefix} \
--client_cert ./device_x509_mqtt.crt \
--client_key ./device_x509_mqtt.key
```

设备模拟程序会一直运行，订阅自己的topic。在控制台输入要发送到AWS IoT的消息，“data from device x509 mqtt.”，设备会接收到自己发送的这个消息。同时，在控制台中也可以看到此设备发送的消息。

执行ctrl+C停止程序，或者重新打开一个shell窗口。如果打开新的shell窗口，需要定位到awsIoTAccessDemo/src目录，同时获取变量account_id和endpoint_prefix。

```
cd ~/awsIoTAccessDemo/src
account_id=`aws sts ``get``-``caller``-``identity ``|`` jq ``.``Account``|``sed ``'s/"//g'`
endpoint_prefix=`aws iot describe-endpoint \
| jq .endpointAddress | sed 's/"//g'| awk -F . '{print $1}'`
```

## 5.4 Custom Authentication

Custom Authentication是由lambda函数来认证授权，所以先要创建lambda。
创建lambda要代入的role

```
IoTDemoAuthorizerFunctionRoleArn=`aws iam create-role \
--role-name IoTDemoAuthorizerFunctionRole \
--assume-role-policy-document "{
  \"Version\": \"2012-10-17\",
  \"Statement\": [
    {
      \"Effect\": \"Allow\",
      \"Principal\": {
        \"Service\": \"lambda.amazonaws.com\"
      },
      \"Action\": \"sts:AssumeRole\"
    }
  ]
}" | jq .Role.Arn | sed 's/"//g'`
```

为lambda角色attach一个policy 

```
aws iam attach-role-policy --role-name IoTDemoAuthorizerFunctionRole \
--policy-arn arn:aws-cn:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
```

创建lambda函数

```
zip function.zip  IoTDemoAuthorizerFunction.py
`IoTDemoAuthorizerFunctionArn``=```aws ``lambda`` create``-``function`` ``\`
`--``function``-``name ``IoTDemoAuthorizerFunction`` \`
`--``zip``-``file fileb``:``//function.zip --handler IoTDemoAuthorizerFunction.lambda_handler \`
`--``runtime python2.7`` ``--``role $``{``IoTDemoAuthorizerFunctionRoleArn``}`` ``\`
`| jq ``.FunctionArn | sed 's/"//g'``` `
```

创建authorizer用于验证token的密钥对

```
`openssl genrsa ``-``out`` ``authorizer``_private``.``pem ``2048`
`openssl rsa ``-``in`` authorizer_private``.``pem ``-``outform PEM ``-``pubout ``-``out`` authorizer_public``.``pem`
```

创建authorizer

```
`authorizerArn=`aws iot create``-``authorizer ``\
-``-``authorizer``-``name ``IoTDemoAuthorizer`` ``\`
`--``authorizer``-``function``-``arn $``{``IoTDemoAuthorizerFunction``Arn}`` ``\`
`--``token``-``key``-``name ``IoTDemoAuthorizerToken`` ``\`
`--``token``-``signing``-``public``-``keys FIRST_KEY``=``"\`cat authorizer_public.pem\```" ``\`
`--``status ACTIVE`` ``|`` jq ``.``authorizerArn | sed 's/"//g'``
```

为authorizer配置调用lambda的权限

```
aws lambda add-permission --function-name IoTDemoAuthorizerFunction \
--statement-id IoTDemoAuthorizerFunctionPermission \
--action 'lambda:InvokeFunction' \
--principal iot.amazonaws.com \
--source-arn `$``{authorizerArn``}`
```

### 5.4.1 http协议

运行设备模拟程序

> 需要注意的是目前实际测试custom authentication认证授权方式下，不支持ATS endpoint，代码中需注意。另外custom authentication也暂时没有python SDK的支持，需要自己编写代码。

```
python device_custom_auth_http.py \
--data "data from device custom authentication http." \
--authorizer_name `IoTDemoAuthorizer \`
--endpoint_prefix ${endpoint_prefix} \
--private_key `authorizer_private``.``pem`
```

在控制台上查看收到的消息。

### 5.4.2 mqtt over websocket协议

由于Custom Authentication不支持ATS endpoint，需要下载VeriSign endpoint的证书。

```
wget https://www.symantec.com/content/en/us/enterprise/verisign/roots/VeriSign-Class%203-Public-Primary-Certification-Authority-G5.pem
```

运行设备模拟程序

```
python device_custom_auth_websocket.py \
--endpoint_prefix ${endpoint_prefix} \
--authorizer_name `IoTDemoAuthorizer``
--private_key authorizer_private.pem`
```

