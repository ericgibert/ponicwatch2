"""
 Simple configuration file for the application using JSON format
 - API keys for Beebotte
 - list of the systems to control
"""
from json import dump, load
from dataclasses import dataclass

@dataclass
class Config():

    def __init__(self, filename):
        self.filename = filename
        try:
            with open(filename, "rt") as json_file:
                self.data = load(json_file)
        except FileNotFoundError:
            self.data = {}

    def save(self):
            with open(self.filename, 'wt') as json_file:
                dump(self.data, json_file, indent=4)

    def __getitem__(self, item):
        return self.data.get(item)

    def __getattr__(self, key):
        try:
            return self.data.get(key)
        except KeyError:
            raise AttributeError(key)


if __name__ == '__main__':
    cfg = Config("../Private/config.txt")
    # cfg.data["API_KEY"] = "api_key"
    # cfg.data["SECRET_KEY"] = "secret_key"
    # cfg.data["toto"] = ['a','b']
    cfg.save()
    print(cfg.data["API_KEY"])
    print(cfg["SECRET_KEY"])
    print(cfg.SECRET_KEY)
    print(cfg.rabbitmq["location"])
