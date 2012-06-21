#!/usr/bin/env python
#-*- coding: UTF-8 -*-

# Librerías Globales
import gtk, sys

# Librerías Locales
from library.controller import Save

gtk.gdk.threads_init()

if __name__ == "__main__":
    app = Save()
    gtk.main()
    sys.exit()
