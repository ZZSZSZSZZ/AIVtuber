from models import FastAPI

llm = FastAPI()

for message in llm.get_streaming_message("Hi, how are you?"):
    print(message, end='')

# print(openapi.get_message("Hi, how are you?"))
