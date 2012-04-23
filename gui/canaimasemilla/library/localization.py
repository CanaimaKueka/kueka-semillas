#!/usr/bin/python
#-*- coding: UTF-8 -*-

from gettext import gettext as _
import gettext
import locale
import logging

def init_localization():
    locale.setlocale(locale.LC_ALL, '')
    loc = locale.getlocale()
    filename = "res/messages_%s.mo" % locale.getlocale()[0][0:2]
    
    try:
        logging.debug( "Opening message file %s for locale %s", filename, loc[0] )
        trans = gettext.GNUTranslations(open( filename, "rb" ) )
    except IOError:
        logging.debug( "Locale not found. Using default messages" )
        trans = gettext.NullTranslations()

    trans.install()
  
if __name__ == '__main__':
    init_localization()
