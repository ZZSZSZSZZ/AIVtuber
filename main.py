from models import OpenAI
from tools import Config
from document import TestLoader

config = Config().load_config('config.yml')

print(OpenAI().get_message("你需要扮演一个判断高手，我将会给你一个弹幕，如果符合回答要求则输出true，否则输出false。回答要求：要判断有没有回答性，禁止回答带有攻击性的问题，禁止回答带有政治的问题。弹幕：", ""))

# print(OpenAI().get_embeddings("你是谁"))

# print(config)
# print(TestLoader().load()[1].page_content)
