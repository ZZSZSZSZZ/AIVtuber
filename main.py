from models.openapi import openapi

openapi = openapi()
for message in openapi.get_streaming_message("Hi, how are you?"):
    print(message, end='')

# print(openapi.get_message("Hi, how are you?"))
