#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Created by Eric Gibert on 12 May 2016

    Controller in MVC model
    - main point of execution

"""
from config import Config

__version__ = "2.20201207 Nicole"
__author__ = 'Eric Gibert'
__license__ = 'MIT'

class Controler():

    def __init__(self, cfg_filename:str):
        self.cfg = Config(cfg_filename)
        self.find_hdwr(self.cfg.SYSTEM["Hardware"])


    def find_hdwr(self, hdwr: dict):
        """
        Create each hardware object from the Config
        :param hdwr:
        :return:
        """
        self.hardware = []
        for hk, hv in hdwr.items():
            print(hk, hv)

    def start(self):
        pass

if __name__ == '__main__':
    ctrl = Controler("../Private/config.txt")
    ctrl.start()