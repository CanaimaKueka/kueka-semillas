#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ==============================================================================
# PAQUETE: canaima-semilla
# ARCHIVO: scripts/c-s.sh
# DESCRIPCIÓN: Script principal. Se encarga de invocar a los demás módulos y
#              funciones según los parámetros proporcionados.
# USO: ./c-s.sh [MÓDULO] [PARÁMETROS] [...]
# COPYRIGHT:
#       (C) 2010-2012 Luis Alejandro Martínez Faneyth <luis@huntingbears.com.ve>
#       (C) 2012 Niv Sardi <xaiki@debian.org>
# LICENCIA: GPL-3
# ==============================================================================
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# COPYING file for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# CODE IS POETRY

# Librerías Globales
import gtk, sys

# Librerías Locales
from canaimasemilla.translator import *
from canaimasemilla.config import *
from canaimasemilla.constructor import *
from canaimasemilla.processor import *

class Main():
    def __init__(self):
        # Creating Window
        self.window, self.outbox , self.inbox = WindowContainer(
            c = self, title = MAIN_TITLE, outpad = 0, inpad = 10,
            spacing = 0
            )

        # Creating Objects
        self.banner = Banner(
            c = self, box = self.outbox, image = BANNER_IMAGE
            )

        self.row_1 = CustomBox(
            c = self, box = self.inbox, align = 'horizontal'
            )

        self.row_2 = CustomBox(
            c = self, box = self.inbox, align = 'horizontal'
            )

        self.create_profile = IconButton(
            c = self, box = self.row_1, icon = PROFILE_ICON,
            text_1 = MAIN_CREATE_PROFILE_TITLE, text_2 = MAIN_CREATE_PROFILE_TEXT,
            width = 330, height = 180, margin = 5, f_1 = ThreadGenerator,
            p_1 = (Profile, {}, True, self.window)
            )

        self.build_image = IconButton(
            c = self, box = self.row_1, icon = BUILD_ICON,
            text_1 = MAIN_BUILD_IMAGE_TITLE, text_2 = MAIN_BUILD_IMAGE_TEXT,
            width = 330, height = 180, margin = 5, f_1 = ThreadGenerator,
            p_1 = (Build, {}, True, self.window)
            )

        self.test_image = IconButton(
            c = self, box = self.row_2, icon = TEST_ICON,
            text_1 = MAIN_TEST_IMAGE_TITLE, text_2 = MAIN_TEST_IMAGE_TEXT,
            width = 330, height = 180, margin = 5, f_1 = ThreadGenerator,
            p_1 = (Test, {}, True, self.window)
            )

        self.save_image = IconButton(
            c = self, box = self.row_2, icon = SAVE_ICON,
            text_1 = MAIN_SAVE_IMAGE_TITLE, text_2 = MAIN_SAVE_IMAGE_TEXT,
            width = 330, height = 180, margin = 5, f_1 = ThreadGenerator,
            p_1 = (Save, {}, True, self.window)
            )

        self.outbox.pack_start(self.inbox, False, False, 0)

        self.bottom_buttons = BottomButtons(
            c = self, box = self.outbox, width = 80, height = 30,
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
                    'img': ABOUT_IMAGE, 'name': app_name,
                    'version': app_version, 'url': app_url,
                    'copyright': app_copyright, 'description': app_description,
                    'authorsfile': AUTHORS_FILE, 'licensefile': LICENCE_FILE,
                    'translatorsfile': TRANSLATORS_FILE
                    },
                True, False
                )
            )

        # Showing
        self.window.add(self.outbox)
        self.window.show_all()

class Build():
    def __init__(self):
        # Creating Window
        self.window, self.outbox , self.inbox = WindowContainer(
            c = self, title = BUILD_TITLE, outpad = 0, inpad = 10,
            spacing = 10
            )

        # Creating Objects
        self.profile_list, self.profile_default = ProfileList(
            c = self, profiledir = PROFILEDIR
            )

        self.native_arch = GetArch()

        self.banner = Banner(
            c = self, box = self.outbox, image = BANNER_IMAGE
            )

        self.profile_name_title = Title(
            c = self, box = self.inbox, text = BUILD_PROFILE_NAME_1
            )

        self.profile_name = Combo(
            c = self, box = self.inbox, combolist = self.profile_list,
            combodefault = self.profile_default, entry = False
            )

        self.profile_name_description = Description(
            c = self, box = self.inbox, text = BUILD_PROFILE_NAME_2
            )

        self.custom_separator_1 = CustomSeparator(
            c = self, box = self.inbox, align = 'horizontal'
            )

        self.profile_arch_title = Title(
            c = self, box = self.inbox, text = BUILD_PROFILE_ARCH_1
            )

        self.profile_arch = OptionList(
            c = self, box = self.inbox, optionlist = supported_arch
            )

        self.profile_arch_description = Description(
            c = self, box = self.inbox, text = BUILD_PROFILE_ARCH_2
            )

        self.custom_separator_2 = CustomSeparator(
            c = self, box = self.inbox, align = 'horizontal'
            )

        self.profile_media_title = Title(
            c = self, box = self.inbox, text = BUILD_PROFILE_MEDIA_1
            )

        self.profile_media = OptionList(
            c = self, box = self.inbox, optionlist = supported_media
            )

        self.profile_media_description = Description(
            c = self, box = self.inbox, text = BUILD_PROFILE_MEDIA_2
            )

        self.outbox.pack_start(self.inbox, False, False, 0)
        self.outbox.pack_start(gtk.HBox(), False, False, 25)

        self.bottom_buttons = BottomButtons(
            c = self, box = self.outbox, width = 80, height = 30,
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
                    'img': ABOUT_IMAGE, 'name': app_name,
                    'version': app_version, 'url': app_url,
                    'copyright': app_copyright, 'description': app_description,
                    'authorsfile': AUTHORS_FILE, 'licensefile': LICENCE_FILE,
                    'translatorsfile': TRANSLATORS_FILE
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
                        self, self.profile_name, self.profile_arch,
                        self.profile_media, self.inbox
                        )
                    },
                True, False
                )
            )

        if self.native_arch == 'i686':
            for child in self.profile_arch:
                if child.get_label() == 'amd64':
                    child.set_sensitive(False)

        # Showing
        self.window.add(self.outbox)
        self.window.show_all()

class Profile():
    def __init__(self):
        # Creating Window
        self.window, self.outbox , self.inbox = WindowContainer(
            c = self, title = BUILD_TITLE, outpad = 0, inpad = 10,
            spacing = 10
            )

        self.locale_list, self.locale_active = LocaleList(
            c = self, supported = supported_locales,
            current = os.environ['LC_ALL']
            )

        self.native_arch = GetArch()

        self.banner = Banner(
            c = self, box = self.outbox, image = BANNER_IMAGE
            )

        self.id_tab, self.distro_tab, self.extrarepos_tab, \
        self.packages_tab, self.includes_tab, self.installer_tab = TabbedBox(
            c = self, box = self.inbox, pos = gtk.POS_TOP, tabs = [
                PROFILE_ID_TAB, PROFILE_DISTRO_TAB, PROFILE_EXTRAREPOS_TAB,
                PROFILE_PACKAGES_TAB, PROFILE_INCLUDES_TAB, PROFILE_INSTALLER_TAB
                ]
            )

        self.profile_name_title = Title(
            c = self, box = self.id_tab, text = PROFILE_PROFILE_NAME_1
            )

        self.profile_name = TextEntry(
            c = self, box = self.id_tab, maxlength = 18, length = 18,
            text = default_profile_name, regex = '^[a-z-]*$'
            )

        self.profile_name_description = Description(
            c = self, box = self.id_tab, text = PROFILE_PROFILE_NAME_2
            )
        self.profile_arch = ''
#        self.custom_separator_1 = CustomSeparator(
#            c = self, box = self.id_tab, align = 'horizontal'
#            )

#        self.profile_arch_title = Title(
#            c = self, box = self.id_tab, text = PROFILE_PROFILE_ARCH_1
#            )

#        self.profile_arch = CheckList(
#            c = self, box = self.id_tab, checklist = supported_arch,
#            checkdefault = ''
#            )

#        self.profile_arch_description = Description(
#            c = self, box = self.id_tab, text = PROFILE_PROFILE_ARCH_2
#            )

        self.custom_separator_2 = CustomSeparator(
            c = self, box = self.id_tab, align = 'horizontal'
            )

        self.author_name_title = Title(
            c = self, box = self.id_tab, text = PROFILE_AUTHOR_NAME_1
            )

        self.author_name = TextEntry(
            c = self, box = self.id_tab, maxlength = 60, length = 60,
            text = default_profile_author, regex = '\w'
            )

        self.author_name_description = Description(
            c = self, box = self.id_tab, text = PROFILE_AUTHOR_NAME_2
            )

        self.custom_separator_3 = CustomSeparator(
            c = self, box = self.id_tab, align = 'horizontal'
            )

        self.author_email_title = Title(
            c = self, box = self.id_tab, text = PROFILE_AUTHOR_EMAIL_1
            )

        self.author_email = TextEntry(
            c = self, box = self.id_tab, maxlength = 60, length = 60,
            text = default_profile_email, regex = '^[_.@0-9A-Za-z-]*$'
            )

        self.author_email_description = Description(
            c = self, box = self.id_tab, text = PROFILE_AUTHOR_EMAIL_2
            )

        self.custom_separator_4 = CustomSeparator(
            c = self, box = self.id_tab, align = 'horizontal'
            )

        self.author_url_title = Title(
            c = self, box = self.id_tab, text = PROFILE_AUTHOR_URL_1
            )

        self.author_url = TextEntry(
            c = self, box = self.id_tab, maxlength = 60, length = 60,
            text = default_profile_url, regex = '^[-A-Za-z0-9+&@#/%?=~_()|!:,.;]*$'
            )

        self.author_url_description = Description(
            c = self, box = self.id_tab, text = PROFILE_AUTHOR_URL_2
            )

        self.custom_separator_5 = CustomSeparator(
            c = self, box = self.id_tab, align = 'horizontal'
            )
        self.os_locale = ''
#        self.os_locale_title = Title(
#            c = self, box = self.id_tab, text = PROFILE_OS_LOCALE_1
#            )

#        self.os_locale = Combo(
#            c = self, box = self.id_tab, combolist = self.locale_list,
#            combodefault = self.locale_active, entry = False
#            )

#        self.os_locale_description = Description(
#            c = self, box = self.id_tab, text = PROFILE_OS_LOCALE_2
#            )

#        self.custom_separator_6 = CustomSeparator(
#            c = self, box = self.id_tab, align = 'horizontal'
#            )

        self.meta_dist_title = Title(
            c = self, box = self.distro_tab, text = PROFILE_META_DIST_1
            )

        self.meta_dist_box = CustomBox(
            c = self, box = self.distro_tab, align = 'horizontal'
            )

        self.meta_dist_description = Description(
            c = self, box = self.distro_tab, text = PROFILE_META_DIST_2
            )

        self.custom_separator_7 = CustomSeparator(
            c = self, box = self.distro_tab, align = 'horizontal'
            )

        self.meta_codename_title = Title(
            c = self, box = self.distro_tab, text = PROFILE_META_CODENAME_1
            )

        self.meta_dist = gtk.combo_box_new_text()
        self.meta_dist.append_text('canaima')
        self.meta_dist.set_active(0)

        self.codename_list, self.codename_active = CodenameList(
            c = self, dist = self.meta_dist, db = apt_templates
            )

        self.meta_codename = Combo(
            c = self, box = self.distro_tab, combolist = self.codename_list,
            combodefault = self.codename_active, entry = True
            )

        self.meta_codename_description = Description(
            c = self, box = self.distro_tab, text = PROFILE_META_CODENAME_2
            )

        self.custom_separator_8 = CustomSeparator(
            c = self, box = self.distro_tab, align = 'horizontal'
            )

        self.meta_repo_title = Title(
            c = self, box = self.distro_tab, text = PROFILE_META_REPO_1
            )

        self.meta_repo = TextEntry(
            c = self, box = self.distro_tab, maxlength = 60, length = 60,
            text = canaima_repo, regex = '^[-A-Za-z0-9+&@#/%?=~_()|!:,.;]*$'
            )

        self.meta_repo_description = Description(
            c = self, box = self.distro_tab, text = PROFILE_META_REPO_2
            )

        self.custom_separator_9 = CustomSeparator(
            c = self, box = self.distro_tab, align = 'horizontal'
            )

        self.meta_reposections_title = Title(
            c = self, box = self.distro_tab, text = PROFILE_META_REPOSECTIONS_1
            )

        self.section_list = SectionList(c = self, dist = self.meta_dist)

        self.meta_reposections = CheckList(
            c = self, box = self.distro_tab, checklist = self.section_list,
            checkdefault = 'main'
            )

        self.meta_dist, = Combo(
            c = self, box = self.meta_dist_box, combolist = cs_distros,
            combodefault = 2, entry = False,
            f_1 = ChangeCodename,
            p_1 = (self, self.meta_codename, apt_templates),
            f_2 = ChangeRepo,
            p_2 = (self, self.meta_repo),
            f_3 = ChangeSections,
            p_3 = (self, self.meta_reposections)
            )

        self.meta_reposections_description = Description(
            c = self, box = self.distro_tab, text = PROFILE_META_REPOSECTIONS_2
            )

        self.os_extrarepos_box_1 = CustomBox(
            c = self, box = self.extrarepos_tab, align = 'horizontal'
            )

        self.os_extrarepos_box_2 = CustomBox(
            c = self, box = self.extrarepos_tab, align = 'horizontal'
            )

        self.os_extrarepos_check = ActiveCheck(
            c = self, box = self.extrarepos_tab,
            text = PROFILE_OS_EXTRAREPOS_CHECK, active = False,
            f_1 = Toggle, p_1 = (self.os_extrarepos_box_1,),
            f_2 = Toggle, p_2 = (self.os_extrarepos_box_2,)
            )

        self.os_extrarepos = ScrolledFrame(
            c = self, box = self.os_extrarepos_box_1
            )

        self.os_extrarepos_url = TextEntry(
            c = self, box = self.os_extrarepos_box_2,
            maxlength = 60, length = 38, text = PROFILE_OS_EXTRAREPOS_URL,
            regex = '^[-A-Za-z0-9+&@#/%?=~_()|!:,.;]*$'
            )

        self.os_extrarepos_branch = TextEntry(
            c = self, box = self.os_extrarepos_box_2,
            maxlength = 60, length = 10, text = PROFILE_OS_EXTRAREPOS_BRANCH,
            regex = '^[A-Za-z0-9-]*$'
            )

        self.os_extrarepos_sections = TextEntry(
            c = self, box = self.os_extrarepos_box_2,
            maxlength = 60, length = 17, text = PROFILE_OS_EXTRAREPOS_SECTIONS,
            regex = '^[A-Za-z0-9\ -]*$'
            )

        self.os_extrarepos_add = ActiveButton(
            c = self, box = self.os_extrarepos_box_2, text = gtk.STOCK_ADD,
            width = 0, height = 0, f_1 = ThreadGenerator, p_1 = (
                AddExtraRepos, {
                    'c': self,
                    'url_entry': self.os_extrarepos_url,
                    'branch_entry': self.os_extrarepos_branch,
                    'sections_entry': self.os_extrarepos_sections,
                    'arch_container': self.profile_arch,
                    'repolistframe': self.os_extrarepos,
                    },
                False, False
                )
            )

        self.os_extrarepos_clean = ActiveButton(
            c = self, box = self.os_extrarepos_box_2, text = gtk.STOCK_CLEAR,
            width = 0, height = 0, f_1 = CleanEntry, p_1 = (self.os_extrarepos,)
            )

        self.os_extrarepos_description = Description(
            c = self, box = self.extrarepos_tab, text = PROFILE_OS_EXTRAREPOS_2
            )

        self.os_packages_title = Title(
            c = self, box = self.packages_tab, text = PROFILE_OS_PACKAGES_1
            )

        self.os_packages_box_1 = CustomBox(
            c = self, box = self.packages_tab, align = 'horizontal'
            )

        self.os_packages_box_2 = CustomBox(
            c = self, box = self.packages_tab, align = 'horizontal'
            )

        self.os_packages = ScrolledFrame(
            c = self, box = self.os_packages_box_1
            )

        self.os_packages_name = TextEntry(
            c = self, box = self.os_packages_box_2,
            maxlength = 60, length = 68, text = PROFILE_OS_PACKAGES_ENTRY,
            regex = '^[A-Za-z0-9\ -]*$'
            )

        self.os_packages_add = ActiveButton(
            c = self, box = self.os_packages_box_2, text = gtk.STOCK_ADD,
            width = 0, height = 0, f_1 = ThreadGenerator, p_1 = (
                AddPackages, {
                    'c': self,
                    'url_entry': self.meta_repo,
                    'branch_entry': self.meta_codename,
                    'section_container': self.meta_reposections,
                    'arch_container': self.profile_arch,
                    'extrareposframe': self.os_extrarepos,
                    'packages_entry': self.os_packages_name,
                    'packageslistframe': self.os_packages,
                    },
                False, False
                )
            )

        self.os_packages_clean = ActiveButton(
            c = self, box = self.os_packages_box_2, text = gtk.STOCK_CLEAR,
            width = 0, height = 0, f_1 = CleanEntry, p_1 = (self.os_packages,),
            )

        self.os_packages_description = Description(
            c = self, box = self.packages_tab, text = PROFILE_OS_PACKAGES_2
            )

        self.custom_separator_12 = CustomSeparator(
            c = self, box = self.packages_tab, align = 'horizontal'
            )

        self.img_pool_packages_title = Title(
            c = self, box = self.packages_tab, text = PROFILE_IMG_POOL_PACKAGES_1
            )

        self.img_pool_packages_box_1 = CustomBox(
            c = self, box = self.packages_tab, align = 'horizontal'
            )

        self.img_pool_packages_box_2 = CustomBox(
            c = self, box = self.packages_tab, align = 'horizontal'
            )

        self.img_pool_packages = ScrolledFrame(
            c = self, box = self.img_pool_packages_box_1
            )

        self.img_pool_packages_name = TextEntry(
            c = self, box = self.img_pool_packages_box_2,
            maxlength = 1024, length = 68,
            text = PROFILE_IMG_POOL_PACKAGES_ENTRY, regex = '^[A-Za-z0-9\ -]*$'
            )

        self.img_pool_packages_add = ActiveButton(
            c = self, box = self.img_pool_packages_box_2, text = gtk.STOCK_ADD,
            width = 0, height = 0,f_1 = ThreadGenerator, p_1 = (
                AddPackages, {
                    'c': self,
                    'url_entry': self.meta_repo,
                    'branch_entry': self.meta_codename,
                    'section_container': self.meta_reposections,
                    'arch_container': self.profile_arch,
                    'extrareposframe': self.os_extrarepos,
                    'packages_entry': self.img_pool_packages_name,
                    'packageslistframe': self.img_pool_packages,
                    },
                False, False
                )
            )

        self.img_pool_packages_clean = ActiveButton(
            c = self, box = self.img_pool_packages_box_2, text = gtk.STOCK_CLEAR,
            width = 0, height = 0, f_1 = CleanEntry, p_1 = (self.img_pool_packages,),
            )

        self.img_pool_packages_description = Description(
            c = self, box = self.packages_tab, text = PROFILE_IMG_POOL_PACKAGES_2
            )

        self.os_includes_title = Title(
            c = self, box = self.includes_tab, text = PROFILE_OS_INCLUDES_1
            )

        self.os_includes_box = CustomBox(
            c = self, box = self.includes_tab, align = 'horizontal'
            )

        self.os_includes = TextEntry(
            c = self, box = self.os_includes_box, maxlength = 1024, length = 68,
            text = PROFILE_OS_INCLUDES_ENTRY, regex = '^.*$'
            )

        self.os_includes_choose = ActiveButton(
            c = self, box = self.os_includes_box, text = gtk.STOCK_OPEN,
            width = 0, height = 0, f_1 = ThreadGenerator, p_1 = (
                UserSelect, {
                    'c': self,
                    'title': PROFILE_OS_INCLUDES_SELECT_TITLE,
                    'action': gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,
                    'allfiltertitle': PROFILE_MIMETYPE_ALL_NAME,
                    'filter': {
                        'name': PROFILE_MIMETYPE_FOLDER_NAME,
                        'mimetypes': ('application/x-directory',)
                        },
                    'entry': self.os_includes
                    },
                True, False
                )
            )

        self.os_includes_clean = ActiveButton(
            c = self, box = self.os_includes_box, text = gtk.STOCK_CLEAR,
            width = 0, height = 0, f_1 = CleanEntry, p_1 = (self.os_includes,),
            )

        self.os_includes_description = Description(
            c = self, box = self.includes_tab, text = PROFILE_OS_INCLUDES_2
            )

        self.custom_separator_14 = CustomSeparator(
            c = self, box = self.includes_tab, align = 'horizontal'
            )

        self.img_includes_title = Title(
            c = self, box = self.includes_tab, text = PROFILE_IMG_INCLUDES_1
            )

        self.img_includes_box = CustomBox(
            c = self, box = self.includes_tab, align = 'horizontal'
            )

        self.img_includes = TextEntry(
            c = self, box = self.img_includes_box, maxlength = 1024, length = 68,
            text = PROFILE_IMG_INCLUDES_ENTRY, regex = '^.*$'
            )

        self.img_includes_choose = ActiveButton(
            c = self, box = self.img_includes_box, text = gtk.STOCK_OPEN,
            width = 0, height = 0, f_1 = ThreadGenerator, p_1 = (
                UserSelect, {
                    'c': self,
                    'title': PROFILE_IMG_INCLUDES_SELECT_TITLE,
                    'action': gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,
                    'allfiltertitle': PROFILE_MIMETYPE_ALL_NAME,
                    'filter': {
                        'name': PROFILE_MIMETYPE_FOLDER_NAME,
                        'mimetypes': ('application/x-directory',)
                        },
                    'entry': self.img_includes
                    },
                True, False
                )
            )

        self.img_includes_clean = ActiveButton(
            c = self, box = self.img_includes_box, text = gtk.STOCK_CLEAR,
            width = 0, height = 0, f_1 = CleanEntry, p_1 = (self.img_includes,),
            )

        self.img_includes_description = Description(
            c = self, box = self.includes_tab, text = PROFILE_IMG_INCLUDES_2
            )

        self.custom_separator_15 = CustomSeparator(
            c = self, box = self.includes_tab, align = 'horizontal'
            )

        self.os_hooks_title = Title(
            c = self, box = self.includes_tab, text = PROFILE_OS_HOOKS_1
            )

        self.os_hooks_box = CustomBox(
            c = self, box = self.includes_tab, align = 'horizontal'
            )

        self.os_hooks = TextEntry(
            c = self, box = self.os_hooks_box, maxlength = 1024, length = 68,
            text = PROFILE_OS_HOOKS_ENTRY, regex = '^.*$'
            )

        self.os_hooks_choose = ActiveButton(
            c = self, box = self.os_hooks_box, text = gtk.STOCK_OPEN,
            width = 0, height = 0, f_1 = ThreadGenerator, p_1 = (
                UserSelect, {
                    'c': self,
                    'title': PROFILE_OS_HOOKS_SELECT_TITLE,
                    'action': gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,
                    'allfiltertitle': PROFILE_MIMETYPE_ALL_NAME,
                    'filter': {
                        'name': PROFILE_MIMETYPE_FOLDER_NAME,
                        'mimetypes': ('application/x-directory',)
                        },
                    'entry': self.os_hooks
                    },
                True, False
                )
            )

        self.os_hooks_clean = ActiveButton(
            c = self, box = self.os_hooks_box, text = gtk.STOCK_CLEAR,
            width = 0, height = 0, f_1 = CleanEntry, p_1 = (self.os_hooks,),
            )

        self.os_hooks_description = Description(
            c = self, box = self.includes_tab, text = PROFILE_OS_HOOKS_2
            )

        self.custom_separator_16 = CustomSeparator(
            c = self, box = self.includes_tab, align = 'horizontal'
            )

        self.img_hooks_title = Title(
            c = self, box = self.includes_tab, text = PROFILE_IMG_HOOKS_1
            )

        self.img_hooks_box = CustomBox(
            c = self, box = self.includes_tab, align = 'horizontal'
            )

        self.img_hooks = TextEntry(
            c = self, box = self.img_hooks_box, maxlength = 1024, length = 68,
            text = PROFILE_IMG_HOOKS_ENTRY, regex = '^.*$'
            )

        self.img_hooks_choose = ActiveButton(
            c = self, box = self.img_hooks_box, text = gtk.STOCK_OPEN,
            width = 0, height = 0, f_1 = ThreadGenerator, p_1 = (
                UserSelect, {
                    'c': self,
                    'title': PROFILE_IMG_HOOKS_SELECT_TITLE,
                    'action': gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,
                    'allfiltertitle': PROFILE_MIMETYPE_ALL_NAME,
                    'filter': {
                        'name': PROFILE_MIMETYPE_FOLDER_NAME,
                        'mimetypes': ('application/x-directory',)
                        },
                    'entry': self.img_hooks
                    },
                True, False
                )
            )

        self.img_hooks_clean = ActiveButton(
            c = self, box = self.img_hooks_box, text = gtk.STOCK_CLEAR,
            width = 0, height = 0, f_1 = CleanEntry, p_1 = (self.img_hooks,),
            )

        self.img_hooks_description = Description(
            c = self, box = self.includes_tab, text = PROFILE_IMG_HOOKS_2
            )

#        self.img_syslinux_splash_title = Title(
#            c = self, box = self.includes_tab, text = PROFILE_IMG_SYSLINUX_SPLASH_1
#            )
        self.img_syslinux_splash = ''
#        self.img_syslinux_splash_box = CustomBox(
#            c = self, box = self.includes_tab, align = 'horizontal'
#            )

#        self.img_syslinux_splash = TextEntry(
#            c = self, box = self.img_syslinux_splash_box, maxlength = 1024,
#            length = 68, text = PROFILE_IMG_SYSLINUX_SPLASH_ENTRY, regex = '^.*$'
#            )

#        self.img_syslinux_splash_choose = ActiveButton(
#            c = self, box = self.img_syslinux_splash_box, text = gtk.STOCK_OPEN,
#            width = 0, height = 0, f_1 = ThreadGenerator, p_1 = (
#                UserSelect, {
#                    'c': self,
#                    'title': PROFILE_IMG_SYSLINUX_SPLASH_SELECT_TITLE,
#                    'action': gtk.FILE_CHOOSER_ACTION_OPEN,
#                    'allfiltertitle': PROFILE_MIMETYPE_ALL_NAME,
#                    'filter': {
#                        'name': PROFILE_MIMETYPE_PNG_NAME,
#                        'mimetypes': ('image/png',)
#                        },
#                    'entry': self.img_syslinux_splash
#                    },
#                True, False
#                )
#            )

#        self.img_syslinux_splash_clean = ActiveButton(
#            c = self, box = self.img_syslinux_splash_box, text = gtk.STOCK_CLEAR,
#            width = 0, height = 0, f_1 = CleanEntry,
#            p_1 = (self.img_syslinux_splash,)
#            )

#        self.img_syslinux_splash_description = Description(
#            c = self, box = self.includes_tab, text = PROFILE_IMG_SYSLINUX_SPLASH_2
#            )

        self.img_debian_installer_box = gtk.VBox()

        self.img_debian_installer_check = ActiveCheck(
            c = self, box = self.installer_tab,
            text = PROFILE_IMG_DEBIAN_INSTALLER_CHECK, active = False,
            f_1 = Toggle, p_1 = (
                False, self.img_debian_installer_box, False, False, False
                ),
            )

        self.img_debian_installer_box = CustomBox(
            c = self, box = self.installer_tab, align = 'vertical'
            )

        self.img_debian_installer_banner_title = Title(
            c = self, box = self.img_debian_installer_box,
            text = PROFILE_IMG_DEBIAN_INSTALLER_BANNER_1
            )

        self.img_debian_installer_banner_box = CustomBox(
            c = self, box = self.img_debian_installer_box, align = 'horizontal'
            )

        self.img_debian_installer_banner = TextEntry(
            c = self, box = self.img_debian_installer_banner_box, maxlength = 1024,
            length = 68, text = PROFILE_IMG_DEBIAN_INSTALLER_BANNER_ENTRY,
            regex = '^.*$'
            )

        self.img_debian_installer_banner_choose = ActiveButton(
            c = self, box = self.img_debian_installer_banner_box, text = gtk.STOCK_OPEN,
            width = 0, height = 0,
            f_1 = ThreadGenerator,
            p_1 = (
                UserSelect, {
                    'c': self,
                    'title': PROFILE_IMG_DEBIAN_INSTALLER_BANNER_SELECT_TITLE,
                    'action': gtk.FILE_CHOOSER_ACTION_OPEN,
                    'allfiltertitle': PROFILE_MIMETYPE_ALL_NAME,
                    'filter': {
                        'name': PROFILE_MIMETYPE_PNG_NAME,
                        'mimetypes': ('image/png',)
                        },
                    'entry': self.img_debian_installer_banner
                    },
                True, False
                )
            )

        self.img_debian_installer_banner_clean = ActiveButton(
            c = self, box = self.img_debian_installer_banner_box, text = gtk.STOCK_CLEAR,
            width = 0, height = 0,
            f_1 = CleanEntry, p_1 = (self.img_debian_installer_banner,),
            )

        self.img_debian_installer_preseed_title = Title(
            c = self, box = self.img_debian_installer_box, text = PROFILE_IMG_DEBIAN_INSTALLER_PRESEED_1
            )

        self.img_debian_installer_preseed_box = CustomBox(
            c = self, box = self.img_debian_installer_box, align = 'horizontal'
            )

        self.img_debian_installer_preseed = TextEntry(
            c = self, box = self.img_debian_installer_preseed_box, maxlength = 1024, length = 68,
            text = PROFILE_IMG_DEBIAN_INSTALLER_PRESEED_ENTRY, regex = '^.*$'
            )

        self.img_debian_installer_preseed_choose = ActiveButton(
            c = self, box = self.img_debian_installer_preseed_box, text = gtk.STOCK_OPEN,
            width = 0, height = 0,
            f_1 = ThreadGenerator,
            p_1 = (
                UserSelect, {
                    'c': self,
                    'title': PROFILE_IMG_DEBIAN_INSTALLER_PRESEED_SELECT_TITLE,
                    'action': gtk.FILE_CHOOSER_ACTION_OPEN,
                    'allfiltertitle': PROFILE_MIMETYPE_ALL_NAME,
                    'entry': self.img_debian_installer_preseed
                    },
                True, False
                )
            )

        self.img_debian_installer_preseed_clean = ActiveButton(
            c = self, box = self.img_debian_installer_preseed_box, text = gtk.STOCK_CLEAR,
            width = 0, height = 0,
            f_1 = CleanEntry, p_1 = (self.img_debian_installer_preseed,),
            )

        self.img_debian_installer_gtk_title = Title(
            c = self, box = self.img_debian_installer_box, text = PROFILE_IMG_DEBIAN_INSTALLER_GTK_1
            )

        self.img_debian_installer_gtk_box = CustomBox(
            c = self, box = self.img_debian_installer_box, align = 'horizontal'
            )

        self.img_debian_installer_gtk = TextEntry(
            c = self, box = self.img_debian_installer_gtk_box, maxlength = 1024, length = 68,
            text = PROFILE_IMG_DEBIAN_INSTALLER_GTK_ENTRY, regex = '^.*$'
            )

        self.img_debian_installer_gtk_choose = ActiveButton(
            c = self, box = self.img_debian_installer_gtk_box, text = gtk.STOCK_OPEN,
            width = 0, height = 0,
            f_1 = ThreadGenerator,
            p_1 = (
                UserSelect, {
                    'c': self,
                    'title': PROFILE_IMG_DEBIAN_INSTALLER_GTK_SELECT_TITLE,
                    'action': gtk.FILE_CHOOSER_ACTION_OPEN,
                    'allfiltertitle': PROFILE_MIMETYPE_ALL_NAME,
                    'entry': self.img_debian_installer_gtk
                    },
                True, False
                )
            )

        self.img_debian_installer_gtk_clean = ActiveButton(
            c = self, box = self.img_debian_installer_gtk_box, text = gtk.STOCK_CLEAR,
            width = 0, height = 0,
            f_1 = CleanEntry, p_1 = (self.img_debian_installer_gtk,),
            )

        self.img_debian_installer_description = Description(
            c = self, box = self.installer_tab,
            text = PROFILE_IMG_DEBIAN_INSTALLER_2
            )

        self.outbox.pack_start(self.inbox, False, False, 0)

        self.bottom_buttons = BottomButtons(
            c = self, box = self.outbox, width = 80, height = 30,
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
                    'img': ABOUT_IMAGE, 'name': app_name,
                    'version': app_version, 'url': app_url,
                    'copyright': app_copyright, 'description': app_description,
                    'authorsfile': AUTHORS_FILE, 'licensefile': LICENCE_FILE,
                    'translatorsfile': TRANSLATORS_FILE
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
                        self, self.profile_name, self.profile_arch,
                        self.author_name, self.author_email, self.author_url,
                        self.os_locale, self.meta_dist, self.meta_codename,
                        self.meta_repo, self.meta_reposections, self.os_extrarepos,
                        self.os_packages, self.img_pool_packages, self.os_includes,
                        self.img_includes, self.os_hooks, self.img_hooks,
                        self.img_syslinux_splash, self.img_debian_installer_check,
                        self.img_debian_installer_banner,
                        self.img_debian_installer_preseed,
                        self.img_debian_installer_gtk
                        )
                    },
                True, False
                )
            )

        if self.native_arch == 'i686':
            for child in self.profilearch:
                if child.get_label() == 'amd64':
                    child.set_sensitive(False)

        # Showing
        self.window.add(self.outbox)
        self.window.show_all()

        Toggle(self, self.os_extrarepos_box_1)
        Toggle(self, self.os_extrarepos_box_2)
        Toggle(self, self.os_includes_box)
        Toggle(self, self.os_hooks_box)
        Toggle(self, self.img_includes_box)
        Toggle(self, self.img_hooks_box)
#        Toggle(self, self.img_syslinux_splash_box)
        Toggle(self, self.img_debian_installer_box)

class Test():
    pass
#    def __init__(self):
#        # Creating Window
#        self.window = gtk.Window()
#        self.window.set_border_width(0)
#        self.window.set_title(TEST_TITLE)
#        self.window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
#        self.window.set_size_request(window_width, window_height)
#        self.window.set_resizable(False)
#        self.window.connect("destroy", gtk.main_quit)
#        self.window.connect("delete-event", gtk.main_quit)
#        self.window.set_icon_from_file(BAR_ICON)

#        self.vbox = gtk.VBox()
#        self.inbox = gtk.VBox()
#        self.inbox.set_border_width(10)

#        self.banner = Banner(self, BANNER_IMAGE)

#        self.test_image_title = Title(c = self, text = TEST_IMAGE_1)
#        self.test_memory_title = Title(c = self, text = TEST_MEMORY_1)
#        self.test_processors_title = Title(c = self, text = TEST_PROCESSORS_1)
#        self.test_start_title = Title(c = self, text = TEST_START_1)

#        self.test_image_help = ActiveLink(c = self, text = TEST_IMAGE_2)
#        self.test_memory_help = ActiveLink(c = self, text = TEST_MEMORY_2)
#        self.test_processors_help = ActiveLink(c = self, text = TEST_PROCESSORS_2)
#        self.test_start_help = ActiveLink(c = self, text = TEST_START_2)
#        self.test_disk_help = ActiveLink(c = self, text = TEST_DISK_2)

#        self.freedisk = GetFreeDisk()
#        self.freeram = GetFreeRam()
#        self.processors = GetProcessors()

#        self.test_image_entries_box = gtk.HBox()

#        self.test_image, self.testimage = TextEntry(
#            c = self, indent = False, maxlength = 1024, length = 68,
#            text = TEST_IMAGE_ENTRY, regex = '^.*$'
#            )

#        self.test_image_choose, self.testimagechoose = ActiveButton(
#            c = self, text = gtk.STOCK_OPEN,
#            width = 0, height = 0,
#            f_1 = ThreadGenerator,
#            p_1 = (
#                UserSelect, {
#                    'c': self,
#                    'title': TEST_IMAGE_SELECT_TITLE,
#                    'action': gtk.FILE_CHOOSER_ACTION_OPEN,
#                    'allfiltertitle': TEST_MIMETYPE_ALL_NAME,
#                    'filter': {
#                        'name': TEST_MIMETYPE_ISO_NAME,
#                        'mimetypes': ('application/octet-stream',)
#                        },
#                    'entry': self.testimage
#                    },
#                True, False
#                )
#            )

#        self.test_image_clean, self.testimageclean = ActiveButton(
#            c = self, text = gtk.STOCK_CLEAR,
#            width = 0, height = 0,
#            f_1 = CleanEntry, p_1 = (self.testimage,),
#            )

#        self.test_memory, self.testmemory = NumericSelector(
#            c = self, indent = True, init = 256.0, lower = 256.0,
#            upper = self.freeram, inc_1 = 10.0, inc_2 = 100.0
#            )

#        self.test_processors, self.testprocessors = NumericSelector(
#            c = self, indent = True, init = 1.0, lower = 1.0,
#            upper = self.processors, inc_1 = 1.0, inc_2 = 1.0
#            )

#        self.test_start, self.teststart = OptionList(
#            c = self, indent = True, optionlist = [
##                TEST_START_CD_LABEL, TEST_START_HD_LABEL
#                '-c', '-d'
#                ]
#            )

#        self.test_disk, self.testdisk = NumericSelector(
#            c = self, indent = True, init = 10.0, lower = 5.0,
#            upper = self.freedisk, inc_1 = 1.0, inc_2 = 10.0
#            )

#        self.test_disk_check, self.testdiskcheck = ActiveCheck(
#            c = self, text = TEST_DISK_CHECK_LABEL,
#            active = False,
#            f_1 = Toggle, p_1 = (
#                False, self.test_disk,
#                False, False, False
#                ),
#            )

#        self.bottombuttons = BottomButtons(
#            c = self, width = 80, height = 30,
#            fclose = ThreadGenerator,
#            pclose = (
#                UserMessage, {
#                    'message': TEST_CONFIRM_CANCEL_MSG,
#                    'title': TEST_CONFIRM_CANCEL_TITLE,
#                    'type': gtk.MESSAGE_QUESTION,
#                    'buttons': gtk.BUTTONS_YES_NO,
#                    'c_1': gtk.RESPONSE_YES,
#                    'f_1': self.window.destroy, 'p_1': '',
#                    'c_2': gtk.RESPONSE_YES,
#                    'f_2': gtk.main_quit, 'p_2': ''
#                    },
#                True, False
#                ),
#            fhelp = ThreadGenerator,
#            phelp = (
#                ProcessGenerator, {
#                    'command': ['/usr/bin/yelp', DOCDIR+'/index.html']
#                    },
#                True, False
#            ),
#            fabout = ThreadGenerator,
#            pabout = (
#                AboutWindow, {
#                    'img': ABOUT_IMAGE, 'name': app_name,
#                    'version': app_version, 'url': app_url,
#                    'copyright': app_copyright, 'description': app_description,
#                    'authorsfile': AUTHORS_FILE, 'licensefile': LICENCE_FILE,
#                    'translatorsfile': TRANSLATORS_FILE
#                    },
#                True, False
#                ),
#            fback = ThreadGenerator,
#            pback = (
#                UserMessage, {
#                    'message': TEST_CONFIRM_CANCEL_MSG,
#                    'title': TEST_CONFIRM_CANCEL_TITLE,
#                    'type': gtk.MESSAGE_QUESTION,
#                    'buttons': gtk.BUTTONS_YES_NO,
#                    'c_1': gtk.RESPONSE_YES,
#                    'f_1': self.window.hide, 'p_1': '',
#                    'c_2': gtk.RESPONSE_YES,
#                    'f_2': Main, 'p_2': ''
#                    },
#                True, False
#                ),
#            fgo = ThreadGenerator,
#            pgo = (
#                UserMessage, {
#                    'message': TEST_CONFIRM_OK_MSG,
#                    'title': TEST_CONFIRM_OK_TITLE,
#                    'type': gtk.MESSAGE_QUESTION,
#                    'buttons': gtk.BUTTONS_YES_NO,
#                    'c_1': gtk.RESPONSE_YES,
#                    'f_1': TestImage, 'p_1': (
#                        self, self.testimage, self.testmemory,
#                        self.testprocessors, self.teststart
#                        )
#                    },
#                True, False
#                )
#            )

#        self.vbox.pack_start(self.banner, expand, fill, padding)

#        self.inbox.pack_start(self.test_image_title, expand, fill, padding)
#        self.test_image_entries_box.pack_start(self.test_image, expand, fill, padding)
#        self.test_image_entries_box.pack_start(self.test_image_choose, expand, fill, padding)
#        self.test_image_entries_box.pack_start(self.test_image_clean, expand, fill, padding)
#        self.inbox.pack_start(self.test_image_entries_box, expand, fill, padding)
#        self.inbox.pack_start(self.test_image_help, expand, fill, padding)
#        self.inbox.pack_start(gtk.HSeparator(), expand, fill, padding)
#        self.inbox.pack_start(self.test_memory_title, expand, fill, padding)
#        self.inbox.pack_start(self.test_memory, expand, fill, padding)
#        self.inbox.pack_start(self.test_memory_help, expand, fill, padding)
#        self.inbox.pack_start(gtk.HSeparator(), expand, fill, padding)
#        self.inbox.pack_start(self.test_processors_title, expand, fill, padding)
#        self.inbox.pack_start(self.test_processors, expand, fill, padding)
#        self.inbox.pack_start(self.test_processors_help, expand, fill, padding)
#        self.inbox.pack_start(gtk.HSeparator(), expand, fill, padding)
#        self.inbox.pack_start(self.test_start_title, expand, fill, padding)
#        self.inbox.pack_start(self.test_start, expand, fill, padding)
#        self.inbox.pack_start(self.test_start_help, expand, fill, padding)

#        self.vbox.pack_start(self.inbox, expand, fill, padding)
#        self.vbox.pack_start(self.bottombuttons, expand, fill, padding)

#        self.window.add(self.vbox)
#        self.window.show_all()

class Save():
    pass
#    def __init__(self):
#        # Creating Window
#        self.window = gtk.Window()
#        self.window.set_border_width(0)
#        self.window.set_title(BUILD_TITLE)
#        self.window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
#        self.window.set_size_request(window_width, window_height)
#        self.window.set_resizable(False)
#        self.window.connect("destroy", gtk.main_quit)
#        self.window.set_icon_from_file(BAR_ICON)

#        self.vbox = gtk.VBox(False, 5)
#        self.inbox = gtk.VBox(False, 5)
#        self.inbox.set_border_width(10)

#        self.profile_name_title = Title(c = self, text = BUILD_PROFILE_NAME_1)
#        self.profile_arch_title = Title(c = self, text = BUILD_PROFILE_ARCH_1)
#        self.profile_media_title = Title(c = self, text = BUILD_PROFILE_MEDIA_1)

#        self.profile_name_help = ActiveLink(c = self, text = BUILD_PROFILE_NAME_2)
#        self.profile_arch_help = ActiveLink(c = self, text = BUILD_PROFILE_ARCH_2)
#        self.profile_media_help = ActiveLink(c = self, text = BUILD_PROFILE_MEDIA_2)

#        self.profilelist, self.profiledefault = ProfileList(
#            c = self, profiledir = PROFILEDIR
#            )

#        self.nativearch = GetArch()

#        self.banner = Banner(self, BANNER_IMAGE)

#        self.profile_name, self.profilename = Combo(
#            c = self, indent = True, combolist = self.profilelist,
#            combodefault = self.profiledefault, entry = False
#            )

#        self.profile_arch, self.profilearch = OptionList(
#            c = self, indent = True, optionlist = supported_arch
#            )

#        self.profile_media, self.profilemedia = OptionList(
#            c = self, indent = True, optionlist = supported_media
#            )

#        if self.nativearch == 'i686':
#            for child in self.profilearch:
#                if child.get_label() == 'amd64':
#                    child.set_sensitive(False)

#        self.bottombuttons = BottomButtons(
#            c = self, width = 80, height = 30,
#            fclose = ThreadGenerator,
#            pclose = (
#                UserMessage, {
#                    'message': BUILD_CONFIRM_CANCEL_MSG,
#                    'title': BUILD_CONFIRM_CANCEL_TITLE,
#                    'type': gtk.MESSAGE_QUESTION,
#                    'buttons': gtk.BUTTONS_YES_NO,
#                    'c_1': gtk.RESPONSE_YES,
#                    'f_1': self.window.destroy, 'p_1': '',
#                    'c_2': gtk.RESPONSE_YES,
#                    'f_2': gtk.main_quit, 'p_2': ''
#                    },
#                True, False
#                ),
#            fhelp = ThreadGenerator,
#            phelp = (
#                ProcessGenerator, {
#                    'command': ['/usr/bin/yelp', DOCDIR+'/index.html']
#                    },
#                True, False
#            ),
#            fabout = ThreadGenerator,
#            pabout = (
#                AboutWindow, {
#                    'img': ABOUT_IMAGE, 'name': app_name,
#                    'version': app_version, 'url': app_url,
#                    'copyright': app_copyright, 'description': app_description,
#                    'authorsfile': AUTHORS_FILE, 'licensefile': LICENCE_FILE,
#                    'translatorsfile': TRANSLATORS_FILE
#                    },
#                True, False
#                ),
#            fback = ThreadGenerator,
#            pback = (
#                UserMessage, {
#                    'message': BUILD_CONFIRM_CANCEL_MSG % '\n\n',
#                    'title': BUILD_CONFIRM_CANCEL_TITLE,
#                    'type': gtk.MESSAGE_QUESTION,
#                    'buttons': gtk.BUTTONS_YES_NO,
#                    'c_1': gtk.RESPONSE_YES,
#                    'f_1': self.window.hide, 'p_1': '',
#                    'c_2': gtk.RESPONSE_YES,
#                    'f_2': Main, 'p_2': ''
#                    },
#                True, False
#                ),
#            fgo = ThreadGenerator,
#            pgo = (
#                UserMessage, {
#                    'message': BUILD_CONFIRM_OK_MSG % '\n\n',
#                    'title': BUILD_CONFIRM_OK_TITLE,
#                    'type': gtk.MESSAGE_QUESTION,
#                    'buttons': gtk.BUTTONS_YES_NO,
#                    'c_1': gtk.RESPONSE_YES,
#                    'f_1': BuildImage, 'p_1': (
#                        self, self.profilename, self.profilearch,
#                        self.profilemedia, self.inbox
#                        )
#                    },
#                True, False
#                )
#            )

#        self.vbox.pack_start(self.banner, expand, fill, padding)

#        self.inbox.pack_start(self.profile_name_title, expand, fill, padding)
#        self.inbox.pack_start(self.profile_name_help, expand, fill, padding)
#        self.inbox.pack_start(self.profile_name, expand, fill, padding)
#        self.inbox.pack_start(gtk.HSeparator(), expand, fill, padding)
#        self.inbox.pack_start(self.profile_arch_title, expand, fill, padding)
#        self.inbox.pack_start(self.profile_arch_help, expand, fill, padding)
#        self.inbox.pack_start(self.profile_arch, expand, fill, padding)
#        self.inbox.pack_start(gtk.HSeparator(), expand, fill, padding)
#        self.inbox.pack_start(self.profile_media_title, expand, fill, padding)
#        self.inbox.pack_start(self.profile_media_help, expand, fill, padding)
#        self.inbox.pack_start(self.profile_media, expand, fill, padding)
#        self.inbox.pack_start(self.bottombuttons, expand, fill, padding)

#        self.vbox.pack_start(self.inbox, expand, fill, padding)

#        self.window.add(self.vbox)
#        self.window.show_all()
