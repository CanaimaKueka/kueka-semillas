#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gtk, pango
from aptsources.distinfo import DistInfo

from config import *

def LimitEntry(editable, new_text, new_text_length, position, regex):
    limit = re.compile(regex)
    if limit.match(new_text) is None:
        editable.stop_emission('insert-text')

def CleanEntry(editable, textbuffer):
    textbuffer.set_text('')

def ClearEntry(editable, new_text, text):
    content = editable.get_text()
    if content == text:
        editable.set_text('')

def FillEntry(editable, new_text, text):
    content = editable.get_text()
    if content == '':
        editable.set_text(text)

def OnOff(widget, widgetcontainer):
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

def Dummy(class_id):
    pass

def LocaleList(class_id, supported, current):
    localecount = 0
    localeactive = 0
    localelist = []
    with open(supported, 'r') as supportedlocales:
        for item in supportedlocales:
            localecode = item.split()
            localelist.append(localecode[0])
            if localecode[0].upper().replace('-','') == current.upper().replace('-',''):
                localeactive = localecount
            localecount += 1

    return localelist, localeactive

def CodenameList(class_id, metadist, apt_templates):
    codenamelist = []
    codenameactive = 0
    curmetadist = metadist.get_active_text().title()
    d = DistInfo(curmetadist, apt_templates)

    for template in d.templates:
        codenamelist.append(template.name)

    return codenamelist, codenameactive

def SectionList(class_id, metadist):
    metadisttext = metadist.get_active_text()
    exec "sectionlist = "+metadisttext+"_sections"
    return sectionlist

def ChangeCodename(class_id, ):
    bigcodenames.remove(codename)
    curdistro = distro.get_active_text()
    curdistro_u = curdistro.title()
    codename = gtk.combo_box_new_text()
    d = DistInfo(curdistro_u, apt_templates)
    codenamelist = []
    for template in d.templates:
        if not template.name in codenamelist:
            codenamelist.append(template.name)
            codename.append_text(template.name)
    codename.append_text('otro')
    codename.set_active(0)

    codename.show()
    bigcodenames.pack_start(codename, expand, fill, padding)

    children = reposections.get_children()
    for child in children:
        reposections.remove(child)
    curdistro = distro.get_active_text()
    exec 'currepo = '+curdistro+'_repo'
    repo.set_text(currepo)
    exec 'cursections = '+curdistro+'_sections'
    for section in cursections:
        label = section
        if section.find('-') != -1:
            section = section.replace('-','')
        if section == 'main':
            global mainsection
            mainsection = gtk.CheckButton('main')
            mainsection.set_active(True)
            mainsection.set_sensitive(False)
            mainsection.show()
            reposections.pack_start(mainsection)
        else:
            exec 'global '+section+'section\n'+section+'section = gtk.CheckButton(label)\n'+section+'section.set_active(False)\n'+section+'section.show()\nreposections.pack_start('+section+'section)'

def Banner(class_id, imagefile):
    banner = gtk.HBox(homogeneous, spacing)
    banner.set_border_width(borderwidth)

    image = gtk.Image()
    image.set_from_file(imagefile)
    image.show()
    banner.pack_start(image, expand, fill, padding)

    return banner

def Title(class_id, textblock):
    box = gtk.HBox(homogeneous, spacing)
    box.set_border_width(borderwidth)

    boxwidth = window_width - (borderwidth*10)

    obj = gtk.Label()
    obj.set_markup(textblock)
    obj.set_line_wrap(True)
    obj.set_size_request(boxwidth, -1)
    obj.show()

    box.pack_start(obj, expand, fill, padding)

    return box

def Description(class_id, textblock):
    box = gtk.HBox(homogeneous, spacing)
    box.set_border_width(borderwidth/2)

    boxwidth = window_width - (borderwidth*10)

    objattr = pango.AttrList()
    size = pango.AttrSize(8000, 0, -1)
    objattr.insert(size)

    obj = gtk.Label()
    obj.set_markup(textblock)
    obj.set_line_wrap(True)
    obj.set_size_request(boxwidth, -1)
    obj.set_attributes(objattr)
    obj.show()

    box.pack_start(obj, expand, fill, padding)

    return box

def TextEntry(class_id, maxlength, length, text, regex):
    box = gtk.HBox(homogeneous, spacing)
    box.set_border_width(borderwidth/3)

    obj = gtk.Entry()
    obj.connect('insert-text', LimitEntry, regex)
    obj.connect('focus-in-event', ClearEntry, text)
    obj.connect('focus-out-event', FillEntry, text)
    obj.set_width_chars(length)
    obj.set_max_length(maxlength)
    obj.set_text(text)
    obj.set_sensitive(True)
    obj.set_editable(True)
    obj.set_visibility(True)
    box.pack_start(obj, expand, fill, padding)
    box.show()

    return box, obj

def Combo(class_id, combolist, combodefault, f_1, p_1):
    box = gtk.HBox(homogeneous, spacing)
    box.set_border_width(borderwidth/3)

    combo = gtk.combo_box_new_text()

    for item in combolist:
        combo.append_text(item)

    combo.set_active(combodefault)
    combo.connect('changed', f_1, p_1)
    combo.show()

    box.pack_start(combo, expand, fill, padding)

    return box, combo

def CheckList(class_id, checklist, checkdefault):

    box = gtk.HBox(homogeneous, spacing)
    box.set_border_width(borderwidth/3)

    space = gtk.HSeparator()
    box.pack_start(space, expand, fill, 30)

    items = gtk.VBox(homogeneous, spacing)
    items.set_border_width(borderwidth/3)

    for item in checklist:
        check = gtk.CheckButton(item)
        if item == checkdefault:
            check.set_active(True)
            check.set_sensitive(False)
        check.show()
        items.pack_start(check, expand, fill, padding)

    box.pack_start(items, expand, fill, padding)

    return box, items
