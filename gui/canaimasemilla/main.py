#!/usr/bin/env python
#-*- coding: UTF-8 -*-

# Librerías Globales
import gtk, sys

# Librerías Locales
from library.controller import Main

gtk.gdk.threads_init()

if __name__ == "__main__":
    app = Main()
    gtk.main()
    sys.exit()
