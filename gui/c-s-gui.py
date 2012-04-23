#!/usr/bin/python
#-*- coding: UTF-8 -*-

import os, sys, canaimasemilla

if os.geteuid() != 0:
    print 'It is not recommended to start Ucumari as root.'

path = os.path.dirname(os.path.abspath(canaimasemilla.__file__))
os.chdir(path)
os.execv('/usr/bin/env', ['/usr/bin/env', 'python', 'main.py'] + sys.argv[1:])
