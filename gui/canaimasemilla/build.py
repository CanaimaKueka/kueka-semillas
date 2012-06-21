#!/usr/bin/env python
#-*- coding: UTF-8 -*-

# Librerías Globales
import gtk, sys

# Librerías Locales
from library.controller import Build

gtk.gdk.threads_init()

if __name__ == "__main__":
    app = Build()
    gtk.main()
    sys.exit()
