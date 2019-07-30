// A simple authorizer Lambda function demonstrating
// how to parse auth token and generate response

exports.handler = function(event, context, callback) {
    console.log("%s", event.token)
    var token = JSON.parse(event.token);
    callback(null, generateAuthResponse(token));
};

// Helper function to generate authorization response
var generateAuthResponse = function(token) {
    // Invoke your preferred identity provider
    // to get the authN and authZ response.
    // Following is just for simplicity sake

    var authResponse = {};

    var identityId = token['identityId'];
    var device_id = token['device_id'];

    authResponse.isAuthenticated = true;
    authResponse.principalId = identityId;

    var policyDocument = {};
    policyDocument.Version = '2012-10-17';
    policyDocument.Statement = [];


    var statement0 = {};
    statement0.Action = 'iot:Publish';
    statement0.Effect = 'Allow';
    statement0.Resource = "arn:aws-cn:iot:cn-north-1:*:topic/IoTDemo/"+device_id;
    policyDocument.Statement[0] = statement0;

    var statement1 = {};
    statement1.Action = 'iot:Subscribe';
    statement1.Effect = 'Allow';
    statement1.Resource = "arn:aws-cn:iot:cn-north-1:*:topicfilter/IoTDemo/"+device_id;
    policyDocument.Statement[1] = statement1;

    authResponse.policyDocuments = [policyDocument];
    authResponse.disconnectAfterInSeconds = 3600;
    authResponse.refreshAfterInSeconds = 600;

    return authResponse;
}
