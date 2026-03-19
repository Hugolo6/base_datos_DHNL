import json
import os

class M5config:
    def __init__(self):
        #self.filename = "/mnt/c/py/m5bot/libs/config.json"
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.filename = os.path.join(base_dir, "config.json")
    #obtener la configuracion del json mediante un key
    def get(self,section,):
        with open(self.filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data[section]

