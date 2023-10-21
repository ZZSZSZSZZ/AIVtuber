import json
import requests  # HTTP 请求库
from typing import Iterable, List


openapi_url = "https://u245099-8c76-975ff0f0.westb.seetacloud.com:8443/generate"
openapi_session_id = 0
openapi_request_output_len = 512


class openapi:
    def get_streaming_response(self,
                               prompt: str,
                               api_url: str,
                               session_id: int,
                               request_output_len: int,
                               stream: bool = True,
                               sequence_start: bool = True,
                               sequence_end: bool = True,
                               ignore_eos: bool = False) -> Iterable[List[str]]:
        headers = {'User-Agent': 'Test Client'}
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
                yield output, tokens

    def test(self, prompt: str):
        for output, tokens in self.get_streaming_response(prompt, openapi_url, openapi_session_id, openapi_request_output_len):
            yield output