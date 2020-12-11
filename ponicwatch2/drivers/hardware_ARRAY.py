#!/usr/bin/python3
"""
Hardware driver to provide a RAM bank to store values and access them.

The data persistence is ensured by saving the array in the init_dict of that 'hardware'.

Sensor can be used to read data our if this 'hardware' while switches can write entries.

* pin: name of the memory entry (key)
* value: stored information (value)

"""
import json
class Hardware_Array(object):

    def __init__(self, pig, init_dict, db_rec, debug=None):
        """
        Initiate the data internal dictionary
        :param pig: ignored as this is not a real hardware needing I/O
        :param init_dict: data persistence
        """
        self.data = init_dict
        self.debug = debug
        self.db_rec = db_rec

    def read(self, pin, param=None):
        return pin, self.data.get(pin)

    def write(self, pin, value):
        self.data[pin] = value
        self.db_rec.update(init=json.dumps(self.data))

    def set_pin_as_input(self, pin):
        if pin not in self.data:
            self.data[pin] = None

    def set_pin_as_output(self, pin):
        if pin not in self.data:
            self.data[pin] = None

    def cleanup(self):
        self.db_rec.update(init=json.dumps(self.data))

    @property
    def value(self):
        return json.dumps(self.data)
