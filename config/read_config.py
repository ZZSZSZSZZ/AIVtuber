import yaml


class ReadConfig:
    def __init__(self, yaml_path):
        self.yaml_path = yaml_path

    def read(self):
        with open(self.yaml_path, encoding="utf-8") as F:
            res = yaml.load(stream=F.read(), Loader=yaml.FullLoader)
            return res.text

