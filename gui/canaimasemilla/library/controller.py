#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Librerías Globales
import gtk, sys

# Librerías Locales
from config import *
from library.vocabulary import *
from library.creativity import *
from library.intelligence import *

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
        self.vbox = gtk.VBox(homogeneous, spacing)
        self.banner = Banner(self, GUIDIR+'/images/banner.png')
        self.button_box = gtk.VBox(homogeneous, 5)
        self.button_box.set_border_width(10)
        self.button_row1 = gtk.HBox(homogeneous, spacing)
        self.button_row2 = gtk.HBox(homogeneous, spacing)

        self.create_profile = IconButton(
            class_id = self, icon = GUIDIR+'/images/create-profile.png',
            text_1 = MAIN_CREATE_PROFILE_TITLE, text_2 = MAIN_CREATE_PROFILE_TEXT,
            width = 330, height = 180, f_1 = ThreadGenerator,
            p_1 = (Profile, {}, True, self.window)
            )

        self.build_image = IconButton(
            class_id = self, icon = GUIDIR+'/images/build-image.png',
            text_1 = MAIN_BUILD_IMAGE_TITLE, text_2 = MAIN_BUILD_IMAGE_TEXT,
            width = 330, height = 180, f_1 = ThreadGenerator,
            p_1 = (Build, {}, True, self.window)
            )

        self.test_image = IconButton(
            class_id = self, icon = GUIDIR+'/images/test-image.png',
            text_1 = MAIN_TEST_IMAGE_TITLE, text_2 = MAIN_TEST_IMAGE_TEXT,
            width = 330, height = 180, f_1 = ThreadGenerator,
            p_1 = (Test, {}, True, self.window)
            )

        self.save_image = IconButton(
            class_id = self, icon = GUIDIR+'/images/save-image.png',
            text_1 = MAIN_SAVE_IMAGE_TITLE, text_2 = MAIN_SAVE_IMAGE_TEXT,
            width = 330, height = 180, f_1 = ThreadGenerator,
            p_1 = (Save, {}, True, self.window)
            )

        self.bottombuttons = BottomButtons(
            class_id = self, width = 80, height = 30,
            fclose = gtk.main_quit, pclose = (),
            fhelp = ThreadGenerator,
            phelp = (
                ProcessGenerator, {
                    'command': ['/usr/bin/yelp', DOCDIR+'/index.html']
                    },
                False, False
                ),
            fabout = ThreadGenerator,
            pabout = (
                AboutWindow, {
                    'img': GUIDIR+'/images/logo.png', 'name': app_name,
                    'version': app_version, 'url': app_url,
                    'copyright': app_copyright, 'description': app_description,
                    'authorsfile': SHAREDIR+'/AUTHORS',
                    'licensefile': SHAREDIR+'/LICENSE',
                    'translatorsfile': SHAREDIR+'/TRANSLATORS'
                    },
                True, False
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

        self.vbox = gtk.VBox(homogeneous, spacing)
        self.inbox = gtk.VBox(homogeneous, 5)
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
            combodefault = self.profiledefault, entry = False
            )

        self.profile_arch, self.profilearch = OptionList(
            class_id = self, indent = True, optionlist = supported_arch
            )

        self.profile_media, self.profilemedia = OptionList(
            class_id = self, indent = True, optionlist = supported_media
            )

        if self.nativearch == 'i686':
            for child in self.profilearch:
                if child.get_label() == 'amd64':
                    child.set_sensitive(False)

        self.bottombuttons = BottomButtons(
            class_id = self, width = 80, height = 30,
            fclose = ThreadGenerator,
            pclose = (
                UserMessage, {
                    'message': BUILD_CONFIRM_CANCEL_MSG,
                    'title': BUILD_CONFIRM_CANCEL_TITLE,
                    'type': gtk.MESSAGE_QUESTION,
                    'buttons': gtk.BUTTONS_YES_NO,
                    'c_1': gtk.RESPONSE_YES,
                    'f_1': self.window.destroy, 'p_1': '',
                    'c_2': gtk.RESPONSE_YES,
                    'f_2': gtk.main_quit, 'p_2': ''
                    },
                True, False
                ),
            fhelp = ThreadGenerator,
            phelp = (
                ProcessGenerator, {
                    'command': ['/usr/bin/yelp', DOCDIR+'/index.html']
                    },
                True, False
            ),
            fabout = ThreadGenerator,
            pabout = (
                AboutWindow, {
                    'img': GUIDIR+'/images/logo.png', 'name': app_name,
                    'version': app_version, 'url': app_url,
                    'copyright': app_copyright, 'description': app_description,
                    'authorsfile': SHAREDIR+'/AUTHORS',
                    'licensefile': SHAREDIR+'/LICENSE',
                    'translatorsfile': SHAREDIR+'/TRANSLATORS'
                    },
                True, False
                ),
            fback = ThreadGenerator,
            pback = (
                UserMessage, {
                    'message': BUILD_CONFIRM_CANCEL_MSG % '\n\n',
                    'title': BUILD_CONFIRM_CANCEL_TITLE,
                    'type': gtk.MESSAGE_QUESTION,
                    'buttons': gtk.BUTTONS_YES_NO,
                    'c_1': gtk.RESPONSE_YES,
                    'f_1': self.window.hide, 'p_1': '',
                    'c_2': gtk.RESPONSE_YES,
                    'f_2': Main, 'p_2': ''
                    },
                True, False
                ),
            fgo = ThreadGenerator,
            pgo = (
                UserMessage, {
                    'message': BUILD_CONFIRM_OK_MSG % '\n\n',
                    'title': BUILD_CONFIRM_OK_TITLE,
                    'type': gtk.MESSAGE_QUESTION,
                    'buttons': gtk.BUTTONS_YES_NO,
                    'c_1': gtk.RESPONSE_YES,
                    'f_1': BuildImage, 'p_1': (
                        self, self.profilename, self.profilearch,
                        self.profilemedia, self.inbox
                        )
                    },
                True, False
                )
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

        self.vbox.pack_start(self.inbox, expand, fill, padding)
        self.vbox.pack_start(self.bottombuttons, expand, fill, padding)

        self.window.add(self.vbox)
        self.window.show_all()

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
        self.outbox.pack_start(self.banner, expand, fill, padding)

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
        self.img_pool_packages_title = Title(class_id = self, text = PROFILE_IMG_POOL_PACKAGES_1)
        self.os_includes_title = Title(class_id = self, text = PROFILE_OS_INCLUDES_1)
        self.img_includes_title = Title(class_id = self, text = PROFILE_IMG_INCLUDES_1)
        self.os_hooks_title = Title(class_id = self, text = PROFILE_OS_HOOKS_1)
        self.img_hooks_title = Title(class_id = self, text = PROFILE_IMG_HOOKS_1)
        self.img_syslinux_splash_title = Title(class_id = self, text = PROFILE_IMG_SYSLINUX_SPLASH_1)
        self.img_debian_installer_banner_title = Title(class_id = self, text = PROFILE_IMG_DEBIAN_INSTALLER_BANNER_1)
        self.img_debian_installer_preseed_title = Title(class_id = self, text = PROFILE_IMG_DEBIAN_INSTALLER_PRESEED_1)
        self.img_debian_installer_gtk_title = Title(class_id = self, text = PROFILE_IMG_DEBIAN_INSTALLER_GTK_1)

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
        self.img_pool_packages_description = Description(class_id = self, text = PROFILE_IMG_POOL_PACKAGES_2)
        self.os_includes_description = Description(class_id = self, text = PROFILE_OS_INCLUDES_2)
        self.img_includes_description = Description(class_id = self, text = PROFILE_IMG_INCLUDES_2)
        self.os_hooks_description = Description(class_id = self, text = PROFILE_OS_HOOKS_2)
        self.img_hooks_description = Description(class_id = self, text = PROFILE_IMG_HOOKS_2)
        self.img_syslinux_splash_description = Description(class_id = self, text = PROFILE_IMG_SYSLINUX_SPLASH_2)
        self.img_debian_installer_description = Description(class_id = self, text = PROFILE_IMG_DEBIAN_INSTALLER_2)

        self.profile_name, self.profilename = TextEntry(
            class_id = self, indent = True, maxlength = 18, length = 18,
            text = default_profile_name, regex = '^[a-z-]*$'
            )

        self.profile_arch, self.profilearch = CheckList(
            class_id = self, indent = True,
            checklist = supported_arch, checkdefault = ''
            )

        self.author_name, self.authorname = TextEntry(
            class_id = self, indent = True, maxlength = 60, length = 60,
            text = default_profile_author, regex = '\w'
            )

        self.author_email, self.authoremail = TextEntry(
            class_id = self, indent = True, maxlength = 60, length = 60,
            text = default_profile_email, regex = '^[_.@0-9A-Za-z-]*$'
            )

        self.author_url, self.authorurl = TextEntry(
            class_id = self, indent = True, maxlength = 60, length = 60,
            text = default_profile_url, regex = '^[-A-Za-z0-9+&@#/%?=~_()|!:,.;]*$'
            )

        self.localelist, self.localeactive = LocaleList(
            class_id = self, supported = supported_locales,
            current = os.environ['LC_ALL']
            )

        self.os_locale, self.oslocale = Combo(
            class_id = self, indent = True, combolist = self.localelist,
            combodefault = self.localeactive, entry = False
            )

        self.meta_dist, self.metadist = Combo(
            class_id = self, indent = True, combolist = cs_distros,
            combodefault = 2, entry = False
            )

        self.codenamelist, self.codenameactive = CodenameList(
            class_id = self, dist = self.metadist, db = apt_templates
            )

        self.meta_codename, self.metacodename = Combo(
            class_id = self, indent = True, combolist = self.codenamelist,
            combodefault = self.codenameactive, entry = True
            )

        self.meta_repo, self.metarepo = TextEntry(
            class_id = self, indent = True, maxlength = 60, length = 60,
            text = canaima_repo, regex = '^[-A-Za-z0-9+&@#/%?=~_()|!:,.;]*$'
            )

        self.sectionlist = SectionList(class_id = self, dist = self.metadist)

        self.meta_reposections , self.metareposections = CheckList(
            class_id = self, indent = True,
            checklist = self.sectionlist, checkdefault = 'main'
            )

        self.meta_dist, self.metadist = Combo(
            class_id = self, indent = True, combolist = cs_distros,
            combodefault = 2, entry = False,
            f_1 = ChangeCodename,
            p_1 = (self, self.metacodename, apt_templates),
            f_2 = ChangeRepo,
            p_2 = (self, self.metarepo),
            f_3 = ChangeSections,
            p_3 = (self, self.metareposections)
            )

        self.os_extrarepos, self.osextrarepos = ScrolledFrame(class_id = self)

        self.os_extrarepos_entries_box = gtk.HBox(homogeneous, spacing)

        self.os_extrarepos_check, self.osextrareposcheck = ActiveCheck(
            class_id = self, text = PROFILE_OS_EXTRAREPOS_CHECK, active = False,
            )

        self.os_extrarepos_check, self.osextrareposcheck = ActiveCheck(
            class_id = self, text = PROFILE_OS_EXTRAREPOS_CHECK, active = False,
            f_1 = Toggle, p_1 = (
                self.osextrareposcheck, self.os_extrarepos,
                False, False, False
                ),
            f_2 = Toggle, p_2 = (
                self.osextrareposcheck, self.os_extrarepos_entries_box,
                False, False, False
                )
            )

        self.os_extrarepos_url, self.osextrareposurl = TextEntry(
            class_id = self, indent = False, maxlength = 60, length = 38,
            text = PROFILE_OS_EXTRAREPOS_URL, regex = '^[-A-Za-z0-9+&@#/%?=~_()|!:,.;]*$'
            )

        self.os_extrarepos_branch, self.osextrareposbranch = TextEntry(
            class_id = self, indent = False, maxlength = 60, length = 10,
            text = PROFILE_OS_EXTRAREPOS_BRANCH, regex = '^[A-Za-z0-9-]*$'
            )

        self.os_extrarepos_sections, self.osextrarepossections = TextEntry(
            class_id = self, indent = False, maxlength = 60, length = 17,
            text = PROFILE_OS_EXTRAREPOS_SECTIONS, regex = '^[A-Za-z0-9\ -]*$'
            )

        self.os_extrarepos_add, self.osextrareposadd = ActiveButton(
            class_id = self, text = gtk.STOCK_ADD,
            width = 0, height = 0,
            f_1 = ThreadGenerator,
            p_1 = (
                AddExtraRepos, {
                    'class_id': self,
                    'url_entry': self.osextrareposurl,
                    'branch_entry': self.osextrareposbranch,
                    'sections_entry': self.osextrarepossections,
                    'arch_container': self.profilearch,
                    'repolistframe': self.osextrarepos,
                    },
                False, False
                )
            )

        self.os_extrarepos_clean, self.osextrareposclean = ActiveButton(
            class_id = self, text = gtk.STOCK_CLEAR,
            width = 0, height = 0,
            f_1 = CleanEntry, p_1 = (self.osextrarepos,),
            )

        self.os_packages, self.ospackages = ScrolledFrame(class_id = self)

        self.os_packages_entries_box = gtk.HBox(homogeneous, spacing)

        self.os_packages_name, self.ospackagesname = TextEntry(
            class_id = self, indent = False, maxlength = 60, length = 68,
            text = PROFILE_OS_PACKAGES_ENTRY, regex = '^[A-Za-z0-9\ -]*$'
            )

        self.os_packages_add, self.ospackagesadd = ActiveButton(
            class_id = self, text = gtk.STOCK_ADD,
            width = 0, height = 0,
            f_1 = ThreadGenerator,
            p_1 = (
                AddPackages, {
                    'class_id': self,
                    'url_entry': self.metarepo,
                    'branch_entry': self.metacodename,
                    'section_container': self.metareposections,
                    'arch_container': self.profilearch,
                    'extrareposframe': self.osextrarepos,
                    'packages_entry': self.ospackagesname,
                    'packageslistframe': self.ospackages,
                    },
                False, False
                )
            )

        self.os_packages_clean, self.ospackagesclean = ActiveButton(
            class_id = self, text = gtk.STOCK_CLEAR,
            width = 0, height = 0,
            f_1 = CleanEntry, p_1 = (self.ospackages,),
            )

        self.img_pool_packages, self.imgpoolpackages = ScrolledFrame(class_id = self)

        self.img_pool_packages_entries_box = gtk.HBox(homogeneous, spacing)

        self.img_pool_packages_name, self.imgpoolpackagesname = TextEntry(
            class_id = self, indent = False, maxlength = 1024, length = 68,
            text = PROFILE_IMG_POOL_PACKAGES_ENTRY, regex = '^[A-Za-z0-9\ -]*$'
            )

        self.img_pool_packages_add, self.imgpoolpackagesadd = ActiveButton(
            class_id = self, text = gtk.STOCK_ADD,
            width = 0, height = 0,
            f_1 = ThreadGenerator,
            p_1 = (
                AddPackages, {
                    'class_id': self,
                    'url_entry': self.metarepo,
                    'branch_entry': self.metacodename,
                    'section_container': self.metareposections,
                    'arch_container': self.profilearch,
                    'extrareposframe': self.osextrarepos,
                    'packages_entry': self.imgpoolpackagesname,
                    'packageslistframe': self.imgpoolpackages,
                    },
                False, False
                )
            )

        self.img_pool_packages_clean, self.imgpoolpackagesclean = ActiveButton(
            class_id = self, text = gtk.STOCK_CLEAR,
            width = 0, height = 0,
            f_1 = CleanEntry, p_1 = (self.imgpoolpackages,),
            )

        self.os_includes_entries_box = gtk.HBox(homogeneous, spacing)

        self.os_includes, self.osincludes = TextEntry(
            class_id = self, indent = False, maxlength = 1024, length = 68,
            text = PROFILE_OS_INCLUDES_ENTRY, regex = '^.*$'
            )

        self.os_includes_choose, self.osincludeschoose = ActiveButton(
            class_id = self, text = gtk.STOCK_OPEN,
            width = 0, height = 0,
            f_1 = ThreadGenerator,
            p_1 = (
                UserSelect, {
                    'class_id': self,
                    'title': PROFILE_OS_INCLUDES_SELECT_TITLE,
                    'action': gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,
                    'allfiltertitle': PROFILE_MIMETYPE_ALL_NAME,
                    'filter': {
                        'name': PROFILE_MIMETYPE_FOLDER_NAME,
                        'mimetypes': ('application/x-directory',)
                        },
                    'entry': self.osincludes
                    },
                True, False
                )
            )

        self.os_includes_clean, self.osincludesclean = ActiveButton(
            class_id = self, text = gtk.STOCK_CLEAR,
            width = 0, height = 0,
            f_1 = CleanEntry, p_1 = (self.osincludes,),
            )

        self.img_includes_entries_box = gtk.HBox(homogeneous, spacing)

        self.img_includes, self.imgincludes = TextEntry(
            class_id = self, indent = False, maxlength = 1024, length = 68,
            text = PROFILE_IMG_INCLUDES_ENTRY, regex = '^.*$'
            )

        self.img_includes_choose, self.imgincludeschoose = ActiveButton(
            class_id = self, text = gtk.STOCK_OPEN,
            width = 0, height = 0,
            f_1 = ThreadGenerator,
            p_1 = (
                UserSelect, {
                    'class_id': self,
                    'title': PROFILE_IMG_INCLUDES_SELECT_TITLE,
                    'action': gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,
                    'allfiltertitle': PROFILE_MIMETYPE_ALL_NAME,
                    'filter': {
                        'name': PROFILE_MIMETYPE_FOLDER_NAME,
                        'mimetypes': ('application/x-directory',)
                        },
                    'entry': self.imgincludes
                    },
                True, False
                )
            )

        self.img_includes_clean, self.imgincludesclean = ActiveButton(
            class_id = self, text = gtk.STOCK_CLEAR,
            width = 0, height = 0,
            f_1 = CleanEntry, p_1 = (self.imgincludes,),
            )

        self.os_hooks_entries_box = gtk.HBox(homogeneous, spacing)

        self.os_hooks, self.oshooks = TextEntry(
            class_id = self, indent = False, maxlength = 1024, length = 68,
            text = PROFILE_OS_HOOKS_ENTRY, regex = '^.*$'
            )

        self.os_hooks_choose, self.oshookschoose = ActiveButton(
            class_id = self, text = gtk.STOCK_OPEN,
            width = 0, height = 0,
            f_1 = ThreadGenerator,
            p_1 = (
                UserSelect, {
                    'class_id': self,
                    'title': PROFILE_OS_HOOKS_SELECT_TITLE,
                    'action': gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,
                    'allfiltertitle': PROFILE_MIMETYPE_ALL_NAME,
                    'filter': {
                        'name': PROFILE_MIMETYPE_FOLDER_NAME,
                        'mimetypes': ('application/x-directory',)
                        },
                    'entry': self.oshooks
                    },
                True, False
                )
            )

        self.os_hooks_clean, self.oshooksclean = ActiveButton(
            class_id = self, text = gtk.STOCK_CLEAR,
            width = 0, height = 0,
            f_1 = CleanEntry, p_1 = (self.oshooks,),
            )

        self.img_hooks_entries_box = gtk.HBox(homogeneous, spacing)

        self.img_hooks, self.imghooks = TextEntry(
            class_id = self, indent = False, maxlength = 1024, length = 68,
            text = PROFILE_IMG_HOOKS_ENTRY, regex = '^.*$'
            )

        self.img_hooks_choose, self.imghookschoose = ActiveButton(
            class_id = self, text = gtk.STOCK_OPEN,
            width = 0, height = 0,
            f_1 = ThreadGenerator,
            p_1 = (
                UserSelect, {
                    'class_id': self,
                    'title': PROFILE_IMG_HOOKS_SELECT_TITLE,
                    'action': gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,
                    'allfiltertitle': PROFILE_MIMETYPE_ALL_NAME,
                    'filter': {
                        'name': PROFILE_MIMETYPE_FOLDER_NAME,
                        'mimetypes': ('application/x-directory',)
                        },
                    'entry': self.imghooks
                    },
                True, False
                )
            )

        self.img_hooks_clean, self.imghooksclean = ActiveButton(
            class_id = self, text = gtk.STOCK_CLEAR,
            width = 0, height = 0,
            f_1 = CleanEntry, p_1 = (self.imghooks,),
            )

        self.img_syslinux_splash_entries_box = gtk.HBox(homogeneous, spacing)

        self.img_syslinux_splash, self.imgsyslinuxsplash = TextEntry(
            class_id = self, indent = False, maxlength = 1024, length = 68,
            text = PROFILE_IMG_SYSLINUX_SPLASH_ENTRY, regex = '^.*$'
            )

        self.img_syslinux_splash_choose, self.imgsyslinuxsplashchoose = ActiveButton(
            class_id = self, text = gtk.STOCK_OPEN,
            width = 0, height = 0,
            f_1 = ThreadGenerator,
            p_1 = (
                UserSelect, {
                    'class_id': self,
                    'title': PROFILE_IMG_SYSLINUX_SPLASH_SELECT_TITLE,
                    'action': gtk.FILE_CHOOSER_ACTION_OPEN,
                    'allfiltertitle': PROFILE_MIMETYPE_ALL_NAME,
                    'filter': {
                        'name': PROFILE_MIMETYPE_PNG_NAME,
                        'mimetypes': ('image/png',)
                        },
                    'entry': self.imgsyslinuxsplash
                    },
                True, False
                )
            )

        self.img_syslinux_splash_clean, self.imgsyslinuxsplashclean = ActiveButton(
            class_id = self, text = gtk.STOCK_CLEAR,
            width = 0, height = 0,
            f_1 = CleanEntry, p_1 = (self.imgsyslinuxsplash,),
            )

        self.img_debian_installer_entries_box = gtk.VBox(homogeneous, spacing)

        self.img_debian_installer_check, self.imgdebianinstallercheck = ActiveCheck(
            class_id = self, text = PROFILE_IMG_DEBIAN_INSTALLER_CHECK,
            active = False,
            )

        self.img_debian_installer_check, self.imgdebianinstallercheck = ActiveCheck(
            class_id = self, text = PROFILE_IMG_DEBIAN_INSTALLER_CHECK,
            active = False,
            f_1 = Toggle, p_1 = (
                self.img_debian_installer_check, self.img_debian_installer_entries_box,
                False, False, False
                ),
            )

        self.img_debian_installer_banner_entries_box = gtk.HBox(homogeneous, spacing)

        self.img_debian_installer_banner, self.imgdebianinstallerbanner = TextEntry(
            class_id = self, indent = False, maxlength = 1024, length = 68,
            text = PROFILE_IMG_DEBIAN_INSTALLER_BANNER_ENTRY, regex = '^.*$'
            )

        self.img_debian_installer_banner_choose, self.imgdebianinstallerbannerchoose = ActiveButton(
            class_id = self, text = gtk.STOCK_OPEN,
            width = 0, height = 0,
            f_1 = ThreadGenerator,
            p_1 = (
                UserSelect, {
                    'class_id': self,
                    'title': PROFILE_IMG_DEBIAN_INSTALLER_BANNER_SELECT_TITLE,
                    'action': gtk.FILE_CHOOSER_ACTION_OPEN,
                    'allfiltertitle': PROFILE_MIMETYPE_ALL_NAME,
                    'filter': {
                        'name': PROFILE_MIMETYPE_PNG_NAME,
                        'mimetypes': ('image/png',)
                        },
                    'entry': self.imgdebianinstallerbanner
                    },
                True, False
                )
            )

        self.img_debian_installer_banner_clean, self.imgdebianinstallerbannerclean = ActiveButton(
            class_id = self, text = gtk.STOCK_CLEAR,
            width = 0, height = 0,
            f_1 = CleanEntry, p_1 = (self.imgdebianinstallerbanner,),
            )

        self.img_debian_installer_preseed_entries_box = gtk.HBox(homogeneous, spacing)

        self.img_debian_installer_preseed, self.imgdebianinstallerpreseed = TextEntry(
            class_id = self, indent = False, maxlength = 1024, length = 68,
            text = PROFILE_IMG_DEBIAN_INSTALLER_PRESEED_ENTRY, regex = '^.*$'
            )

        self.img_debian_installer_preseed_choose, self.imgdebianinstallerpreseedchoose = ActiveButton(
            class_id = self, text = gtk.STOCK_OPEN,
            width = 0, height = 0,
            f_1 = ThreadGenerator,
            p_1 = (
                UserSelect, {
                    'class_id': self,
                    'title': PROFILE_IMG_DEBIAN_INSTALLER_PRESEED_SELECT_TITLE,
                    'action': gtk.FILE_CHOOSER_ACTION_OPEN,
                    'allfiltertitle': PROFILE_MIMETYPE_ALL_NAME,
                    'entry': self.imgdebianinstallerpreseed
                    },
                True, False
                )
            )

        self.img_debian_installer_preseed_clean, self.imgdebianinstallerpreseedclean = ActiveButton(
            class_id = self, text = gtk.STOCK_CLEAR,
            width = 0, height = 0,
            f_1 = CleanEntry, p_1 = (self.imgdebianinstallerpreseed,),
            )

        self.img_debian_installer_gtk_entries_box = gtk.HBox(homogeneous, spacing)

        self.img_debian_installer_gtk, self.imgdebianinstallergtk = TextEntry(
            class_id = self, indent = False, maxlength = 1024, length = 68,
            text = PROFILE_IMG_DEBIAN_INSTALLER_GTK_ENTRY, regex = '^.*$'
            )

        self.img_debian_installer_gtk_choose, self.imgdebianinstallergtkchoose = ActiveButton(
            class_id = self, text = gtk.STOCK_OPEN,
            width = 0, height = 0,
            f_1 = ThreadGenerator,
            p_1 = (
                UserSelect, {
                    'class_id': self,
                    'title': PROFILE_IMG_DEBIAN_INSTALLER_GTK_SELECT_TITLE,
                    'action': gtk.FILE_CHOOSER_ACTION_OPEN,
                    'allfiltertitle': PROFILE_MIMETYPE_ALL_NAME,
                    'entry': self.imgdebianinstallergtk
                    },
                True, False
                )
            )

        self.img_debian_installer_gtk_clean, self.imgdebianinstallergtkclean = ActiveButton(
            class_id = self, text = gtk.STOCK_CLEAR,
            width = 0, height = 0,
            f_1 = CleanEntry, p_1 = (self.imgdebianinstallergtk,),
            )

        self.bottombuttons = BottomButtons(
            class_id = self, width = 80, height = 30,
            fclose = ThreadGenerator,
            pclose = (
                UserMessage, {
                    'message': PROFILE_CONFIRM_CANCEL_MSG % '\n\n',
                    'title': PROFILE_CONFIRM_CANCEL_TITLE,
                    'type': gtk.MESSAGE_QUESTION,
                    'buttons': gtk.BUTTONS_YES_NO,
                    'c_1': gtk.RESPONSE_YES,
                    'f_1': self.window.destroy, 'p_1': '',
                    'c_2': gtk.RESPONSE_YES,
                    'f_2': gtk.main_quit, 'p_2': ''
                    },
                True, False
                ),
            fhelp = ThreadGenerator,
            phelp = (
                ProcessGenerator, {
                    'command': ['/usr/bin/yelp', DOCDIR+'/index.html']
                    },
                True, False
            ),
            fabout = ThreadGenerator,
            pabout = (
                AboutWindow, {
                    'img': GUIDIR+'/images/logo.png', 'name': app_name,
                    'version': app_version, 'url': app_url,
                    'copyright': app_copyright, 'description': app_description,
                    'authorsfile': SHAREDIR+'/AUTHORS',
                    'licensefile': SHAREDIR+'/LICENSE',
                    'translatorsfile': SHAREDIR+'/TRANSLATORS'
                    },
                True, False
                ),
            fback = ThreadGenerator,
            pback = (
                UserMessage, {
                    'message': PROFILE_CONFIRM_CANCEL_MSG % '\n\n',
                    'title': PROFILE_CONFIRM_CANCEL_TITLE,
                    'type': gtk.MESSAGE_QUESTION,
                    'buttons': gtk.BUTTONS_YES_NO,
                    'c_1': gtk.RESPONSE_YES,
                    'f_1': self.window.hide, 'p_1': '',
                    'c_2': gtk.RESPONSE_YES,
                    'f_2': Main, 'p_2': ''
                    },
                True, False
                ),
            fgo = ThreadGenerator,
            pgo = (
                UserMessage, {
                    'message': PROFILE_CONFIRM_OK_MSG % '\n\n',
                    'title': PROFILE_CONFIRM_OK_TITLE,
                    'type': gtk.MESSAGE_QUESTION,
                    'buttons': gtk.BUTTONS_YES_NO,
                    'c_1': gtk.RESPONSE_YES,
                    'f_1': CreateProfile, 'p_1': (
                        self, self.profilename, self.profilearch,
                        self.authorname, self.authoremail, self.authorurl,
                        self.oslocale, self.metadist, self.metacodename,
                        self.metarepo, self.metareposections, self.osextrarepos,
                        self.ospackages, self.imgpoolpackages, self.osincludes,
                        self.imgincludes, self.oshooks, self.imghooks,
                        self.imgsyslinuxsplash, self.imgdebianinstallercheck,
                        self.imgdebianinstallerbanner,
                        self.imgdebianinstallerpreseed,
                        self.imgdebianinstallergtk
                        )
                    },
                True, False
                )
            )

        self.vbox.pack_start(self.profile_name_title, expand, fill, padding)
        self.vbox.pack_start(self.profile_name_description, expand, fill, padding)
        self.vbox.pack_start(self.profile_name, expand, fill, padding)
        self.vbox.pack_start(gtk.HSeparator(), expand, fill, padding)
        self.vbox.pack_start(self.profile_arch_title, expand, fill, padding)
        self.vbox.pack_start(self.profile_arch_description, expand, fill, padding)
        self.vbox.pack_start(self.profile_arch, expand, fill, padding)
        self.vbox.pack_start(gtk.HSeparator(), expand, fill, padding)
        self.vbox.pack_start(self.author_name_title, expand, fill, padding)
        self.vbox.pack_start(self.author_name_description, expand, fill, padding)
        self.vbox.pack_start(self.author_name, expand, fill, padding)
        self.vbox.pack_start(gtk.HSeparator(), expand, fill, padding)
        self.vbox.pack_start(self.author_email_title, expand, fill, padding)
        self.vbox.pack_start(self.author_email_description, expand, fill, padding)
        self.vbox.pack_start(self.author_email, expand, fill, padding)
        self.vbox.pack_start(gtk.HSeparator(), expand, fill, padding)
        self.vbox.pack_start(self.author_url_title, expand, fill, padding)
        self.vbox.pack_start(self.author_url_description, expand, fill, padding)
        self.vbox.pack_start(self.author_url, expand, fill, padding)
        self.vbox.pack_start(gtk.HSeparator(), expand, fill, padding)
        self.vbox.pack_start(self.os_locale_title, expand, fill, padding)
        self.vbox.pack_start(self.os_locale_description, expand, fill, padding)
        self.vbox.pack_start(self.os_locale, expand, fill, padding)
        self.vbox.pack_start(gtk.HSeparator(), expand, fill, padding)
        self.vbox.pack_start(self.meta_dist_title, expand, fill, padding)
        self.vbox.pack_start(self.meta_dist_description, expand, fill, padding)
        self.vbox.pack_start(self.meta_dist, expand, fill, padding)
        self.vbox.pack_start(gtk.HSeparator(), expand, fill, padding)
        self.vbox.pack_start(self.meta_codename_title, expand, fill, padding)
        self.vbox.pack_start(self.meta_codename_description, expand, fill, padding)
        self.vbox.pack_start(self.meta_codename, expand, fill, padding)
        self.vbox.pack_start(gtk.HSeparator(), expand, fill, padding)
        self.vbox.pack_start(self.meta_repo_title, expand, fill, padding)
        self.vbox.pack_start(self.meta_repo_description, expand, fill, padding)
        self.vbox.pack_start(self.meta_repo, expand, fill, padding)
        self.vbox.pack_start(gtk.HSeparator(), expand, fill, padding)
        self.vbox.pack_start(self.meta_reposections_title, expand, fill, padding)
        self.vbox.pack_start(self.meta_reposections_description, expand, fill, padding)
        self.vbox.pack_start(self.meta_reposections, expand, fill, padding)
        self.vbox.pack_start(gtk.HSeparator(), expand, fill, padding)
        self.vbox.pack_start(self.os_extrarepos_check, expand, fill, padding)
        self.vbox.pack_start(self.os_extrarepos, expand, fill, padding)
        self.os_extrarepos_entries_box.pack_start(self.os_extrarepos_url, expand, fill, padding)
        self.os_extrarepos_entries_box.pack_start(self.os_extrarepos_branch, expand, fill, padding)
        self.os_extrarepos_entries_box.pack_start(self.os_extrarepos_sections, expand, fill, padding)
        self.os_extrarepos_entries_box.pack_start(self.os_extrarepos_add, expand, fill, padding)
        self.os_extrarepos_entries_box.pack_start(self.os_extrarepos_clean, expand, fill, padding)
        self.vbox.pack_start(self.os_extrarepos_entries_box, expand, fill, padding)
        self.vbox.pack_start(self.os_extrarepos_description, expand, fill, padding)
        self.vbox.pack_start(gtk.HSeparator(), expand, fill, padding)
        self.vbox.pack_start(self.os_packages_title, expand, fill, padding)
        self.vbox.pack_start(self.os_packages, expand, fill, padding)
        self.os_packages_entries_box.pack_start(self.os_packages_name, expand, fill, padding)
        self.os_packages_entries_box.pack_start(self.os_packages_add, expand, fill, padding)
        self.os_packages_entries_box.pack_start(self.os_packages_clean, expand, fill, padding)
        self.vbox.pack_start(self.os_packages_entries_box, expand, fill, padding)
        self.vbox.pack_start(self.os_packages_description, expand, fill, padding)
        self.vbox.pack_start(gtk.HSeparator(), expand, fill, padding)
        self.vbox.pack_start(self.img_pool_packages_title, expand, fill, padding)
        self.vbox.pack_start(self.img_pool_packages, expand, fill, padding)
        self.img_pool_packages_entries_box.pack_start(self.img_pool_packages_name, expand, fill, padding)
        self.img_pool_packages_entries_box.pack_start(self.img_pool_packages_add, expand, fill, padding)
        self.img_pool_packages_entries_box.pack_start(self.img_pool_packages_clean, expand, fill, padding)
        self.vbox.pack_start(self.img_pool_packages_entries_box, expand, fill, padding)
        self.vbox.pack_start(self.img_pool_packages_description, expand, fill, padding)
        self.vbox.pack_start(gtk.HSeparator(), expand, fill, padding)
        self.vbox.pack_start(self.os_includes_title, expand, fill, padding)
        self.os_includes_entries_box.pack_start(self.os_includes, expand, fill, padding)
        self.os_includes_entries_box.pack_start(self.os_includes_choose, expand, fill, padding)
        self.os_includes_entries_box.pack_start(self.os_includes_clean, expand, fill, padding)
        self.vbox.pack_start(self.os_includes_entries_box, expand, fill, padding)
        self.vbox.pack_start(self.os_includes_description, expand, fill, padding)
        self.vbox.pack_start(gtk.HSeparator(), expand, fill, padding)
        self.vbox.pack_start(self.img_includes_title, expand, fill, padding)
        self.img_includes_entries_box.pack_start(self.img_includes, expand, fill, padding)
        self.img_includes_entries_box.pack_start(self.img_includes_choose, expand, fill, padding)
        self.img_includes_entries_box.pack_start(self.img_includes_clean, expand, fill, padding)
        self.vbox.pack_start(self.img_includes_entries_box, expand, fill, padding)
        self.vbox.pack_start(self.img_includes_description, expand, fill, padding)
        self.vbox.pack_start(gtk.HSeparator(), expand, fill, padding)
        self.vbox.pack_start(self.os_hooks_title, expand, fill, padding)
        self.os_hooks_entries_box.pack_start(self.os_hooks, expand, fill, padding)
        self.os_hooks_entries_box.pack_start(self.os_hooks_choose, expand, fill, padding)
        self.os_hooks_entries_box.pack_start(self.os_hooks_clean, expand, fill, padding)
        self.vbox.pack_start(self.os_hooks_entries_box, expand, fill, padding)
        self.vbox.pack_start(self.os_hooks_description, expand, fill, padding)
        self.vbox.pack_start(gtk.HSeparator(), expand, fill, padding)
        self.vbox.pack_start(self.img_hooks_title, expand, fill, padding)
        self.img_hooks_entries_box.pack_start(self.img_hooks, expand, fill, padding)
        self.img_hooks_entries_box.pack_start(self.img_hooks_choose, expand, fill, padding)
        self.img_hooks_entries_box.pack_start(self.img_hooks_clean, expand, fill, padding)
        self.vbox.pack_start(self.img_hooks_entries_box, expand, fill, padding)
        self.vbox.pack_start(self.img_hooks_description, expand, fill, padding)
        self.vbox.pack_start(gtk.HSeparator(), expand, fill, padding)
        self.vbox.pack_start(self.img_syslinux_splash_title, expand, fill, padding)
        self.img_syslinux_splash_entries_box.pack_start(self.img_syslinux_splash, expand, fill, padding)
        self.img_syslinux_splash_entries_box.pack_start(self.img_syslinux_splash_choose, expand, fill, padding)
        self.img_syslinux_splash_entries_box.pack_start(self.img_syslinux_splash_clean, expand, fill, padding)
        self.vbox.pack_start(self.img_syslinux_splash_entries_box, expand, fill, padding)
        self.vbox.pack_start(self.img_syslinux_splash_description, expand, fill, padding)
        self.vbox.pack_start(gtk.HSeparator(), expand, fill, padding)
        self.vbox.pack_start(self.img_debian_installer_check, expand, fill, padding)
        self.img_debian_installer_entries_box.pack_start(self.img_debian_installer_banner_title, expand, fill, padding)
        self.img_debian_installer_banner_entries_box.pack_start(self.img_debian_installer_banner, expand, fill, padding)
        self.img_debian_installer_banner_entries_box.pack_start(self.img_debian_installer_banner_choose, expand, fill, padding)
        self.img_debian_installer_banner_entries_box.pack_start(self.img_debian_installer_banner_clean, expand, fill, padding)
        self.img_debian_installer_entries_box.pack_start(self.img_debian_installer_banner_entries_box, expand, fill, padding)
        self.img_debian_installer_entries_box.pack_start(self.img_debian_installer_preseed_title, expand, fill, padding)
        self.img_debian_installer_preseed_entries_box.pack_start(self.img_debian_installer_preseed, expand, fill, padding)
        self.img_debian_installer_preseed_entries_box.pack_start(self.img_debian_installer_preseed_choose, expand, fill, padding)
        self.img_debian_installer_preseed_entries_box.pack_start(self.img_debian_installer_preseed_clean, expand, fill, padding)
        self.img_debian_installer_entries_box.pack_start(self.img_debian_installer_preseed_entries_box, expand, fill, padding)
        self.img_debian_installer_entries_box.pack_start(self.img_debian_installer_gtk_title, expand, fill, padding)
        self.img_debian_installer_gtk_entries_box.pack_start(self.img_debian_installer_gtk, expand, fill, padding)
        self.img_debian_installer_gtk_entries_box.pack_start(self.img_debian_installer_gtk_choose, expand, fill, padding)
        self.img_debian_installer_gtk_entries_box.pack_start(self.img_debian_installer_gtk_clean, expand, fill, padding)
        self.img_debian_installer_entries_box.pack_start(self.img_debian_installer_gtk_entries_box, expand, fill, padding)
        self.vbox.pack_start(self.img_debian_installer_entries_box, expand, fill, padding)
        self.vbox.pack_start(self.img_debian_installer_description, expand, fill, padding)

        self.swindow.add_with_viewport(self.vbox)
        self.outbox.add(self.swindow)
        self.outbox.pack_start(self.bottombuttons, expand, fill, padding)

        self.window.add(self.outbox)
        self.window.show_all()

        Toggle(self, self.osextrareposcheck, self.os_extrarepos,
                False, False, False)
        Toggle(self, self.osextrareposcheck, self.os_extrarepos_entries_box,
                False, False, False)
        Toggle(self, None, self.os_includes,
                False, False, False)
        Toggle(self, None, self.os_hooks,
                False, False, False)
        Toggle(self, None, self.img_includes,
                False, False, False)
        Toggle(self, None, self.img_hooks,
                False, False, False)
        Toggle(self, None, self.img_syslinux_splash,
                False, False, False)
        Toggle(self, self.img_debian_installer_check,
                self.img_debian_installer_entries_box, False, False, False)

class Test():
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
            combodefault = self.profiledefault, entry = False
            )

        self.profile_arch, self.profilearch = OptionList(
            class_id = self, indent = True, optionlist = supported_arch
            )

        self.profile_media, self.profilemedia = OptionList(
            class_id = self, indent = True, optionlist = supported_media
            )

        if self.nativearch == 'i686':
            for child in self.profilearch:
                if child.get_label() == 'amd64':
                    child.set_sensitive(False)

        self.bottombuttons = BottomButtons(
            class_id = self, width = 80, height = 30,
            fclose = ThreadGenerator,
            pclose = (
                UserMessage, {
                    'message': BUILD_CONFIRM_CANCEL_MSG,
                    'title': BUILD_CONFIRM_CANCEL_TITLE,
                    'type': gtk.MESSAGE_QUESTION,
                    'buttons': gtk.BUTTONS_YES_NO,
                    'c_1': gtk.RESPONSE_YES,
                    'f_1': self.window.destroy, 'p_1': '',
                    'c_2': gtk.RESPONSE_YES,
                    'f_2': gtk.main_quit, 'p_2': ''
                    },
                True, False
                ),
            fhelp = ThreadGenerator,
            phelp = (
                ProcessGenerator, {
                    'command': ['/usr/bin/yelp', DOCDIR+'/index.html']
                    },
                True, False
            ),
            fabout = ThreadGenerator,
            pabout = (
                AboutWindow, {
                    'img': GUIDIR+'/images/logo.png', 'name': app_name,
                    'version': app_version, 'url': app_url,
                    'copyright': app_copyright, 'description': app_description,
                    'authorsfile': SHAREDIR+'/AUTHORS',
                    'licensefile': SHAREDIR+'/LICENSE',
                    'translatorsfile': SHAREDIR+'/TRANSLATORS'
                    },
                True, False
                ),
            fback = ThreadGenerator,
            pback = (
                UserMessage, {
                    'message': BUILD_CONFIRM_CANCEL_MSG % '\n\n',
                    'title': BUILD_CONFIRM_CANCEL_TITLE,
                    'type': gtk.MESSAGE_QUESTION,
                    'buttons': gtk.BUTTONS_YES_NO,
                    'c_1': gtk.RESPONSE_YES,
                    'f_1': self.window.hide, 'p_1': '',
                    'c_2': gtk.RESPONSE_YES,
                    'f_2': Main, 'p_2': ''
                    },
                True, False
                ),
            fgo = ThreadGenerator,
            pgo = (
                UserMessage, {
                    'message': BUILD_CONFIRM_OK_MSG % '\n\n',
                    'title': BUILD_CONFIRM_OK_TITLE,
                    'type': gtk.MESSAGE_QUESTION,
                    'buttons': gtk.BUTTONS_YES_NO,
                    'c_1': gtk.RESPONSE_YES,
                    'f_1': BuildImage, 'p_1': (
                        self, self.profilename, self.profilearch,
                        self.profilemedia, self.inbox
                        )
                    },
                True, False
                )
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

class Save():
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
            combodefault = self.profiledefault, entry = False
            )

        self.profile_arch, self.profilearch = OptionList(
            class_id = self, indent = True, optionlist = supported_arch
            )

        self.profile_media, self.profilemedia = OptionList(
            class_id = self, indent = True, optionlist = supported_media
            )

        if self.nativearch == 'i686':
            for child in self.profilearch:
                if child.get_label() == 'amd64':
                    child.set_sensitive(False)

        self.bottombuttons = BottomButtons(
            class_id = self, width = 80, height = 30,
            fclose = ThreadGenerator,
            pclose = (
                UserMessage, {
                    'message': BUILD_CONFIRM_CANCEL_MSG,
                    'title': BUILD_CONFIRM_CANCEL_TITLE,
                    'type': gtk.MESSAGE_QUESTION,
                    'buttons': gtk.BUTTONS_YES_NO,
                    'c_1': gtk.RESPONSE_YES,
                    'f_1': self.window.destroy, 'p_1': '',
                    'c_2': gtk.RESPONSE_YES,
                    'f_2': gtk.main_quit, 'p_2': ''
                    },
                True, False
                ),
            fhelp = ThreadGenerator,
            phelp = (
                ProcessGenerator, {
                    'command': ['/usr/bin/yelp', DOCDIR+'/index.html']
                    },
                True, False
            ),
            fabout = ThreadGenerator,
            pabout = (
                AboutWindow, {
                    'img': GUIDIR+'/images/logo.png', 'name': app_name,
                    'version': app_version, 'url': app_url,
                    'copyright': app_copyright, 'description': app_description,
                    'authorsfile': SHAREDIR+'/AUTHORS',
                    'licensefile': SHAREDIR+'/LICENSE',
                    'translatorsfile': SHAREDIR+'/TRANSLATORS'
                    },
                True, False
                ),
            fback = ThreadGenerator,
            pback = (
                UserMessage, {
                    'message': BUILD_CONFIRM_CANCEL_MSG % '\n\n',
                    'title': BUILD_CONFIRM_CANCEL_TITLE,
                    'type': gtk.MESSAGE_QUESTION,
                    'buttons': gtk.BUTTONS_YES_NO,
                    'c_1': gtk.RESPONSE_YES,
                    'f_1': self.window.hide, 'p_1': '',
                    'c_2': gtk.RESPONSE_YES,
                    'f_2': Main, 'p_2': ''
                    },
                True, False
                ),
            fgo = ThreadGenerator,
            pgo = (
                UserMessage, {
                    'message': BUILD_CONFIRM_OK_MSG % '\n\n',
                    'title': BUILD_CONFIRM_OK_TITLE,
                    'type': gtk.MESSAGE_QUESTION,
                    'buttons': gtk.BUTTONS_YES_NO,
                    'c_1': gtk.RESPONSE_YES,
                    'f_1': BuildImage, 'p_1': (
                        self, self.profilename, self.profilearch,
                        self.profilemedia, self.inbox
                        )
                    },
                True, False
                )
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
