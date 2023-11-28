import yaml


class Config:
    json = None  # json格式的配置文件

    def load_config(self, yaml_file=None):
        """
        用于加载配置文件
        :param yaml_file: yaml文件路径
        :return: json格式的配置文件
        """
        if yaml_file is None:
            print("Config文件未指定:(")
        try:
            file = open(yaml_file, 'r', encoding='utf-8')
            self.json = yaml.load(file, Loader=yaml.FullLoader)
        except IOError as e:
            print(e)
        finally:
            if file is not None:
                file.close()
        return self.json
