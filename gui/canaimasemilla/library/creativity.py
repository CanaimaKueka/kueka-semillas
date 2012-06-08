#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gtk, pango, vte

from config import *

def Banner(class_id, image):
    box = gtk.HBox(homogeneous, spacing)
    box.set_border_width(0)

    banner = gtk.Image()
    banner.set_from_file(image)
    banner.show()

    box.pack_start(banner, expand, fill, padding)

    return box

def Title(class_id, text):
    box = gtk.HBox(homogeneous, spacing)
    box.set_border_width(borderwidth/5)

    title = gtk.Label()
    title.set_markup(text)
    title.set_line_wrap(True)
    title.set_size_request(window_width - (borderwidth*10), -1)
    title.show()

    box.pack_start(title, expand, fill, padding)

    return box

def Description(class_id, text):
    box = gtk.HBox(homogeneous, spacing)
    box.set_border_width(borderwidth/5)

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

def TextEntry(class_id, indent, maxlength, length, text, regex, flimit, fclear, ffill):
    box = gtk.HBox(homogeneous, spacing)
    if indent:
        box.set_border_width(borderwidth)
    else:
        box.set_border_width(borderwidth/5)

    if indent:
        box.pack_start(gtk.HSeparator(), expand, fill, 30)
    textentry = gtk.Entry()
    textentry.set_width_chars(length)
    textentry.set_max_length(maxlength)
    textentry.set_text(text)
    textentry.set_sensitive(True)
    textentry.set_editable(True)
    textentry.set_visibility(True)
    textentry.connect('insert-text', flimit, regex)
    textentry.connect('focus-in-event', fclear, text)
    textentry.connect('focus-out-event', ffill, text)
    textentry.show()

    box.pack_start(textentry, expand, fill, padding)

    return box, textentry

def Combo(class_id, indent, combolist, combodefault, entry,
                    f_1 = False, p_1 = False,
                    f_2 = False, p_2 = False,
                    f_3 = False, p_3 = False
                    ):

    box = gtk.HBox(homogeneous, spacing)
    box.set_border_width(borderwidth)

    if indent:
        box.pack_start(gtk.HSeparator(), expand, fill, 30)

    if entry:
        combo = gtk.combo_box_entry_new_text()
    else:
        combo = gtk.combo_box_new_text()

    for item in combolist:
        combo.append_text(item)

    if f_1:
        combo.connect('changed', f_1, p_1)

    if f_2:
        combo.connect('changed', f_2, p_2)

    if f_3:
        combo.connect('changed', f_3, p_3)

    combo.set_active(combodefault)
    combo.show()

    box.pack_start(combo, expand, fill, padding)

    return box, combo

def CheckList(class_id, indent, checklist, checkdefault = ''):
    box = gtk.HBox(homogeneous, spacing)
    box.set_border_width(borderwidth)

    if indent:
        box.pack_start(gtk.HSeparator(), expand, fill, 30)

    items = gtk.VBox(homogeneous, spacing)
    items.set_border_width(borderwidth)

    for item in checklist:
        check = gtk.CheckButton(item)
        if checkdefault != '' and item == checkdefault:
            check.set_active(True)
            check.set_sensitive(False)
        check.show()
        items.pack_start(check, expand, fill, padding)

    box.pack_start(items, expand, fill, padding)

    return box, items

def OptionList(class_id, indent, optionlist, optiondefault = ''):
    box = gtk.HBox(homogeneous, spacing)
    box.set_border_width(borderwidth)

    if indent:
        box.pack_start(gtk.HSeparator(), expand, fill, 30)

    items = gtk.VBox(homogeneous, spacing)
    items.set_border_width(borderwidth)

    option = None
    for item in optionlist:
        option = gtk.RadioButton(option, item)
        if optiondefault != '' and item == optiondefault:
            option.set_active(True)
            option.set_sensitive(False)
        option.show()
        items.pack_start(option, expand, fill, padding)

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

def ActiveButton(class_id, text, width, height,
                    f_1 = False, p_1 = False,
                    f_2 = False, p_2 = False,
                    f_3 = False, p_3 = False
                    ):

    box = gtk.HBox(homogeneous, spacing)
    box.set_border_width(0)

    button = gtk.Button(stock = text)

    if width != 0 and height != 0:
        button.set_size_request(width, height)

    if f_1:
        button.connect('clicked', f_1, *p_1)

    if f_2:
        button.connect('clicked', f_2, *p_2)

    if f_3:
        button.connect('clicked', f_3, *p_3)

    button.show()

    box.pack_start(button, expand, fill, padding)

    return box, button

def ActiveCheck(class_id, text, active,
                    f_1 = False, p_1 = False,
                    f_2 = False, p_2 = False,
                    f_3 = False, p_3 = False
                    ):

    box = gtk.HBox(homogeneous, spacing)
    box.set_border_width(0)

    check = gtk.CheckButton(text)
    check.set_border_width(borderwidth)

    if active:
        check.set_active(True)

    if f_1:
        check.connect('toggled', f_1, p_1)

    if f_2:
        check.connect('toggled', f_2, p_2)

    if f_3:
        check.connect('toggled', f_3, p_3)

    check.show()

    box.pack_start(check, expand, fill, padding)

    return box, check

def UserMessage(message, title, type, buttons,
                    c_1 = False, f_1 = False, p_1 = '',
                    c_2 = False, f_2 = False, p_2 = '',
                    c_3 = False, f_3 = False, p_3 = ''
                    ):

    dialog = gtk.MessageDialog(
        parent = None, flags = 0, type = type,
        buttons = buttons, message_format = message
        )
    dialog.set_title(title)
    answer = dialog.run()
    dialog.destroy()

    if answer == c_1:
        f_1(*p_1)

    if answer == c_2:
        f_2(*p_2)

    if answer == c_3:
        f_3(*p_3)

    return answer

def ProgressWindow(text, title, term, fcancel, pcancel,
                    q_window, q_bar, q_msg, q_terminal):

    dialog = gtk.Dialog()
    dialog.set_title(title)
    dialogarea = dialog.get_content_area()
    dialog.set_position(gtk.WIN_POS_CENTER_ALWAYS)
    if term:
        dialog.set_size_request(window_width*3/4, window_height*3/4)
    else:
        dialog.set_size_request(window_width*3/4, window_height/4)
    dialog.set_resizable(False)

    box = gtk.VBox(homogeneous, spacing)
    box.set_border_width(borderwidth)

    label = gtk.Label()
    label.set_markup(text)
    progress = gtk.ProgressBar()

    if term:
        terminal = vte.Terminal()
        terminal.set_cursor_blinks(True)
        terminal.set_emulation('xterm')
        terminal.set_font_from_string('fixed 8')
        terminal.set_scrollback_lines(1000)
        terminal.set_audible_bell(True)
        terminal.set_visible_bell(False)

    box.pack_start(label, expand, fill, padding)
    box.pack_start(progress, expand, fill, padding)

    if term:
        box.pack_start(gtk.HSeparator(), expand, fill, padding)
        box.pack_start(terminal, expand, fill, padding)

    button = gtk.Button(stock = gtk.STOCK_CANCEL)
    if fcancel:
        button.connect("clicked", fcancel, *pcancel)
    button.connect_object("clicked", gtk.Window.destroy, dialog)
    box.pack_start(gtk.HSeparator(), expand, fill, padding)
    box.pack_start(button, expand, fill, padding)

    dialogarea.add(box)
    dialog.show_all()
    
    q_window.put(dialog)
    q_bar.put(progress)
    q_msg.put(label)
    if term:
        q_terminal.put(terminal)
    return dialog

def IconButton(class_id, icon, text_1, text_2, width, height, f_1, p_1):
    box = gtk.VBox(homogeneous, spacing)
    box.set_border_width(borderwidth)

    button = gtk.Button()
    button.connect("clicked", f_1, *p_1)
    button.set_size_request(width, height)

    inbox = gtk.VBox(homogeneous, spacing)
    inbox.set_border_width(borderwidth)

    image = gtk.Image()
    image.set_from_file(icon)

    attr = pango.AttrList()
    size = pango.AttrSize(20000, 0, -1)
    attr.insert(size)

    title = gtk.Label()
    title.set_markup(text_1)
    title.set_justify(gtk.JUSTIFY_CENTER)
    title.set_attributes(attr)

    description = gtk.Label()
    description.set_markup(text_2)
    description.set_line_wrap(True)
    description.set_justify(gtk.JUSTIFY_CENTER)

    inbox.pack_start(image, expand, fill, padding)
    inbox.pack_start(title, expand, fill, padding)
    inbox.pack_start(gtk.HSeparator(), expand, fill, padding)
    inbox.pack_start(description, expand, fill, padding)
    button.add(inbox)
    box.pack_start(button, expand, fill, padding)

    return box

def AboutWindow(img, name, version, url, copyright, description,
    authorsfile, licensefile, translatorsfile):

    about = gtk.AboutDialog()
    about.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
    about.set_logo(gtk.gdk.pixbuf_new_from_file(img))
    about.set_name(name)
    about.set_version(version)
    about.set_copyright(copyright)
    about.set_comments(description)
    about.set_website(url)

    try:
        f = open(licensefile, 'r')
        license = f.read()
        f.close()
    except Exception, msg:
        license =  'NOT FOUND'

    try:
        f = open(authorsfile, 'r')
        a = f.read()
        authors = a.split('\n')
        f.close()
    except Exception, msg:
        authors = 'NOT FOUND'

    try:
        f = open(translatorsfile, 'r')
        translators = f.read()
        f.close()
    except Exception, msg:
        translators = 'NOT FOUND'

    about.set_translator_credits(translators)
    about.set_authors(authors)
    about.set_license(license)

    about.run()
    about.destroy()

def BottomButtons(class_id, width, height, fclose = False, pclose = False, 
        fhelp = False, phelp = False, fabout = False, pabout = False,
        fback = False, pback = False, fgo = False, pgo = False
        ):

    box = gtk.VBox(homogeneous, spacing)
    hbox = gtk.HBox(homogeneous, spacing)

    if fclose:
        close_button, close = ActiveButton(
            class_id = class_id, text = gtk.STOCK_CLOSE,
            width = width, height = height,
            f_1 = fclose, p_1 = pclose
        )

        hbox.pack_start(close_button, expand, fill, padding)

    if fhelp:
        help_button, help = ActiveButton(
            class_id = class_id, text = gtk.STOCK_HELP,
            width = width, height = height,
            f_1 = fhelp, p_1 = phelp
        )

        hbox.pack_start(help_button, expand, fill, padding)

    if fabout:
        about_button, about = ActiveButton(
            class_id = class_id, text = gtk.STOCK_ABOUT,
            width = width, height = height,
            f_1 = fabout, p_1 = pabout
        )

        hbox.pack_start(about_button, expand, fill, padding)

    hbox.pack_start(gtk.HSeparator(), expand, fill, 140)

    if fback:
        back_button, back = ActiveButton(
            class_id = class_id, text = gtk.STOCK_GO_BACK,
            width = width, height = height,
            f_1 = fback, p_1 = pback
        )

        hbox.pack_start(back_button, expand, fill, padding)

    if fgo:
        go_button, go = ActiveButton(
            class_id = class_id, text = gtk.STOCK_GO_FORWARD,
            width = width, height = height,
            f_1 = fgo, p_1 = pgo
        )

        hbox.pack_start(go_button, expand, fill, padding)

    box.pack_start(gtk.HSeparator(), expand, fill, padding)
    box.pack_start(hbox, expand, fill, padding)

    return box
