import json
import requests
from tools import Config


class OpenAI:
    # 获取配置文件
    config = Config().load_config('config.yml')['model']['openai']

    def get_message(self, content: str):
        """
        用于获取LLM消息
        :param content: 问题
        :rtype: object
        """
        url = self.config['chat_url']
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.config['key']
        }
        data = {
            "max_tokens": self.config['chat_max_tokens'],
            "model": self.config['chat_model'],
            "temperature": self.config['chat_temperature'],
            "top_p": self.config['chat_top_p'],
            "presence_penalty": self.config['chat_presence_penalty'],
            "frequency_penalty": self.config['chat_frequency_penalty'],
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
        """
        用于转换文本到词向量
        :param content: 需要转换的文本
        :rtype: object
        """
        url = self.config['embeddings_url']
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.config['key']
        }
        data = {
            "input": content,
            "model": self.config['embeddings_model']
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
