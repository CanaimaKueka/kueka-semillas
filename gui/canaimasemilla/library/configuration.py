#!/usr/bin/python
#-*- coding: UTF-8 -*-


def ConfigSectionMap(Config, section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
        except:
            dict1[option] = None
    return dict1
