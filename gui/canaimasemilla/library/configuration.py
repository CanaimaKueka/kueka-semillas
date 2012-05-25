#!/usr/bin/python
#-*- coding: UTF-8 -*-

from library.misc import *

def ConfigMapper(Config, CONFDIR):
    conffiles = listdirfullpath(CONFDIR)
    configuration = Config.read(conffiles)
    dictionary = {}
    sections = Config.sections()
    for section in sections:
        options = Config.options(section)
        for option in options:
            try:
                giveme = Config.get(section, option)
                if section == 'array':
                    process = giveme[1:-1].split(',')
                elif section == 'boolean':
                    process = giveme
                elif section == 'integer':
                    process = int(giveme)
                else:
                    process = '"'+giveme+'"'
                dictionary[option] = process
            except:
                dictionary[option] = None
    return dictionary
