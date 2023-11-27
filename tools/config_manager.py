import yaml


class Config:
    json = None

    def load_config(self, yamlfile=None):
        if yamlfile is None:
            print("Config文件未指定:(")
        try:
            file = open(yamlfile, 'r', encoding='utf-8')
            self.json = yaml.load(file, Loader=yaml.FullLoader)
        except IOError as e:
            print(e)
        finally:
            if file is not None:
                file.close()

    def get_json(self):
        return self.json
