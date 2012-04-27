#!/usr/bin/python
#-*- coding: UTF-8 -*-

import os, ConfigParser
from library.configuration import *

curdir = os.path.dirname(os.path.abspath(os.getcwd()))

if curdir == '/usr/share/pyshared':
    GUIDIR = '/usr/share/pyshared/canaimasemilla'
    CONFDIR = '/etc/canaima-semilla/gui'
    BINDIR = '/usr/bin'
    CSBIN = 'c-s'
    COREDIR = '/usr/share/canaima-semilla/scripts'
    PROFILEDIR = '/usr/share/canaima-semilla/profiles'
    DOCDIR = '/usr/share/doc/canaima-semilla/html'
    ICONDIR = '/usr/share/icons/hicolor'
else:
    GUIDIR = curdir+'/canaimasemilla'
    SRCDIR = os.path.dirname(curdir)
    CONFDIR = SRCDIR+'/config/gui'
    BINDIR = SRCDIR+'/scripts'
    CSBIN = 'c-s.sh'
    COREDIR = SRCDIR+'/scripts'
    PROFILEDIR = SRCDIR+'/profiles'
    DOCDIR = SRCDIR+'/documentation/html'
    ICONDIR = SRCDIR+'/icons/hicolor'

Config = ConfigParser.ConfigParser()
configload = ConfigMapper(Config, CONFDIR)

for configoption, configvalue in configload.iteritems():
    exec str(configoption)+' = '+str(configvalue)
