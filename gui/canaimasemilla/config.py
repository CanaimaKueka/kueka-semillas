#!/usr/bin/python
#-*- coding: UTF-8 -*-

import os, ConfigParser

def listdirfullpath(d):
    return [os.path.join(d, f) for f in os.listdir(d)]

def ConfigMapper(confdir):
    dictionary = {}
    config = ConfigParser.ConfigParser()
    conffiles = listdirfullpath(confdir)
    configuration = config.read(conffiles)
    sections = config.sections()
    for section in sections:
        options = config.options(section)
        for option in options:
            try:
                giveme = config.get(section, option)
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
    LOCALEDIR = '/usr/share/locale/'
    SHAREDIR = '/usr/share/canaima-semilla/'
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
    LOCALEDIR = SRCDIR+'/locale'
    SHAREDIR = SRCDIR

configload = ConfigMapper(CONFDIR)

for configoption, configvalue in configload.iteritems():
    exec str(configoption)+' = '+str(configvalue)
