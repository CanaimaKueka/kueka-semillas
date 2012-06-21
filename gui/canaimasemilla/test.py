#!/usr/bin/env python
#-*- coding: UTF-8 -*-

# Librerías Globales
import gtk, sys

# Librerías Locales
from library.controller import Test

gtk.gdk.threads_init()

if __name__ == "__main__":
    app = Test()
    gtk.main()
    sys.exit()
