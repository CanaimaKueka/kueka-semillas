#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import gtk, sys
#import pygtk, gtk, re, os, sys, threading, urllib2, shutil, pango, gobject, Queue, time, tempfile
#from subprocess import Popen, PIPE, STDOUT
#from aptsources.distinfo import DistInfo

## Librerías Locales
import main
from library.vocabulary import *
from library.intelligence import *
from library.dynamism import *
from library.creativity import *
from config import *

gtk.gdk.threads_init()

class Profile():
    def __init__(self):
        self.window = gtk.Window()
        self.window.set_border_width(0)
        self.window.set_title(PROFILE_TITLE)
        self.window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        self.window.set_size_request(window_width, window_height)
        self.window.set_resizable(False)
        self.window.connect("destroy", gtk.main_quit)
        self.window.set_icon_from_file(ICONDIR+'/48x48/apps/c-s-gui.png')

        self.outbox = gtk.VBox(False, 0)
        self.swindow = gtk.ScrolledWindow()
        self.swindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.swindow.set_border_width(10)
        self.vbox = gtk.VBox(False, 5)

        self.banner = Banner(self, GUIDIR+'/images/banner.png')
        self.outbox.pack_start(self.banner, False, False, 0)

        self.profile_name_title = Title(class_id = self, text = PROFILE_PROFILE_NAME_1)
        self.profile_arch_title = Title(class_id = self, text = PROFILE_PROFILE_ARCH_1)
        self.author_name_title = Title(class_id = self, text = PROFILE_AUTHOR_NAME_1)
        self.author_email_title = Title(class_id = self, text = PROFILE_AUTHOR_EMAIL_1)
        self.author_url_title = Title(class_id = self, text = PROFILE_AUTHOR_URL_1)
        self.os_locale_title = Title(class_id = self, text = PROFILE_OS_LOCALE_1)
        self.meta_dist_title = Title(class_id = self, text = PROFILE_META_DIST_1)
        self.meta_codename_title = Title(class_id = self, text = PROFILE_META_CODENAME_1)
        self.meta_repo_title = Title(class_id = self, text = PROFILE_META_REPO_1)
        self.meta_reposections_title = Title(class_id = self, text = PROFILE_META_REPOSECTIONS_1)
        self.os_packages_title = Title(class_id = self, text = PROFILE_OS_PACKAGES_1)

        self.profile_name_description = Description(class_id = self, text = PROFILE_PROFILE_NAME_2)
        self.profile_arch_description = Description(class_id = self, text = PROFILE_PROFILE_ARCH_2)
        self.author_name_description = Description(class_id = self, text = PROFILE_AUTHOR_NAME_2)
        self.author_email_description = Description(class_id = self, text = PROFILE_AUTHOR_EMAIL_2)
        self.author_url_description = Description(class_id = self, text = PROFILE_AUTHOR_URL_2)
        self.os_locale_description = Description(class_id = self, text = PROFILE_OS_LOCALE_2)
        self.meta_dist_description = Description(class_id = self, text = PROFILE_META_DIST_2)
        self.meta_codename_description = Description(class_id = self, text = PROFILE_META_CODENAME_2)
        self.meta_repo_description = Description(class_id = self, text = PROFILE_META_REPO_2)
        self.meta_reposections_description = Description(class_id = self, text = PROFILE_META_REPOSECTIONS_2)
        self.os_extrarepos_description = Description(class_id = self, text = PROFILE_OS_EXTRAREPOS_2)
        self.os_packages_description = Description(class_id = self, text = PROFILE_OS_PACKAGES_2)

        self.profile_name, self.profilename = TextEntry(
            class_id = self, indent = True, maxlength = 18, length = 18,
            text = default_profile_name, regex = '^[a-z-]*$',
            flimit = LimitEntry, fclear = ClearEntry, ffill = FillEntry
            )

        self.profile_arch, self.profilearch = CheckList(
            class_id = self, indent = True,
            checklist = supported_arch, checkdefault = ''
            )

        self.author_name, self.authorname = TextEntry(
            class_id = self, indent = True, maxlength = 60, length = 60,
            text = default_profile_author, regex = '\w',
            flimit = LimitEntry, fclear = ClearEntry, ffill = FillEntry
            )

        self.author_email, self.authoremail = TextEntry(
            class_id = self, indent = True, maxlength = 60, length = 60,
            text = default_profile_email, regex = '^[_.@0-9A-Za-z-]*$',
            flimit = LimitEntry, fclear = ClearEntry, ffill = FillEntry
            )

        self.author_url, self.authorurl = TextEntry(
            class_id = self, indent = True, maxlength = 60, length = 60,
            text = default_profile_url, regex = '^[-A-Za-z0-9+&@#/%?=~_()|!:,.;]*$',
            flimit = LimitEntry, fclear = ClearEntry, ffill = FillEntry
            )

        self.localelist, self.localeactive = LocaleList(
            class_id = self, supported = supported_locales,
            current = os.environ['LC_ALL']
            )

        self.os_locale, self.oslocale = Combo(
            class_id = self, indent = True, combolist = self.localelist,
            combodefault = self.localeactive, entry = False,
            f_1 = Dummy, p_1 = {},
            f_2 = Dummy, p_2 = {},
            f_3 = Dummy, p_3 = {}
            )

        self.meta_dist, self.metadist = Combo(
            class_id = self, indent = True, combolist = cs_distros,
            combodefault = 2, entry = False,
            f_1 = ChangeCodename, p_1 = {},
            f_2 = ChangeRepo, p_2 = {},
            f_3 = ChangeSections, p_3 = {}
            )

        self.codenamelist, self.codenameactive = CodenameList(
            class_id = self, dist = self.metadist, db = apt_templates
            )

        self.meta_codename, self.metacodename = Combo(
            class_id = self, indent = True, combolist = self.codenamelist,
            combodefault = self.codenameactive, entry = True,
            f_1 = Dummy, p_1 = {},
            f_2 = Dummy, p_2 = {},
            f_3 = Dummy, p_3 = {}
            )

        self.meta_repo, self.metarepo = TextEntry(
            class_id = self, indent = True, maxlength = 60, length = 60,
            text = canaima_repo, regex = '^[-A-Za-z0-9+&@#/%?=~_()|!:,.;]*$',
            flimit = LimitEntry, fclear = ClearEntry, ffill = FillEntry
            )

        self.sectionlist = SectionList(class_id = self, dist = self.metadist)

        self.meta_reposections , self.metareposections = CheckList(
            class_id = self, indent = True,
            checklist = self.sectionlist, checkdefault = 'main'
            )

        self.os_extrarepos, self.osextrarepos = ScrolledFrame(class_id = self)

        self.os_extrarepos_entries_box = gtk.HBox(homogeneous, spacing)

        self.os_extrarepos_check, self.osextrareposcheck = ActiveCheck(
            class_id = self, text = PROFILE_OS_EXTRAREPOS_CHECK, active = False,
            f_1 = Toggle, p_1 = { 'destination': self.os_extrarepos },
            f_2 = Toggle, p_2 = { 'destination': self.os_extrarepos_entries_box },
            f_3 = Dummy, p_3 = {}
            )

        self.os_extrarepos_url, self.osextrareposurl = TextEntry(
            class_id = self, indent = False, maxlength = 60, length = 38,
            text = PROFILE_OS_EXTRAREPOS_URL, regex = '^[-A-Za-z0-9+&@#/%?=~_()|!:,.;]*$',
            flimit = LimitEntry, fclear = ClearEntry, ffill = FillEntry
            )

        self.os_extrarepos_branch, self.osextrareposbranch = TextEntry(
            class_id = self, indent = False, maxlength = 60, length = 10,
            text = PROFILE_OS_EXTRAREPOS_BRANCH, regex = '^[A-Za-z0-9-]*$',
            flimit = LimitEntry, fclear = ClearEntry, ffill = FillEntry
            )

        self.os_extrarepos_sections, self.osextrarepossections = TextEntry(
            class_id = self, indent = False, maxlength = 60, length = 17,
            text = PROFILE_OS_EXTRAREPOS_SECTIONS, regex = '^[A-Za-z0-9\ -]*$',
            flimit = LimitEntry, fclear = ClearEntry, ffill = FillEntry
            )

        self.os_extrarepos_add, self.osextrareposadd = ActiveButton(
            class_id = self, text = gtk.STOCK_ADD,
            width = 0, height = 0, f_1 = AddExtraRepos,
            p_1 = {
                'url': self.osextrareposurl,
                'branch': self.osextrareposbranch,
                'sections': self.osextrarepossections,
                'arch_container': self.profilearch,
                'repolist': self.osextrarepos,
                'fvalidation': is_valid_url,
                'fok': AddExtraReposThread,
                'ferror': UserMessage,
                'fprogresswindow': ProgressWindow,
                'frequest': HeadRequest,
                'errormessage': PROFILE_OS_EXTRAREPOS_VALIDATE_URL_ERROR,
                'errortitle': PROFILE_OS_EXTRAREPOS_VALIDATE_URL_ERROR_TITLE,
                'progressmessage': PROFILE_OS_EXTRAREPOS_VALIDATE_URL,
                'progresstitle': PROFILE_OS_EXTRAREPOS_VALIDATE
            },
            f_2 = Dummy, p_2 = {},
            f_3 = Dummy, p_3 = {}
            )

        self.os_extrarepos_clean, self.osextrareposclean = ActiveButton(
            class_id = self, text = gtk.STOCK_CLEAR,
            width = 0, height = 0,
            f_1 = CleanEntry, p_1 = { 'destination': self.osextrarepos },
            f_2 = Dummy, p_2 = {},
            f_3 = Dummy, p_3 = {}
            )

        self.os_packages, self.ospackages = ScrolledFrame(class_id = self)

        self.os_packages_entries_box = gtk.HBox(homogeneous, spacing)

        self.os_packages_name, self.ospackagesname = TextEntry(
            class_id = self, indent = False, maxlength = 60, length = 38,
            text = PROFILE_OS_PACKAGES_NAME, regex = '^[A-Za-z0-9\ -]*$',
            flimit = LimitEntry, fclear = ClearEntry, ffill = FillEntry
            )

        self.os_packages_add, self.ospackagesadd = ActiveButton(
            class_id = self, text = gtk.STOCK_ADD,
            width = 0, height = 0, f_1 = AddPackages,
            p_1 = {
                'url': self.metarepo,
                'branch': self.metacodename,
                'section_container': self.metareposections,
                'arch_container': self.profilearch,
                'extrarepos': self.osextrarepos,
                'packages': self.ospackagesname,
                'packageslist': self.ospackages,
                'fok': AddPackagesThread,
                'ferror': UserMessage,
                'fprogresswindow': ProgressWindow,
                'fprogress': DownloadProgress,
                'freplace': replace_all,
                'fcleantempdir': CleanTempDir,
                'errormessage': PROFILE_OS_EXTRAREPOS_VALIDATE_URL_ERROR,
                'errortitle': PROFILE_OS_EXTRAREPOS_VALIDATE_URL_ERROR_TITLE,
                'progressmessage': PROFILE_OS_EXTRAREPOS_VALIDATE_URL,
                'progresstitle': PROFILE_OS_EXTRAREPOS_VALIDATE
            },
            f_2 = Dummy, p_2 = {},
            f_3 = Dummy, p_3 = {}
            )

        self.os_packages_clean, self.ospackagesclean = ActiveButton(
            class_id = self, text = gtk.STOCK_CLEAR,
            width = 0, height = 0,
            f_1 = CleanEntry, p_1 = { 'destination': self.ospackages },
            f_2 = Dummy, p_2 = {},
            f_3 = Dummy, p_3 = {}
            )

        self.vbox.pack_start(self.profile_name_title, False, False, 0)
        self.vbox.pack_start(self.profile_name_description, False, False, 0)
        self.vbox.pack_start(self.profile_name, False, False, 0)
        self.vbox.pack_start(gtk.HSeparator(), False, False, 0)
        self.vbox.pack_start(self.profile_arch_title, False, False, 0)
        self.vbox.pack_start(self.profile_arch_description, False, False, 0)
        self.vbox.pack_start(self.profile_arch, False, False, 0)
        self.vbox.pack_start(gtk.HSeparator(), False, False, 0)
        self.vbox.pack_start(self.author_name_title, False, False, 0)
        self.vbox.pack_start(self.author_name_description, False, False, 0)
        self.vbox.pack_start(self.author_name, False, False, 0)
        self.vbox.pack_start(gtk.HSeparator(), False, False, 0)
        self.vbox.pack_start(self.author_email_title, False, False, 0)
        self.vbox.pack_start(self.author_email_description, False, False, 0)
        self.vbox.pack_start(self.author_email, False, False, 0)
        self.vbox.pack_start(gtk.HSeparator(), False, False, 0)
        self.vbox.pack_start(self.author_url_title, False, False, 0)
        self.vbox.pack_start(self.author_url_description, False, False, 0)
        self.vbox.pack_start(self.author_url, False, False, 0)
        self.vbox.pack_start(gtk.HSeparator(), False, False, 0)
        self.vbox.pack_start(self.os_locale_title, False, False, 0)
        self.vbox.pack_start(self.os_locale_description, False, False, 0)
        self.vbox.pack_start(self.os_locale, False, False, 0)
        self.vbox.pack_start(gtk.HSeparator(), False, False, 0)
        self.vbox.pack_start(self.meta_dist_title, False, False, 0)
        self.vbox.pack_start(self.meta_dist_description, False, False, 0)
        self.vbox.pack_start(self.meta_dist, False, False, 0)
        self.vbox.pack_start(gtk.HSeparator(), False, False, 0)
        self.vbox.pack_start(self.meta_codename_title, False, False, 0)
        self.vbox.pack_start(self.meta_codename_description, False, False, 0)
        self.vbox.pack_start(self.meta_codename, False, False, 0)
        self.vbox.pack_start(gtk.HSeparator(), False, False, 0)
        self.vbox.pack_start(self.meta_repo_title, False, False, 0)
        self.vbox.pack_start(self.meta_repo_description, False, False, 0)
        self.vbox.pack_start(self.meta_repo, False, False, 0)
        self.vbox.pack_start(gtk.HSeparator(), False, False, 0)
        self.vbox.pack_start(self.meta_reposections_title, False, False, 0)
        self.vbox.pack_start(self.meta_reposections_description, False, False, 0)
        self.vbox.pack_start(self.meta_reposections, False, False, 0)
        self.vbox.pack_start(gtk.HSeparator(), False, False, 0)
        self.vbox.pack_start(self.os_extrarepos_check, False, False, 0)
        self.vbox.pack_start(self.os_extrarepos, False, False, 0)
        self.os_extrarepos_entries_box.pack_start(self.os_extrarepos_url, False, False, 0)
        self.os_extrarepos_entries_box.pack_start(self.os_extrarepos_branch, False, False, 0)
        self.os_extrarepos_entries_box.pack_start(self.os_extrarepos_sections, False, False, 0)
        self.os_extrarepos_entries_box.pack_start(self.os_extrarepos_add, False, False, 0)
        self.os_extrarepos_entries_box.pack_start(self.os_extrarepos_clean, False, False, 0)
        self.vbox.pack_start(self.os_extrarepos_entries_box, False, False, 0)
        self.vbox.pack_start(self.os_extrarepos_description, False, False, 0)
        self.vbox.pack_start(gtk.HSeparator(), False, False, 0)
        self.vbox.pack_start(self.os_packages_title, False, False, 0)
        self.vbox.pack_start(self.os_packages, False, False, 0)
        self.os_packages_entries_box.pack_start(self.os_packages_name, False, False, 0)
        self.os_packages_entries_box.pack_start(self.os_packages_add, False, False, 0)
        self.os_packages_entries_box.pack_start(self.os_packages_clean, False, False, 0)
        self.vbox.pack_start(self.os_packages_entries_box, False, False, 0)
        self.vbox.pack_start(self.os_packages_description, False, False, 0)
        self.swindow.add_with_viewport(self.vbox)
        self.outbox.add(self.swindow)

        self.separator = gtk.HSeparator()
        self.outbox.pack_start(self.separator, False, False, 0)

        self.box = self.Botones(False, 0, False, False, 0, 5, 80, 30)
        self.outbox.pack_start(self.box, False, False, 0)
        
        self.window.add(self.outbox)
        self.window.show_all()

        Toggle(self.os_extrarepos_check, { 'destination': self.os_extrarepos })
        Toggle(self.os_extrarepos_check, { 'destination': self.os_extrarepos_entries_box })

if __name__ == "__main__":
    app = Profile()
    gtk.main()
    sys.exit()
