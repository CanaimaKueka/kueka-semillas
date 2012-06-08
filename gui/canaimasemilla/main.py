#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Librerías Globales
import gtk, sys

# Librerías Locales
import build, profile, test, save
from library.vocabulary import *
from library.creativity import Banner, IconButton, BottomButtons, AboutWindow
from library.intelligence import ThreadGenerator, ProcessGenerator
from config import *

gtk.gdk.threads_init()

class Main():
    def __init__(self):
        # Creating Window
        self.window = gtk.Window()
        self.window.set_border_width(0)
        self.window.set_title(MAIN_TITLE)
        self.window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        self.window.set_size_request(window_width, window_height)
        self.window.set_resizable(False)
        self.window.connect("destroy", gtk.main_quit)
        self.window.set_icon_from_file(ICONDIR+'/48x48/apps/c-s-gui.png')

        # Creating Objects
        self.vbox = gtk.VBox(False, 5)
        self.banner = Banner(self, GUIDIR+'/images/banner.png')
        self.button_box = gtk.VBox(homogeneous, spacing)
        self.button_box.set_border_width(10)
        self.button_row1 = gtk.HBox(homogeneous, spacing)
        self.button_row2 = gtk.HBox(homogeneous, spacing)

        self.create_profile = IconButton(
            class_id = self, icon = GUIDIR+'/images/create-profile.png',
            text_1 = MAIN_CREATE_PROFILE_TITLE, text_2 = MAIN_CREATE_PROFILE_TEXT,
            width = 330, height = 170, f_1 = ThreadGenerator,
            p_1 = (True, self.window, profile.Profile, {})
            )

        self.build_image = IconButton(
            class_id = self, icon = GUIDIR+'/images/build-image.png',
            text_1 = MAIN_BUILD_IMAGE_TITLE, text_2 = MAIN_BUILD_IMAGE_TEXT,
            width = 330, height = 170, f_1 = ThreadGenerator,
            p_1 = (True, self.window, build.Build, {})
            )

        self.test_image = IconButton(
            class_id = self, icon = GUIDIR+'/images/test-image.png',
            text_1 = MAIN_TEST_IMAGE_TITLE, text_2 = MAIN_TEST_IMAGE_TEXT,
            width = 330, height = 170, f_1 = ThreadGenerator,
            p_1 = (True, self.window, test.Test, {})
            )

        self.save_image = IconButton(
            class_id = self, icon = GUIDIR+'/images/save-image.png',
            text_1 = MAIN_SAVE_IMAGE_TITLE, text_2 = MAIN_SAVE_IMAGE_TEXT,
            width = 330, height = 170, f_1 = ThreadGenerator,
            p_1 = (True, self.window, save.Save, {})
            )

        self.bottombuttons = BottomButtons(
            class_id = self, width = 80, height = 30,
            fclose = gtk.main_quit, pclose = (),
            fhelp = ThreadGenerator,
            phelp = (
                False, False, ProcessGenerator, {
                    'command': ['/usr/bin/yelp', DOCDIR+'/index.html']
                    }
                ),
            fabout = ThreadGenerator,
            pabout = (
                True, False, AboutWindow, {
                    'img': GUIDIR+'/images/logo.png', 'name': app_name,
                    'version': app_version, 'url': app_url,
                    'copyright': app_copyright, 'description': app_description,
                    'authorsfile': SHAREDIR+'/AUTHORS',
                    'licensefile': SHAREDIR+'/LICENSE',
                    'translatorsfile': SHAREDIR+'/TRANSLATORS'
                    }
                )
            )

        # Packing Objects
        self.vbox.pack_start(self.banner, expand, fill, padding)
        self.button_row1.pack_start(self.create_profile, expand, fill, padding)
        self.button_row1.pack_start(self.build_image, expand, fill, padding)
        self.button_box.pack_start(self.button_row1, expand, fill, padding)
        self.button_row2.pack_start(self.test_image, expand, fill, padding)
        self.button_row2.pack_start(self.save_image, expand, fill, padding)
        self.button_box.pack_start(self.button_row2, expand, fill, padding)
        self.vbox.pack_start(self.button_box, expand, fill, padding)
        self.vbox.pack_start(self.bottombuttons, expand, fill, padding)
        self.window.add(self.vbox)

        # Showing
        self.window.show_all()

if __name__ == "__main__":
    app = Main()
    gtk.main()
    sys.exit()
