#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gtk, re

from config import *
from library.intelligence import *

def Dummy(signaled, class_id):
    pass

def LimitEntry(editable, new_text, new_text_length, position, regex):
    limit = re.compile(regex)
    if limit.match(new_text) is None:
        editable.stop_emission('insert-text')

def CleanEntry(editable, destination):
    textbuffer = destination['destination']
    textbuffer.set_text('')

def ClearEntry(editable, new_text, text):
    content = editable.get_text()
    if content == text:
        editable.set_text('')

def FillEntry(editable, new_text, text):
    content = editable.get_text()
    if content == '':
        editable.set_text(text)

def Toggle(widget, destination):
    widgetcontainer = destination['destination']
    on_off_widgetlist = widgetcontainer.get_children()
    for on_off_widget in on_off_widgetlist:
        new_widgets = on_off_widget.get_children()
        on_off_widgetlist = on_off_widgetlist + new_widgets
    for on_off_widget in on_off_widgetlist:
        if on_off_widget != widget:
            if on_off_widget.get_sensitive() == True:
                on_off_setting = False
            else:
                on_off_setting = True
            on_off_widget.set_sensitive(on_off_setting)

def ChangeCodename(signaled, class_id):
    dist = class_id.metadist
    db = apt_templates
    codenamecombo = class_id.metacodename
    codenamelist, codenameactive = CodenameList(class_id, dist, db)
    codenamecombo.get_model().clear()
    for item in codenamelist:
        codenamecombo.append_text(item)
    codenamecombo.set_active(codenameactive)

def ChangeRepo(signaled, class_id):
    dist = class_id.metadist.get_active_text()
    repoentry = class_id.metarepo
    exec "newrepotext = "+dist+"_repo"
    repoentry.set_text(newrepotext)

def ChangeSections(signaled, class_id):
    sections = class_id.metareposections
    checklist = SectionList(class_id, class_id.metadist)
    checkdefault = section_default
    children = sections.get_children()
    for child in children:
        sections.remove(child)
    for item in checklist:
        check = gtk.CheckButton(item)
        if item == checkdefault:
            check.set_active(True)
            check.set_sensitive(False)
        check.show()
        sections.pack_start(check, expand, fill, padding)

def AddExtraReposThread(signaled, class_id):
    url = urlbox.get_active_text()
    branch = branchbox.get_active_text()
    sections = sectionsbox.get_active_text()
    
    
    
    
    
