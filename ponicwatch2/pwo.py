"""
Ponicwatch Object Class
- Abstraction over hardware for sensors, switches, triggers...
"""

class PWO():

    def __init__(self, cfg: dict, id: int):
        """
        Takes the object from the Config file
        :param cfg:
        :param id:
        """
        self.data = cfg.SYSTEM[str(id)]
        self.id = id

    def __getattr__(self, key):
        try:
            return self.data.get(key)
        except KeyError:
            if key == "id":
                return self.id
            raise AttributeError(key)

    def readValue(self):
        """
        Reads a value from the hardware
        Calculate the matching calculatedValue
        Log the values
        :return:
        """
        self.value = 3 #self.hardware.read(self.params)
        self.calculatedValue = eval((self.formula or "V").replace("V", str(self.value)))
        self.log()

    def log(self):
        """
        Log values after reading
        :return:
        """
        print("Values to log:", self.value, "-->", self.calculatedValue)

if __name__ == '__main__':
    from config import Config
    cfg = Config("../Private/config.txt")
    pwo = PWO(cfg, 1)
    print("id", pwo.id, ":", pwo.name)
    print("Unknown attribute:", pwo.undefined)
    pwo.readValue()
