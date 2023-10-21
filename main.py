from models.openapi import openapi


url = "https://u245099-8c76-975ff0f0.westb.seetacloud.com:8443/generate"

openapi = openapi()

for output, tokens in openapi.get_streaming_response("Hi, how are you?", url, 0, 512):
    print(output, end='')