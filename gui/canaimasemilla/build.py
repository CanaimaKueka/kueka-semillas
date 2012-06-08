#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import gtk, sys

# Librerías Locales
import main
from library.vocabulary import *
from library.creativity import *
from library.dynamism import *
from library.intelligence import *
from config import *

gtk.gdk.threads_init()

class Build():
    def __init__(self):
        # Creating Window
        self.window = gtk.Window()
        self.window.set_border_width(0)
        self.window.set_title(BUILD_TITLE)
        self.window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        self.window.set_size_request(window_width, window_height)
        self.window.set_resizable(False)
        self.window.connect("destroy", gtk.main_quit)
        self.window.set_icon_from_file(ICONDIR+'/48x48/apps/c-s-gui.png')

        self.vbox = gtk.VBox(False, 5)
        self.inbox = gtk.VBox(False, 5)
        self.inbox.set_border_width(10)

        self.profile_name_title = Title(class_id = self, text = BUILD_PROFILE_NAME_1)
        self.profile_arch_title = Title(class_id = self, text = BUILD_PROFILE_ARCH_1)
        self.profile_media_title = Title(class_id = self, text = BUILD_PROFILE_MEDIA_1)

        self.profile_name_description = Description(class_id = self, text = BUILD_PROFILE_NAME_2)
        self.profile_arch_description = Description(class_id = self, text = BUILD_PROFILE_ARCH_2)
        self.profile_media_description = Description(class_id = self, text = BUILD_PROFILE_MEDIA_2)

        self.profilelist, self.profiledefault = ProfileList(
            class_id = self, profiledir = PROFILEDIR
            )

        self.nativearch = GetArch()

        self.banner = Banner(self, GUIDIR+'/images/banner.png')

        self.profile_name, self.profilename = Combo(
            class_id = self, indent = True, combolist = self.profilelist,
            combodefault = self.profiledefault, entry = False,
            f_1 = Dummy, p_1 = {},
            f_2 = Dummy, p_2 = {},
            f_3 = Dummy, p_3 = {}
            )

        self.profile_arch, self.profilearch = OptionList(
            class_id = self, indent = True, optionlist = supported_arch, optiondefault = ''
            )

        self.profile_media, self.profilemedia = OptionList(
            class_id = self, indent = True, optionlist = supported_media, optiondefault = ''
            )

        if self.nativearch == 'i686':
            for child in self.profilearch:
                if child.get_label() == 'amd64':
                    child.set_sensitive(False)

        self.bottombuttons = BottomButtons(
            classid = self, bwidth = 80, bheight = 30,
            fclose = ThreadGenerator,
            pclose = {
                'function': UserMessage,
                'params': (
                    BUILD_CONFIRM_CANCEL_MSG, BUILD_CONFIRM_CANCEL_TITLE,
                    gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO, True,
                    gtk.RESPONSE_YES, KillProcess, (['lb', 'live-build', 'c-s'],),
                    gtk.RESPONSE_YES, self.window.destroy, '',
                    gtk.RESPONSE_YES, gtk.main_quit, ()
                    ),
                'gtk': True,
                'hide': ''
                },
            fhelp = ThreadGenerator,
            phelp = {
                'function': ProcessGenerator,
                'params': (['/usr/bin/yelp', DOCDIR+'/index.html'],),
                'gtk': False
                },
            fabout = ThreadGenerator,
            pabout = {
                'function': AboutWindow,
                'params': (
                    GUIDIR+'/images/logo.png', app_name, app_version,
                    app_url, app_copyright, app_description,
                    SHAREDIR+'/AUTHORS', SHAREDIR+'/LICENSE',
                    SHAREDIR+'/TRANSLATORS'
                    ),
                'gtk': True,
                'hide': ''
                },
            fback = ThreadGenerator,
            pback = {
                'function': UserMessage,
                'params': (
                    BUILD_CONFIRM_CANCEL_MSG, BUILD_CONFIRM_CANCEL_TITLE,
                    gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO, True,
                    gtk.RESPONSE_YES, KillProcess, (['lb', 'live-build', 'c-s'],),
                    gtk.RESPONSE_YES, self.window.hide, (),
                    gtk.RESPONSE_YES, main.Main, ()
                    ),
                'gtk': True,
                'hide': ''
                },
            fgo = ThreadGenerator,
            pgo = {
                'function': UserMessage,
                'params': (
                    BUILD_CONFIRM_OK_MSG, BUILD_CONFIRM_OK_TITLE,
                    gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO, True,
                    gtk.RESPONSE_YES, BuildImage,(
                        self.profilename, self.profilearch,
                        self.profilemedia, self.inbox
                    ),
                    gtk.RESPONSE_YES, Dummy, (),
                    gtk.RESPONSE_YES, Dummy, ()
                    ),
                'gtk': True,
                'hide': ''
                },
            fdummy = Dummy, pdummy = {}
            )

        self.vbox.pack_start(self.banner, expand, fill, padding)

        self.inbox.pack_start(self.profile_name_title, expand, fill, padding)
        self.inbox.pack_start(self.profile_name_description, expand, fill, padding)
        self.inbox.pack_start(self.profile_name, expand, fill, padding)
        self.inbox.pack_start(gtk.HSeparator(), expand, fill, padding)
        self.inbox.pack_start(self.profile_arch_title, expand, fill, padding)
        self.inbox.pack_start(self.profile_arch_description, expand, fill, padding)
        self.inbox.pack_start(self.profile_arch, expand, fill, padding)
        self.inbox.pack_start(gtk.HSeparator(), expand, fill, padding)
        self.inbox.pack_start(self.profile_media_title, expand, fill, padding)
        self.inbox.pack_start(self.profile_media_description, expand, fill, padding)
        self.inbox.pack_start(self.profile_media, expand, fill, padding)
        self.inbox.pack_start(self.bottombuttons, expand, fill, padding)

        self.vbox.pack_start(self.inbox, expand, fill, padding)

        self.window.add(self.vbox)
        self.window.show_all()

if __name__ == "__main__":
    app = Build()
    gtk.main()
    sys.exit()
