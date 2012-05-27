#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gtk, pango

from config import *
from library.dynamism import *

def Banner(class_id, image):
    box = gtk.HBox(homogeneous, spacing)
    box.set_border_width(borderwidth/3)

    banner = gtk.Image()
    banner.set_from_file(image)
    banner.show()

    box.pack_start(banner, expand, fill, padding)

    return box

def Title(class_id, text):
    box = gtk.HBox(homogeneous, spacing)
    box.set_border_width(borderwidth)

    title = gtk.Label()
    title.set_markup(text)
    title.set_line_wrap(True)
    title.set_size_request(window_width - (borderwidth*10), -1)
    title.show()

    box.pack_start(title, expand, fill, padding)

    return box

def Description(class_id, text):
    box = gtk.HBox(homogeneous, spacing)
    box.set_border_width(borderwidth/3)

    style = pango.AttrList()
    size = pango.AttrSize(8000, 0, -1)
    style.insert(size)

    description = gtk.Label()
    description.set_markup(text)
    description.set_line_wrap(True)
    description.set_size_request(window_width - (borderwidth*10), -1)
    description.set_attributes(style)
    description.show()

    box.pack_start(description, expand, fill, padding)

    return box

def TextEntry(class_id, maxlength, length, text, regex):
    box = gtk.HBox(homogeneous, spacing)
    box.set_border_width(borderwidth/3)

    textentry = gtk.Entry()
    textentry.set_width_chars(length)
    textentry.set_max_length(maxlength)
    textentry.set_text(text)
    textentry.set_sensitive(True)
    textentry.set_editable(True)
    textentry.set_visibility(True)
    textentry.connect('insert-text', LimitEntry, regex)
    textentry.connect('focus-in-event', ClearEntry, text)
    textentry.connect('focus-out-event', FillEntry, text)
    textentry.show()

    box.pack_start(textentry, expand, fill, padding)

    return box, textentry

def Combo(class_id, combolist, combodefault, entry, f_1, f_2, f_3):
    box = gtk.HBox(homogeneous, spacing)
    box.set_border_width(borderwidth/3)

    if entry:
        combo = gtk.combo_box_entry_new_text()
    else:
        combo = gtk.combo_box_new_text()

    for item in combolist:
        combo.append_text(item)

    combo.set_active(combodefault)
    combo.connect('changed', f_1, class_id)
    combo.connect('changed', f_2, class_id)
    combo.connect('changed', f_3, class_id)
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

def ScrolledFrame(class_id):
    frame = gtk.Frame()
    frame.set_border_width(borderwidth/3)

    scrolledwindow = gtk.ScrolledWindow()
    scrolledwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

    textview = gtk.TextView()
    textview.set_wrap_mode(gtk.WRAP_WORD)
    textview.set_editable(False)
    text = textview.get_buffer()

    scrolledwindow.add(textview)
    frame.add(scrolledwindow)

    return frame, text

def ActiveButton(class_id, text, f_1, p_1):
    box = gtk.HBox(homogeneous, spacing)
    box.set_border_width(borderwidth*0)

    button = gtk.Button(stock = text)
    button.set_border_width(borderwidth*0)
    button.connect('clicked', f_1, p_1)
    button.show()

    box.pack_start(button, expand, fill, padding)

    return box, button

def ActiveCheck(class_id, text, active, f_1, p_1, f_2, p_2):
    box = gtk.HBox(homogeneous, spacing)
    box.set_border_width(borderwidth/3)

    check = gtk.CheckButton(text)
    check.set_border_width(borderwidth)
    if active:
        check.set_active(True)
    check.connect('toggled', f_1, p_1)
    check.connect('toggled', f_2, p_2)
    check.show()

    box.pack_start(check, expand, fill, padding)

    return box, check
