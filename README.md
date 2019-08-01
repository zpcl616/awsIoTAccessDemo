<!doctype html>
<html><head><title>如何把设备安全的接入AWS IoT</title><meta charset="UTF-8"><link href="http://fonts.googleapis.com/css?family=Crimson+Text:400,400italic,700,700italic|Roboto:400,700,700italic,400italic" rel="stylesheet" type="text/css"><style>/*
 * Copyright 2014 Quip
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may
 * not use this file except in compliance with the License. You may obtain
 * a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 * License for the specific language governing permissions and limitations
 * under the License.
 */

body {
    font-size: 15px;
    color: #333;
    background: white;
    padding: 60px 95px;
    max-width: 900px;
    margin: 0 auto;
    text-rendering: optimizeLegibility;
    font-feature-settings: "kern";
    font-kerning: normal;
    -moz-font-feature-settings: "kern";
    -webkit-font-feature-settings: "kern";
}

/* Headings */
h1,
h2,
h3,
th {
    font-family: Roboto, sans-serif;
    font-weight: 700;
    margin: 0;
    margin-top: 1.25em;
    margin-bottom: 0.75em;
}

h1 {
    font-size: 35px;
    line-height: 42px;
}

h1:first-child {
    margin-top: 0;
}

h2 {
    font-size: 18px;
    line-height: 22px;
}

h3 {
    text-transform: uppercase;
    font-size: 13px;
    line-height: 16px;
}

/* Body text */
body,
p,
ul,
ol,
td {
    font-family: "Crimson Text", serif;
    font-size: 16px;
    line-height: 20px;
}

blockquote,
q {
    display: block;
    margin: 1em 0;
    font-style: italic;
}

blockquote a,
q a {
    text-decoration: underline;
}

blockquote {
    padding-left: 10px;
    border-left: 4px solid #a6a6a6;
}

q {
    color: #a6a6a6;
    line-height: 40px;
    font-size: 24px;
    text-align: center;
    quotes: none;
}

q a {
    color: #a6a6a6;
}

code,
pre {
    font-family: Consolas, "Liberation Mono", Menlo, "Courier Prime Web",
        Courier, monospace;
    background: #f2f2f2;
}

code {
    padding: 1px;
    margin: 0 -1px;
    border-radius: 3px;
}

pre {
    display: block;
    line-height: 20px;
    text-shadow: 0 1px white;
    padding: 5px 5px 5px 30px;
    white-space: nowrap;
    position: relative;
    margin: 1em 0;
}

pre:before {
    content: "";
    position: absolute;
    top: 0;
    bottom: 0;
    left: 15px;
    border-left: solid 1px #dadada;
}

/* Lists */
div[data-section-style="5"],
div[data-section-style="6"],
div[data-section-style="7"] {
    margin: 12px 0;
}

ul {
    padding: 0 0 0 40px;
}

ul li {
    margin-bottom: 0.4em;
}

/* Bulleted list */
div[data-section-style="5"] ul {
    list-style-type: disc;
}
div[data-section-style="5"] ul ul {
    list-style-type: circle;
}
div[data-section-style="5"] ul ul ul {
    list-style-type: square;
}
div[data-section-style="5"] ul ul ul ul {
    list-style-type: disc;
}
div[data-section-style="5"] ul ul ul ul ul {
    list-style-type: circle;
}
div[data-section-style="5"] ul ul ul ul ul ul {
    list-style-type: square;
}

/* Numbered list */
div[data-section-style="6"] ul {
    list-style-type: decimal;
}
div[data-section-style="6"] ul ul {
    list-style-type: lower-alpha;
}
div[data-section-style="6"] ul ul ul {
    list-style-type: lower-roman;
}
div[data-section-style="6"] ul ul ul ul {
    list-style-type: decimal;
}
div[data-section-style="6"] ul ul ul ul ul {
    list-style-type: lower-alpha;
}
div[data-section-style="6"] ul ul ul ul ul ul {
    list-style-type: lower-roman;
}

/* Checklist */
div[data-section-style="7"] ul {
    list-style-type: none;
}

div[data-section-style="7"] ul li:before {
    content: "\2610";
    position: absolute;
    display: inline;
    margin-right: 1.2em;
    margin-left: -1.2em;
}

div[data-section-style="7"] ul li.parent:before {
    content: "";
}

div[data-section-style="7"] ul li.parent {
    font-weight: bold;
}

div[data-section-style="7"] ul li.checked {
    text-decoration: line-through;
}

div[data-section-style="7"] ul li.checked:before {
    content: "\2611";
    text-decoration: none;
}

/* Tables */
div[data-section-style="8"] {
    margin: 12px 0;
}

table {
    border-spacing: 0;
    border-collapse: separate;
    border: solid 1px #bbb;
    table-layout: fixed;
    position: relative;
}

table th,
table td {
    padding: 2px 2px 0;
    min-width: 1.5em;
    word-wrap: break-word;
}

table th {
    border-bottom: 1px solid #c7cbd1;
    background: #f2f2f2;
    font-weight: bold;
    vertical-align: bottom;
    color: #3a4449;
    text-align: center;
}

table td {
    padding-top: 0;
    border-left: 1px solid #c7cbd1;
    border-top: 1px solid #c7cbd1;
    vertical-align: top;
}

table td.bold {
    font-weight: bold;
}

table td.italic {
    font-style: italic;
}

table td.underline {
    text-decoration: underline;
}

table td.strikethrough {
    text-decoration: line-through;
}

table td.underline.strikethrough {
    text-decoration: underline line-through;
}

table td:first-child {
    border-left: hidden;
}

table tr:first-child td {
    border-top: hidden;
}

/* Images */
div[data-section-style="11"] {
    margin-top: 20px;
    margin-bottom: 20px;
    margin-left: auto;
    margin-right: auto;
}

div[data-section-style="11"][data-section-float="0"] {
    clear: both;
    text-align: center;
}

div[data-section-style="11"][data-section-float="1"] {
    float: left;
    clear: left;
    margin-right: 20px;
}

div[data-section-style="11"][data-section-float="2"] {
    float: right;
    clear: right;
    margin-left: 20px;
}

div[data-section-style="11"] img {
    display: block;
    max-width: 100%;
    height: auto;
    margin: auto;
}

hr {
    width: 70px;
    margin: 20px auto;
}

/* Apps */
div[data-section-style="19"].placeholder {
    margin: 0.8em auto;
    padding: 4px 0;
    display: block;
    color: #3d87f5;
    text-align: center;
    border: 1px solid rgba(41, 182, 242, 0.2);
    border-radius: 3px;
    background: #e9f8fe;
    font-family: Roboto, sans-serif;
}

div[data-section-style="19"].first-party-element {
    margin-bottom: 10px;
    background-repeat: no-repeat;
    background-size: contain;
}

div[data-section-style="19"].first-party-element.kanban {
    background-image: url("https://quip-cdn.com/nK0hSyhsb4jrLIL2s5Ma-g");
    height: 166px;
}

div[data-section-style="19"].first-party-element.calendar {
    background-image: url("https://quip-cdn.com/OYujqLny03RILxcLIiyERg");
    height: 244px;
}

div[data-section-style="19"].first-party-element.poll {
    background-image: url("https://quip-cdn.com/fbIiFrcKGv__4NB7CBfxoA");
    height: 116px;
}

div[data-section-style="19"].first-party-element.countdown {
    background-image: url("https://quip-cdn.com/3bPhykD2dBei9sSjCWteTQ");
    height: 96px;
}

div[data-section-style="19"].first-party-element.process_bar {
    background-image: url("https://quip-cdn.com/ybQlHnHEIIBLog5rZmYs_w");
    height: 36px;
}

div[data-section-style="19"].first-party-element.project_tracker {
    background-image: url("https://quip-cdn.com/OFQU087b4Mxzz1ZaHwtjXA");
    height: 164px;
}

div[data-section-style="19"] img {
    margin: 0.5em;
}

div[data-section-style="19"] img.masked-image {
    margin: 0;
    transform-origin: top left;
}

div[data-section-style="19"] .image-mask {
    position: relative;
    overflow: hidden;
}
</style></head><body><h1 id='TMK9CA64wPV'>如何把设备安全的接入AWS IoT</h1>

<h1 id='TMK9CAYlAHl'>1. 简介</h1>

AWS IoT服务支持多种协议和认证授权的方式，且分别有其适用的场景。<br/>

<h1 id='TMK9CA2qh8I'>2. AWS IoT支持的协议</h1>

设备要接入AWS IoT，首先要使用AWS IoT支持的协议来跟IoT平台交互。<br/>

<h2 id='TMK9CAaJ3EE'>2.1 http协议</h2>

http协议是互联网中最为常见的协议，http也支持后面提到所有的认证和授权的方式。但是在物联网的场景中，它也有着协议开销比较大的缺点，另外http只有请求响应的模式，不支持物联网场景中非常重要的订阅模式，不能支持下行消息的下发。<br/>

http协议可以使用各种语言的http库进行编码，AWS也通过AWS SDK对http协议提供了部分支持。<br/>

<h2 id='TMK9CAGDKy8'>2.2 mqtt协议</h2>

mqtt协议是物联网场景中使用最为广泛的协议，具有协议开销小，支持发布订阅等所有模式的优点。它只支持X509证书的认证方式。<br/>

AWS通过AWS IoT SDK提供对mqtt协议的支持。<br/>

<h2 id='TMK9CAcX2bJ'>2.3 mqtt over websocket</h2>

mqtt over websocket是基于websocket上的mqtt协议，也具备mqtt协议的优点，另外它使用了443的端口，在网络环境可达性上比mqtt更有优势，但是也相对更为复杂一些。<br/>

AWS通过AWS IoT SDK提供对mqtt over websocket的支持。<br/>

<h1 id='TMK9CAMH3Zk'>3. AWS IoT支持的认证和授权</h1>

设备接入AWS IoT的时候，必须要进行认证，确认设备的合法身份。通过认证后，还需要对设备的请求进行鉴权，只有经过授权的请求才会被AWS IoT接受。不同的设备认证方式，其授权方式也可能会有所不同。<br/>

<h2 id='TMK9CAWi8xc'>3.1 IAM Identities(user, group, role)</h2>

可以使用IAM提供的身份来认证设备。设备需要预置或者通过其他方式获取security credential，再通过SigV4的签名算法对与IoT交互的请求进行签名。AWS IoT服务通过SigV4的签名算法来认证设备的身份。通过认证后，再根据身份拥有的IAM policy来对请求进行鉴权，流程如下图所示：<br/>

<div data-section-style='11' style='max-width:100%'><img src='https://quip-amazon.com/blob/TMK9AABk0dS/w_3tGqCWdL_XuWere0JeEg?a=69ps7KTjm4rOW5Yp9XIMM2aDW7RI0e7dizQpDpsUMAEa' id='TMK9CASXTCz' alt='' width='800' height='352'></img></div><h2 id='TMK9CAT5mpB'>3.2 Cognito Identities</h2>

使用使用第三方的身份，如google，facebook，OIDC，SAML等，或者用户开发的自定义的身份，然后在Cognito身份池中交换得到Cognito身份，并使用这个身份来认证设备。Cognito身份的鉴权方式比较负责，首先Cognito身份池会为经过认证的身份配置一个role，进而使用role的policy对请求进行鉴权，另外，Cognito身份也会在IoT中绑定一个IoT Policy，这个IoT policy也会对请求进行鉴权。所以说，Cognito身份的最终权限是身份池role的IAM policy与Cognito身份的IoT policy的交集。由于IoT policy支持很多策略变量，通常的建议是，IAM policy可以给一个相对大的权限，然后在IoT policy中实现精细化的权限管理。<br/>

<div data-section-style='11' style='max-width:100%'><img src='https://quip-amazon.com/blob/TMK9AABk0dS/J5lLRQ9sLQa0W4EYNLXT5g?a=ftSudZs6Y3LphiTbBgqtaA4xWzyJajf7l6OKX04jC4wa' id='TMK9CAtRVYw' alt='' width='800' height='438'></img></div><h2 id='TMK9CAsuD9B'>3.3 X509证书</h2>

使用X509证书来认证设备。认证通过后，通过X509证书绑定的IoT policy对请求进行鉴权。<br/>

<div data-section-style='11' style='max-width:100%'><img src='https://quip-amazon.com/blob/TMK9AABk0dS/GQoxicRzFzls6GtkUhZUbA?a=ZVQcTadFjacksUssc9WEuomaZg0NjPf3dfG0u4cPDOMa' id='TMK9CAZwL1G' alt='' width='800' height='411'></img></div><br/>

<h2 id='TMK9CAyv4Om'>3.4 Custom Authentication</h2>

使用自己定义的authorizer来认证设备，实际上是通过编写的lambda逻辑来对设备进行认证。认证通过后，lambda函数返回一个IoT policy，AWS IoT根据这个IoT policy来对请求进行鉴权。<br/>

<div data-section-style='11' style='max-width:100%'><img src='https://quip-amazon.com/blob/TMK9AABk0dS/wKXs3zfF_fqnZyqEpaLr_A?a=4Rvxbb89t5T3JHF6LrIS9V456ep4GFBTFJaxKiippREa' id='TMK9CAPfTGb' alt='' width='800' height='302'></img></div><h1 id='TMK9CAnZ9Yx'>4. 准备工作</h1>

安装配置aws cli，安装jq<br/>

<pre id='TMK9CAFGXRI'>pip install awscli --user<br>pip install jq --user</pre>

下载代码<br/>

<pre id='TMK9CAds2iv'>cd ~<br>git clone https://github.com/zpcl616/awsIoTAccessDemo.git</pre>

进入代码目录<br/>

<pre id='TMK9CALbXnk'>cd awsIoTAccessDemo/src</pre>

下载AWS IoT的Root CA文件<br/>

<pre id='TMK9CAgiAut'>wget <a href="https://www.amazontrust.com/repository/AmazonRootCA1.pem">https://www.amazontrust.com/repository/AmazonRootCA1.pem</a></pre>

依次登陆AWS控制台，打开服务—〉AWS IoT—〉测试—〉订阅主题—〉输入“IoTDemo/#”—〉点击订阅主题。<br/>

Demo过程中设备发送的消息可以在这里看到结果。<br/>

<br/>

获取account id<br/>

<pre id='TMK9CAAD8Id'>account_id=<code>aws sts get-caller-identity | jq .Account|sed 's/"//g'</code></pre>

获取AWS IoT的customer endpoint<br/>

<pre id='TMK9CABaaud'>endpoint_prefix=`aws iot describe-endpoint \<br>| jq .endpointAddress | sed 's/"//g'| awk -F . '{print $1}'`</pre>

<blockquote id='TMK9CAN8GRo'>注意，后续在每个新开的shell窗口都要执行这两步以获取account_id和endpoint_prefix。</blockquote>

<h1 id='TMK9CAFyQYW'>5. 设备接入场景</h1>

<h2 id='TMK9CAWuzRo'>5.1 IAM Identity认证方式</h2>

首先，创建一个IAM user，IoTDeviceUser。<br/>

<pre id='TMK9CAwzHkU'>aws iam create-user --user-name IoTDeviceUser</pre>

为IoTDeviceUser用户创建access key<br/>

<pre id='TMK9CAuluOF'>aws iam create-access-key \<br>    --user-name IoTDeviceUser1 &gt; /tmp/IoT_demo_access_key</pre>

记录下AccessKeyId和SecretAccessKey<br/>

<pre id='TMK9CAcmto9'>AccessKeyId=`cat /tmp/IoT_demo_access_key| jq .AccessKey.AccessKeyId`<br>SecretAccessKey=`cat /tmp/IoT_demo_access_key| jq .AccessKey.SecretAccessKey`</pre>

<h3 id='TMK9CA1MLmQ'>5.1.1 http协议</h3>

为设备创建IAM policy<br/>

<pre id='TMK9CAdQGOX'>device_IAM_http_policy_arn=`aws iam create-policy \<br>--policy-name IoTDeviceIAMHttpPolicy \<br>--policy-document "{<br>    \"Version\": \"2012-10-17\",<br>    \"Statement\": [<br>        {<br>            \"Sid\": \"VisualEditor0\",<br>            \"Effect\": \"Allow\",<br>            \"Action\": \"iot:Publish\",<br>            \"Resource\": [<br>                \"arn:aws-cn:iot:cn-north-1:${account_id}:topic/IoTDemo/device_IAM_http\"<br>            ]<br>        }<br>    ]<br>}" | jq .Policy.Arn`</pre>

把policy绑定IAM user。<br/>

<pre id='TMK9CAeRXdw'>aws iam attach-user-policy --user-name IoTDeviceUser \<br>--policy-arn ${device_IAM_http_policy_arn}</pre>

运行设备模拟程序。<br/>

<pre id='TMK9CAVE6ZL'>python device_IAM_http.py --data "data from device IAM http." \<br>--AccessKeyId ${AccessKeyId} --SecretAccessKey ${SecretAccessKey}</pre>

然后在第4章节打开的控制台中查看收到的消息（后面不再赘述）。<br/>

<h3 id='TMK9CAfegLu'>5.1.2 mqtt over websocket</h3>

为设备创建IAM policy<br/>

<pre id='TMK9CAWEXaa'>device_IAM_websocket_policy_arn=`aws iam create-policy \<br>--policy-name IoTDeviceIAMWebsocketPolicy \<br>--policy-document "{<br>    \"Version\": \"2012-10-17\",<br>    \"Statement\": [<br>        {<br>            \"Sid\": \"VisualEditor0\",<br>            \"Effect\": \"Allow\",<br>            \"Action\": [<br>                \"iot:Publish\",<br>                \"iot:Receive\"<br>            ],<br>            \"Resource\": \"arn:aws-cn:iot:cn-north-1:${account_id}:topic/IoTDemo/device_IAM_websocket\"<br>        },<br>        {<br>            \"Sid\": \"VisualEditor1\",<br>            \"Effect\": \"Allow\",<br>            \"Action\": \"iot:Connect\",<br>            \"Resource\": \"arn:aws-cn:iot:cn-north-1:${account_id}:client/device_IAM_websocket\"<br>        },<br>        {<br>            \"Sid\": \"VisualEditor2\",<br>            \"Effect\": \"Allow\",<br>            \"Action\": \"iot:Subscribe\",<br>            \"Resource\": \"arn:aws-cn:iot:cn-north-1:${account_id}:topicfilter/IoTDemo/device_IAM_websocket\"<br>        }<br>    ]<br>}" | jq .Policy.Arn`</pre>

把policy绑定IAM user。<br/>

<pre id='TMK9CAqVWDX'>aws iam attach-user-policy --user-name IoTDeviceUser \<br>--policy-arn ${device_IAM_websocket_policy_arn}</pre>

运行设备模拟程序<br/>

<pre id='TMK9CA8Tjyd'>python device_IAM_websocket.py --endpoint_prefix ${endpoint_prefix} \<br>--AccessKeyId ${AccessKeyId} --SecretAccessKey ${SecretAccessKey}</pre>

设备模拟程序会一直运行，订阅自己的topic。在控制台输入要发送到AWS IoT的消息，“data from device IAM websocket.”，设备会接收到自己发送的这个消息。同时，在控制台中也可以看到此设备发送的消息。<br/>

<br/>

执行ctrl+C停止程序，或者重新打开一个shell窗口。如果打开新的shell窗口，需要定位到awsIoTAccessDemo/src目录，同时获取变量account_id和endpoint_prefix。<br/>

<pre id='TMK9CAqKydE'>cd ~/awsIoTAccessDemo/src<br>account_id=<code>aws sts </code><code>get</code><code>-</code><code>caller</code><code>-</code><code>identity </code><code>|</code><code> jq </code><code>.</code><code>Account</code><code>|</code><code>sed </code><code>'s/"//g'</code><br>endpoint_prefix=`aws iot describe-endpoint \<br>| jq .endpointAddress | sed 's/"//g'| awk -F . '{print $1}'`</pre>

<h2 id='TMK9CAwHg0z'>5.2 Cognito Identities认证方式</h2>

首先，创建Cognito身份池<br/>

<pre id='TMK9CAartHP'>IdentityPoolId=`aws cognito-identity create-identity-pool \<br>--identity-pool-name IoTDevicesPool \<br>--no-allow-unauthenticated-identities \<br>--developer-provider-name login.IoTDemo.dev`</pre>

<br/>

创建经过认证的Cognito Identity代入的role。<br/>

<pre id='TMK9CA6CIf8'>IoTDeviceRoleInCognitoArn=`aws iam create-role \<br>--role-name IoTDeviceRoleInCognito \<br>--assume-role-policy-document "{<br>  \"Version\": \"2012-10-17\",<br>  \"Statement\": [<br>    {<br>      \"Effect\": \"Allow\",<br>      \"Principal\": {<br>        \"Federated\": \"cognito-identity.amazonaws.com\"<br>      },<br>      \"Action\": \"sts:AssumeRoleWithWebIdentity\",<br>      \"Condition\": {<br>        \"StringEquals\": {<br>          \"cognito-identity.amazonaws.com:aud\": \"${IdentityPoolId}\"<br>        },<br>        \"ForAnyValue:StringLike\": {<br>          \"cognito-identity.amazonaws.com:amr\": \"authenticated\"<br>        }<br>      }<br>    }<br>  ]<br>}" | jq .Role.Arn`</pre>

<br/>

绑定role到cognito身份池<br/>

<pre id='TMK9CAY1xWm'>aws cognito-identity set-identity-pool-roles \<br>--identity-pool-id ${IdentityPoolId} \<br>--roles authenticated=${IoTDeviceRoleInCognitoArn}</pre>

给role绑定可以attach policy的权限<br/>

<blockquote id='TMK9CAwKM5h'>设备在使用cognito身份接入IoT的时候，还需要为其attach一个IoT的policy。 通常情况下，考虑权限的安全，这一步需要在后端的服务来执行，这里为了简化，由设备来为自己attach policy，生产系统中应该禁止使用这种方法。</blockquote>

<pre id='TMK9CAj3rD9'>IoTPolicyManagerArn=`aws iam create-policy \<br>--policy-name IoTPolicyManager \<br>--policy-document "{<br>    \"Version\": \"2012-10-17\",<br>    \"Statement\": [<br>        {<br>            \"Sid\": \"VisualEditor0\",<br>            \"Effect\": \"Allow\",<br>            \"Action\": \"iot:AttachPolicy\",<br>            \"Resource\": \"arn:aws-cn:iot:cn-north-1:${account_id}:policy/*\"<br>        }<br>    ]<br>}" | jq .Policy.Arn`</pre>

把policy attach到role<br/>

<pre id='TMK9CAKergr'>aws iam attach-role-policy --role-name IoTDeviceRoleInCognito \<br>--policy-arn ${IoTPolicyManagerArn}</pre>

Cognito身份池支持多种身份认证的方式，这里使用了developer provider来获取身份并交换Cognito身份。<br/>

创建一个IAM user，developerIdpUser，用来获取developer provider的权限<br/>

<pre id='TMK9CAyshPR'>aws iam create-user --user-name developerIdpUser</pre>

创建策略，并把策略attach到developerIdpUser<br/>

<pre id='TMK9CAmErqt'>developerIdpPolicy_arn=`aws iam create-policy \<br>--policy-name developerIdpPolicy \<br>--policy-document "{<br>    \"Version\": \"2012-10-17\",<br>    \"Statement\": [<br>        {<br>        \"Sid\": \"VisualEditor0\",<br>        \"Effect\": \"Allow\",<br>        \"Action\": \"cognito-identity:GetOpenIdTokenForDeveloperIdentity\",<br>        \"Resource\": \"arn:aws-cn:cognito-identity:cn-north-1:${account_id}:identitypool/${IdentityPoolId}\"<br>        }<br>    ]<br>}" | jq .Policy.Arn`</pre>

<pre id='TMK9CA0CIRL'>aws iam attach-user-policy --user-name developerIdpUser \<br>--policy-arn ${developerIdpPolicy_arn}</pre>

为developerIdpUser用户创建access key<br/>

<pre id='TMK9CA02V11'>aws iam create-access-key \<br>    --user-name developerIdpUser &gt; /tmp/IoT_demo_access_key2</pre>

记录下AccessKeyId和SecretAccessKey<br/>

<pre id='TMK9CAmdXnT'>AccessKeyId=`cat /tmp/IoT_demo_access_key2 | jq .AccessKey.AccessKeyId`<br>SecretAccessKey=`cat /tmp/IoT_demo_access_key2 | jq .AccessKey.SecretAccessKey`</pre>

运行developer_provider.py<br/>

<pre id='TMK9CA8Vj3u'>python developer_provider.py --identityPoolId ${IdentityPoolId} \<br>--AccessKeyId ${AccessKeyId} --SecretAccessKey ${SecretAccessKey}</pre>

developer_provider.py会在在<a href="http://0.0.0.0:8383/">http://0.0.0.0:8383/</a> 接受请求，并返回Cognito身份池的身份信息。<br/>

<h3 id='TMK9CAVX7wU'>5.2.1 http协议</h3>

打开一个新的shell窗口，定位到awsIoTAccessDemo/src目录，同时获取变量account_id和endpoint_prefix。<br/>

<pre id='TMK9CAAnmCC'>cd ~/awsIoTAccessDemo/src<br>account_id=<code>aws sts </code><code>get</code><code>-</code><code>caller</code><code>-</code><code>identity </code><code>|</code><code> jq </code><code>.</code><code>Account</code><code>|</code><code>sed </code><code>'s/"//g'</code><br>endpoint_prefix=`aws iot describe-endpoint \<br>| jq .endpointAddress | sed 's/"//g'| awk -F . '{print $1}'`</pre>

通过Cognito方式认证的设备，需要IAM policy和IoT policy同时授权。<br/>

为设备创建IAM policy，并将其attach到Cognito role<br/>

<pre id='TMK9CAmorDx'>IoTDeviceCognitoHttpPolicyArn=`aws iam create-policy \<br>--policy-name IoTDeviceCognitoHttpPolicy \<br>--policy-document "{<br>    \"Version\": \"2012-10-17\",<br>    \"Statement\": [<br>        {<br>            \"Sid\": \"VisualEditor0\",<br>            \"Effect\": \"Allow\",<br>            \"Action\": \"iot:Publish\",<br>            \"Resource\": [<br>                \"arn:aws-cn:iot:cn-north-1:${account id}:topic/IoTDemo/device_cognito_http\"<br>            ]<br>        }<br>    ]<br>}" | jq .Policy.Arn`</pre>

<pre id='TMK9CA9wj3c'>aws iam attach-role-policy --role-name IoTDeviceRoleInCognito \<br>--policy-arn ${IoTDeviceCognitoHttpPolicyArn}</pre>

创建IoT policy<br/>

<pre id='TMK9CAValus'>aws iot create-policy --policy-name IoTPolicyForDeviceCognitohttp \<br> --policy-document "{<br>    \"Version\": \"2012-10-17\",<br>    \"Statement\": [<br>        {<br>        \"Effect\": \"Allow\",<br>        \"Action\": \"iot:Publish\",<br>        \"Resource\": [<br>                \"arn:aws-cn:iot:cn-north-1:${account_id}:topic/IoTDemo/device_cognito_http\"<br>            ]<br>        }<br>    ]<br>}"</pre>

运行设备模拟程序发送消息。<br/>

<pre id='TMK9CAsPU4R'>python device_cognito_http.py --data "data from device cognito http." \<br>--developer_provicer_endpoint "http://127.0.0.1:8383/login/" \<br>--iot_policy_name IoTPolicyForDeviceCognitohttp</pre>

在控制台查看接受到的消息。<br/>

<h3 id='TMK9CA2tSV2'>5.2.2 mqtt over websocket协议</h3>

为设备创建IAM policy，并将其attach到Cognito role<br/>

<pre id='TMK9CAapFZ4'>IoTDeviceCognitoWebsocketPolicyArn=`aws iam create-policy \<br>--policy-name IoTDeviceCognitoWebsocketPolicy \<br>--policy-document "{<br>    \"Version\": \"2012-10-17\",<br>    \"Statement\": [<br>        {<br>            \"Sid\": \"VisualEditor0\",<br>            \"Effect\": \"Allow\",<br>            \"Action\": [<br>                \"iot:Publish\",<br>                \"iot:Receive\"<br>            ],<br>            \"Resource\": \"arn:aws-cn:iot:cn-north-1:${account_id}:topic/IoTDemo/device_cognito_websocket\"<br>        },<br>        {<br>            \"Sid\": \"VisualEditor1\",<br>            \"Effect\": \"Allow\",<br>            \"Action\": \"iot:Connect\",<br>            \"Resource\": \"arn:aws-cn:iot:cn-north-1:${account_id}:client/device_cognito_websocket\"<br>        },<br>        {<br>            \"Sid\": \"VisualEditor2\",<br>            \"Effect\": \"Allow\",<br>            \"Action\": \"iot:Subscribe\",<br>            \"Resource\": \"arn:aws-cn:iot:cn-north-1:${account_id}:topicfilter/IoTDemo/device_cognito_websocket\"<br>        }<br>    ]<br>} | jq .Policy.Arn`</pre>

<pre id='TMK9CAbqJGv'>aws iam attach-role-policy --role-name IoTDeviceRoleInCognito \<br>--policy-arn ${IoTDeviceCognitoWebsocketPolicyArn}</pre>

创建IoT policy<br/>

<pre id='TMK9CAd4Kdd'>aws iot create-policy --policy-name IoTPolicyForDeviceCognitoWebsocket \<br>--policy-document "{<br>\"Version\": \"2012-10-17\",<br>    \"Statement\": [<br>        {<br>            \"Sid\": \"VisualEditor0\",<br>            \"Effect\": \"Allow\",<br>            \"Action\": [<br>                \"iot:Publish\",<br>                \"iot:Receive\"<br>            ],<br>            \"Resource\": \"arn:aws-cn:iot:cn-north-1:${account_id}:topic/IoTDemo/device_cognito_websocket\"<br>        },<br>        {<br>            \"Sid\": \"VisualEditor1\",<br>            \"Effect\": \"Allow\",<br>            \"Action\": \"iot:Connect\",<br>            \"Resource\": \"arn:aws-cn:iot:cn-north-1:${account_id}:client/device_cognito_websocket\"<br>        },<br>        {<br>            \"Sid\": \"VisualEditor2\",<br>            \"Effect\": \"Allow\",<br>            \"Action\": \"iot:Subscribe\",<br>            \"Resource\": \"arn:aws-cn:iot:cn-north-1:${account_id}:topicfilter/IoTDemo/device_cognito_websocket\"<br>        }<br>    ]<br>} </pre>

运行设备模拟程序<br/>

<pre id='TMK9CAVHNGt'>python device_cognito_websocket.py \<br>--developer_provicer_endpoint "http://127.0.0.1:8383/login/" \<br>--iot_policy_name IoTPolicyForDeviceCognitoWebsocket \<br>--endpoint_prefix ${endpoint_prefix}</pre>

设备模拟程序会一直运行，订阅自己的topic。在控制台输入要发送到AWS IoT的消息，“data from device Cognito websocket.”，设备会接收到自己发送的这个消息。同时，在控制台中也可以看到此设备发送的消息。<br/>

<br/>

执行ctrl+C停止程序，或者重新打开一个shell窗口。如果打开新的shell窗口，需要定位到awsIoTAccessDemo/src目录，同时获取变量account_id和endpoint_prefix。<br/>

<pre id='TMK9CArgbfC'>cd ~/awsIoTAccessDemo/src<br>account_id=<code>aws sts </code><code>get</code><code>-</code><code>caller</code><code>-</code><code>identity </code><code>|</code><code> jq </code><code>.</code><code>Account</code><code>|</code><code>sed </code><code>'s/"//g'</code><br>endpoint_prefix=`aws iot describe-endpoint \<br>| jq .endpointAddress | sed 's/"//g'| awk -F . '{print $1}'`</pre>

<h2 id='TMK9CAu4C39'>5.3 X.509证书认证方式</h2>

<h3 id='TMK9CAgmv2x'>5.3.1 http协议</h3>

为设备创建证书<br/>

<pre id='TMK9CArU1HD'>device_x509_http_crt_arn=`aws iot create-keys-and-certificate \<br>--set-as-active --certificate-pem-outfile device_x509_http.crt \<br>--public-key-outfile device_x509_http.pem --private-key-outfile device_x509_http.key \<br>| jq .certificateArn`</pre>

为设备创建IoT policy<br/>

<pre id='TMK9CAgEqT5'>aws iot create-policy --policy name IoTPolicyForDeviceX509Http \<br>--policy-document "{<br>  \"Version\": \"2012-10-17\",<br>  \"Statement\": [<br>    {<br>      \"Effect\": \"Allow\",<br>      \"Action\": \"iot:Publish\",<br>      \"Resource\": [<br>        \"arn:aws-cn:iot:cn-north-1:${account_id}:topic/IoTDemo/device_x509_http\"<br>      ]<br>    }<br>  ]<br>}"</pre>

把IoT policy attach到设备证书<br/>

<pre id='TMK9CAmcSAk'>aws iot attach-policy --policy-name IoTPolicyForDeviceX509Http \<br>--target ${device_x509_http_crt_arn}</pre>

运行设备模拟程序<br/>

<pre id='TMK9CAL4eSW'>python device_x509_http.py --data "data from device x509 http."\<br>--endpoint_prefix ${endpoint_prefix} \<br>--client_cert ./device_x509_http.crt \<br>--client_key ./device_x509_http.key</pre>

在控制台上查看收到的消息。<br/>

<h3 id='TMK9CAwCjMb'>5.3.2 mqtt协议</h3>

为设备创建证书<br/>

<pre id='TMK9CARygoU'>device_x509_mqtt_crt_arn=`aws iot create-keys-and-certificate \<br>--set-as-active --certificate-pem-outfile device_x509_mqtt.crt \<br>--public-key-outfile device_x509_mqtt.pem --private-key-outfile device_x509_mqtt.key \<br>| jq .certificateArn`</pre>

为设备创建IoT policy<br/>

<pre id='TMK9CAR6GBc'>aws iot create-policy --policy name IoTPolicyForDeviceX509Mqtt \<br>--policy-document "{<br>  \"Version\": \"2012-10-17\",<br>    \"Statement\": [<br>        {<br>            \"Sid\": \"VisualEditor0\",<br>            \"Effect\": \"Allow\",<br>            \"Action\": [<br>                \"iot:Publish\",<br>                \"iot:Receive\"<br>            ],<br>            \"Resource\": \"arn:aws-cn:iot:cn-north-1:${account_id}:topic/IoTDemo/device_x509_mqtt\"<br>        },<br>        {<br>            \"Sid\": \"VisualEditor1\",<br>            \"Effect\": \"Allow\",<br>            \"Action\": \"iot:Connect\",<br>            \"Resource\": \"arn:aws-cn:iot:cn-north-1:${account_id}:client/device_x509_mqtt\"<br>        },<br>        {<br>            \"Sid\": \"VisualEditor2\",<br>            \"Effect\": \"Allow\",<br>            \"Action\": \"iot:Subscribe\",<br>            \"Resource\": \"arn:aws-cn:iot:cn-north-1:${account_id}:topicfilter/IoTDemo/device_x509_mqtt\"<br>        }<br>    ]<br>} </pre>

把IoT policy attach到设备证书<br/>

<pre id='TMK9CATw7FL'>aws iot attach-policy --policy-name IoTPolicyForDeviceX509Mqtt \<br>--target ${device_x509_mqtt_crt_arn}</pre>

运行设备模拟程序<br/>

<pre id='TMK9CAmHfOS'>python device_x509_mqtt.py \<br>--endpoint_prefix ${endpoint_prefix} \<br>--client_cert ./device_x509_mqtt.crt \<br>--client_key ./device_x509_mqtt.key</pre>

设备模拟程序会一直运行，订阅自己的topic。在控制台输入要发送到AWS IoT的消息，“data from device x509 mqtt.”，设备会接收到自己发送的这个消息。同时，在控制台中也可以看到此设备发送的消息。<br/>

<br/>

执行ctrl+C停止程序，或者重新打开一个shell窗口。如果打开新的shell窗口，需要定位到awsIoTAccessDemo/src目录，同时获取变量account_id和endpoint_prefix。<br/>

<pre id='TMK9CAE3ee6'>cd ~/awsIoTAccessDemo/src<br>account_id=<code>aws sts </code><code>get</code><code>-</code><code>caller</code><code>-</code><code>identity </code><code>|</code><code> jq </code><code>.</code><code>Account</code><code>|</code><code>sed </code><code>'s/"//g'</code><br>endpoint_prefix=`aws iot describe-endpoint \<br>| jq .endpointAddress | sed 's/"//g'| awk -F . '{print $1}'`</pre>

<h2 id='TMK9CAtVkWJ'>5.4 Custom Authentication</h2>

Custom Authentication是由lambda函数来认证授权，所以先要创建lambda。<br/>

创建lambda要代入的role<br/>

<pre id='TMK9CAkiCqs'>IoTDemoAuthorizerFunctionRoleArn=`aws iam create-role \<br>--role-name IoTDemoAuthorizerFunctionRole \<br>--assume-role-policy-document "{<br>  \"Version\": \"2012-10-17\",<br>  \"Statement\": [<br>    {<br>      \"Effect\": \"Allow\",<br>      \"Principal\": {<br>        \"Service\": \"lambda.amazonaws.com\"<br>      },<br>      \"Action\": \"sts:AssumeRole\"<br>    }<br>  ]<br>}" | jq .Role.Arn | sed 's/"//g'`</pre>

为lambda角色attach一个policy <br/>

<pre id='TMK9CAouVXB'>aws iam attach-role-policy --role-name IoTDemoAuthorizerFunctionRole \<br>--policy-arn arn:aws-cn:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole</pre>

创建lambda函数<br/>

<pre id='TMK9CA8HVPx'>zip function.zip  IoTDemoAuthorizerFunction.py<br><code>IoTDemoAuthorizerFunctionArn</code><code>=</code><code>`aws </code><code>lambda</code><code> create</code><code>-</code><code>function</code><code> </code><code>\</code><br><code>--</code><code>function</code><code>-</code><code>name </code><code>IoTDemoAuthorizerFunction</code><code> \</code><br><code>--</code><code>zip</code><code>-</code><code>file fileb</code><code>:</code><code>//function.zip --handler IoTDemoAuthorizerFunction.lambda_handler \</code><br><code>--</code><code>runtime python2.7</code><code> </code><code>--</code><code>role $</code><code>{</code><code>IoTDemoAuthorizerFunctionRoleArn</code><code>}</code><code> </code><code>\</code><br><code>| jq </code><code>.FunctionArn | sed 's/"//g'`</code><code> </code></pre>

创建authorizer用于验证token的密钥对<br/>

<pre id='TMK9CAkx8NR'><code>openssl genrsa </code><code>-</code><code>out</code><code> </code><code>authorizer</code><code>_private</code><code>.</code><code>pem </code><code>2048</code><br><code>openssl rsa </code><code>-</code><code>in</code><code> authorizer_private</code><code>.</code><code>pem </code><code>-</code><code>outform PEM </code><code>-</code><code>pubout </code><code>-</code><code>out</code><code> authorizer_public</code><code>.</code><code>pem</code></pre>

创建authorizer<br/>

<pre id='TMK9CAyOKJv'><code>authorizerArn=`aws iot create</code><code>-</code><code>authorizer </code><code>\<br>-</code><code>-</code><code>authorizer</code><code>-</code><code>name </code><code>IoTDemoAuthorizer</code><code> </code><code>\</code><br><code>--</code><code>authorizer</code><code>-</code><code>function</code><code>-</code><code>arn $</code><code>{</code><code>IoTDemoAuthorizerFunction</code><code>Arn}</code><code> </code><code>\</code><br><code>--</code><code>token</code><code>-</code><code>key</code><code>-</code><code>name </code><code>IoTDemoAuthorizerToken</code><code> </code><code>\</code><br><code>--</code><code>token</code><code>-</code><code>signing</code><code>-</code><code>public</code><code>-</code><code>keys FIRST_KEY</code><code>=</code><code>"\`cat authorizer_public.pem\`</code><code>" </code><code>\</code><br><code>--</code><code>status ACTIVE</code><code> </code><code>|</code><code> jq </code><code>.</code><code>authorizerArn | sed 's/"//g'`</code></pre>

为authorizer配置调用lambda的权限<br/>

<pre id='TMK9CArUYJN'>aws lambda add-permission --function-name IoTDemoAuthorizerFunction \<br>--statement-id IoTDemoAuthorizerFunctionPermission \<br>--action 'lambda:InvokeFunction' \<br>--principal iot.amazonaws.com \<br>--source-arn <code>$</code><code>{authorizerArn</code><code>}</code></pre>

<h3 id='TMK9CAGVMK2'>5.4.1 http协议</h3>

运行设备模拟程序<br/>

<blockquote id='TMK9CAnUR7n'>需要注意的是目前实际测试custom authentication认证授权方式下，不支持ATS endpoint，代码中需注意。另外custom authentication也暂时没有python SDK的支持，需要自己编写代码。</blockquote>

<pre id='TMK9CAGIwQD'>python device_custom_auth_http.py \<br>--data "data from device custom authentication http." \<br>--authorizer_name <code>IoTDemoAuthorizer \</code><br>--endpoint_prefix ${endpoint_prefix} \<br>--private_key <code>authorizer_private</code><code>.</code><code>pem</code></pre>

在控制台上查看收到的消息。<br/>

<h3 id='TMK9CAhZfkU'>5.4.2 mqtt over websocket协议</h3>

由于Custom Authentication不支持ATS endpoint，需要下载VeriSign endpoint的证书。<br/>

<pre id='TMK9CAlYoxw'>wget <a href="https://www.symantec.com/content/en/us/enterprise/verisign/roots/VeriSign-Class%203-Public-Primary-Certification-Authority-G5.pem">https://www.symantec.com/content/en/us/enterprise/verisign/roots/VeriSign-Class%203-Public-Primary-Certification-Authority-G5.pem</a></pre>

运行设备模拟程序<br/>

<pre id='TMK9CAt8HYC'>python device_custom_auth_websocket.py \<br>--endpoint_prefix ${endpoint_prefix} \<br>--authorizer_name <code>IoTDemoAuthorizer</code><code><br>--private_key authorizer_private.pem</code></pre>

</body></html>
