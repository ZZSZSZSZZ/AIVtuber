from models.openapi import openapi

openapi = openapi()

for message in openapi.test("Hi, how are you?"):
    print(message, end='')
