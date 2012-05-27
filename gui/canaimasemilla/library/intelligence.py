#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from aptsources.distinfo import DistInfo
from config import *

def Dummy(signaled, class_id):
    pass

def LocaleList(class_id, supported, current):
    localecount = 0
    localeactive = 0
    localelist = []
    with open(supported, 'r') as supportedlocales:
        for item in supportedlocales:
            localecode = item.split()
            localelist.append(localecode[0])
            if localecode[0].upper().replace('-','') == current.upper().replace('-',''):
                localeactive = localecount
            localecount += 1

    return localelist, localeactive

def CodenameList(class_id, dist, db):
    codenamelist = []
    codenameactive = 0
    udist = dist.get_active_text().title()
    d = DistInfo(udist, db)

    for template in d.templates:
        if not template.name in codenamelist:
            codenamelist.append(template.name)

    return codenamelist, codenameactive

def SectionList(class_id, dist):
    text = dist.get_active_text()
    exec "sectionlist = "+text+"_sections"
    return sectionlist

def listdirfullpath(d):
    return [os.path.join(d, f) for f in os.listdir(d)]

def is_valid_url(url):
    regex = re.compile(
        r'^(http|ftp|file):///?'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|[a-zA-Z0-9-]*|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return regex.search(url)

def AddExtraRepos(class_id, textbuffer, extrareposurl, extrareposrama, extrareposseccion):
    if is_valid_url(extrareposurl.get_text()):
        hilo = threading.Thread(
            target = AddExtraReposThread, args=(self, homogeneous, spacing, expand, fill, padding, borderwidth, textbuffer, extrareposurl, extrareposrama, extrareposseccion))
            hilo.start()
        else:
            hilo = threading.Thread(target=self.ErrorExtraReposThread, args=(PROFILE_OS_EXTRAREPOS_VALIDATE_URL_ERROR, PROFILE_OS_EXTRAREPOS_VALIDATE_URL_ERROR_TITLE))
            hilo.start()
