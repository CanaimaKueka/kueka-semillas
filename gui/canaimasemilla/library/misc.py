#!/usr/bin/python
#-*- coding: UTF-8 -*-

import os

def listdirfullpath(d):
    return [os.path.join(d, f) for f in os.listdir(d)]
