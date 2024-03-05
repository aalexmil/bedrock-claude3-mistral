import boto3
import json

# Assume Role
sts_client = boto3.client("sts")
response = sts_client.assume_role(
    RoleArn="arn:aws:iam::123456789012:role/Cross-Account-Role",
    RoleSessionName="find-me-in-CloudTrail" # This shows up as username in CloudTrail
)

# Create Boto3 session and client
session = boto3.Session(
    aws_access_key_id     = response['Credentials']['AccessKeyId'],
    aws_secret_access_key = response['Credentials']['SecretAccessKey'],
    aws_session_token     = response['Credentials']['SessionToken']
)

boto3_bedrock_client = session.client(service_name='bedrock-runtime', region_name="us-west-2")


prompt_data = "Write a Python program that calculates the first 93 prime numbers."

################################################################
# Mistral Mixtral 8x7b
modelId = 'mistral.mixtral-8x7b-instruct-v0:1'
accept = 'application/json'
contentType = 'application/json'

# Invoke model
response = boto3_bedrock_client.invoke_model(
    body=json.dumps({
        "prompt"      : prompt_data,
        "max_tokens"  : 2000,
        "temperature" : 0.5,
    }),
    modelId     = modelId,
    accept      = accept,
    contentType = contentType
)

response_body = json.loads(response.get('body').read())
print(response_body.get("outputs")[0]['text'])
################################################################

################################################################
# Mistral Mixtral 7b
modelId     = 'mistral.mistral-7b-instruct-v0:2'
accept      = 'application/json'
contentType = 'application/json'

body = json.dumps({
     "prompt"      : prompt_data,
     "max_tokens"  : 2000,
     "temperature" : 0.5,
    })


response = boto3_bedrock_client.invoke_model(
     body        = body,
     modelId     = modelId,
     accept      = accept,
     contentType = contentType
    )

response_body = json.loads(response.get('body').read())

print(response_body.get("outputs")[0]['text'])
################################################################

################################################################
#Claude v3 Sonnet

modelId     = 'anthropic.claude-3-sonnet-20240229-v1:0'
accept      = 'application/json'
contentType = 'application/json'

body = json.dumps({
    "messages": [{
        "role": "user",
        "content": [{
            "type": "text",
            "text": prompt_data
        }]
    }],
    "anthropic_version": "bedrock-2023-05-31",
    "max_tokens": 2000
})

response = boto3_bedrock_client.invoke_model(
     body        = body,
     modelId     = modelId,
     accept      = accept,
     contentType = contentType
    )

response_body = json.loads(response.get('body').read())
print(response_body['content'][0]['text'])
################################################################
