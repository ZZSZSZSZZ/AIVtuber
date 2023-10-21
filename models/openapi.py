import json
import requests  # HTTP 请求库
from typing import Iterable, List

openapi_url = "https://u245099-b439-7fe6db8e.westb.seetacloud.com:8443/generate"
openapi_session_id = 0
openapi_request_output_len = 512


class openapi:

    @staticmethod
    # 流式请求消息
    def get_streaming_response(prompt: str,
                               api_url: str = openapi_url,
                               session_id: int = openapi_session_id,
                               request_output_len: int = openapi_request_output_len,
                               stream: bool = True,
                               sequence_start: bool = True,
                               sequence_end: bool = True,
                               ignore_eos: bool = False) -> Iterable[List[str]]:
        headers = {'User-Agent': 'Client'}
        data = {
            'prompt': prompt,
            'stream': stream,
            'session_id': session_id,
            'request_output_len': request_output_len,
            'sequence_start': sequence_start,
            'sequence_end': sequence_end,
            'ignore_eos': ignore_eos
        }
        response = requests.post(api_url, headers=headers, json=data, stream=stream)

        for chunk in response.iter_lines(chunk_size=8192, decode_unicode=False, delimiter=b'\n'):
            if chunk:
                data = json.loads(chunk.decode('utf-8'))
                output = data['text']
                tokens = data['tokens']
                yield output

    @staticmethod
    # 请求消息
    def get_message(prompt: str,
                    api_url: str = openapi_url,
                    session_id: int = openapi_session_id,
                    request_output_len: int = openapi_request_output_len,
                    stream: bool = False,
                    sequence_start: bool = True,
                    sequence_end: bool = True,
                    ignore_eos: bool = False) -> Iterable[List[str]]:
        headers = {'User-Agent': 'Client'}
        data = {
            'prompt': prompt,
            'stream': stream,
            'session_id': session_id,
            'request_output_len': request_output_len,
            'sequence_start': sequence_start,
            'sequence_end': sequence_end,
            'ignore_eos': ignore_eos
        }
        response = requests.post(api_url, headers=headers, json=data, stream=stream)
        response = json.loads(response.text)
        return response['text']

