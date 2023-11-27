import json
import requests
from tools import Config


class OpenAI:
    config = Config()
    config.load_config('config.yml')
    config = config.get_json()['openai']

    def get_message(self, content: str, model: str = "gpt-3.5-turbo-1106", temperature: float = 0.4, top_p: float = 0.8,
                    presence_penalty: float = 2, frequency_penalty: float = 1):
        url = self.config['openai_chat_url']
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.config['openai_key']
        }
        data = {
            "max_tokens": 1200,
            "model": model,
            "temperature": temperature,
            "top_p": top_p,
            "presence_penalty": presence_penalty,
            "frequency_penalty": frequency_penalty,
            "messages": [
                {
                    "role": "system",
                    "content": "我希望你扮演一只猫娘Vtuber，现在正在直播，请用一名主播的口吻回答我的问题，每次回话最好不要超过20个字，不要反问，你的名字：6点半。性别：女。性格：非常可爱，俏皮，活泼。知识掌握程度：大学毕业。人物特点：长有毛茸茸的猫耳朵和一个猫尾巴(这是生理自带)，喜欢在一句话的结尾加上喵～。"
                },
                {
                    "role": "user",
                    "content": content
                }
            ]
        }

        response = requests.post(url, headers=headers, data=json.dumps(data).encode('utf-8'))
        result = response.content.decode("utf-8")
        content = json.loads(result)['choices'][0]['message']['content']
        return content

    def get_embeddings(self, content: str):
        url = self.config['openai_embeddings_url']
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.config['openai_key']
        }
        data = {
            "input": content,
            "model": "text-embedding-ada-002"
        }

        response = requests.post(url, headers=headers, data=json.dumps(data).encode('utf-8'))
        result = response.content.decode("utf-8")
        embedding = json.loads(result)['data'][0]['embedding']
        return embedding

    @staticmethod
    def get_moderations(content: str):
        url = "https://api.openai-hk.com/v1/moderations"
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer hk-5lyjq81000006178a2f895dbc6f126d0912d82a3707433a8"
        }
        data = {
            "input": content
        }

        response = requests.post(url, headers=headers, data=json.dumps(data).encode('utf-8'))
        result = response.content.decode("utf-8")
        return result
