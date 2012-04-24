#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import pygtk, gtk, re, os, threading, urllib2, shutil, pango
from subprocess import Popen, PIPE, STDOUT

# Librerías Locales
import main
from library.strings import *
from library.localization import *
from config import *

class Profile_1():

    def Banner(self, homogeneous, spacing, expand, fill, padding, borderwidth, imagefile):
        banner = gtk.HBox(homogeneous, spacing)
        banner.set_border_width(borderwidth)

        image = gtk.Image()
        image.set_from_file(imagefile)
        image.show()
        
        banner.pack_start(image, expand, fill, padding)

        return banner
        
    def Ask(self, homogeneous, spacing, expand, fill, padding, borderwidth, textblock):
        ask = gtk.HBox(homogeneous, spacing)
        ask.set_border_width(borderwidth)

        askwidth = WindowWidth - (borderwidth*4)

        descripcion = gtk.Label()
        descripcion.set_markup(textblock)
        descripcion.set_line_wrap(True)
        descripcion.set_size_request(askwidth, -1)
        descripcion.show()
        
        ask.pack_start(descripcion, expand, fill, padding)
        
        return ask

    def Entry(self, homogeneous, spacing, expand, fill, padding, borderwidth, maxlength, pretexto, regex):
        def Limit(editable, new_text, new_text_length, position):
            limit = re.compile(regex)
            if limit.match(new_text) is None:
                editable.stop_emission('insert-text')

        entry = gtk.HBox(homogeneous, spacing)
        entry.set_border_width(borderwidth)

        global nombresabor

        nombresabor = gtk.Entry()
        nombresabor.connect('insert-text', Limit)
        nombresabor.set_max_length(maxlength)
        nombresabor.set_text(pretexto)
        nombresabor.set_sensitive(True)
        nombresabor.set_editable(True)
        nombresabor.set_visibility(True)
        entry.pack_start(nombresabor, expand, fill, padding)
        nombresabor.show()

        return entry

    def Description(self, homogeneous, spacing, expand, fill, padding, borderwidth, textblock):
        description = gtk.HBox(homogeneous, spacing)
        description.set_border_width(borderwidth)

        descriptionwidth = WindowWidth - (borderwidth*4)
        
        attrdescription = pango.AttrList()
        size = pango.AttrSize(8500, 0, -1)
        attrdescription.insert(size)
        
        text = gtk.Label()
        text.set_markup(textblock)
        text.set_line_wrap(True)
        text.set_size_request(descriptionwidth, -1)
        text.set_attributes(attrdescription)
        text.show()
        
        description.pack_start(text, expand, fill, padding)
        
        return description

    def Botones(self, homogeneous, spacing, expand, fill, padding, borderwidth, width, height):
    
        def cerrar(self):
            hilo = threading.Thread(target=cerrarexec, args=(self))
            hilo.start()
            
        def cerrarexec(self):            
            gtk.gdk.threads_enter()
            md = gtk.MessageDialog( parent = None,
                                    flags = 0,
                                    type = gtk.MESSAGE_QUESTION,
                                    buttons = gtk.BUTTONS_YES_NO,
                                    message_format = ConfirmCancelCreateProfileLabel )
            md.set_title(CancelLabel)
            respuesta = md.run()
            md.destroy()
            gtk.gdk.threads_leave()

            if respuesta == gtk.RESPONSE_YES:
                shutil.rmtree(PROFILEDIR+'/'+nombresabor.get_text())
                self.window.destroy()
                gtk.main_quit()

        def ayuda(self):
            hilo = threading.Thread(target=ayudaexec, args=(self))
            hilo.start()

        def ayudaexec(self, widget=None):            
            x = Popen(['/usr/bin/yelp', DOCDIR+'/index.html'], shell=False, stdout=PIPE)
            
        def atras(self):
            hilo = threading.Thread(target=atrasexec, args=(self))
            hilo.start()
            
        def atrasexec(self):
            gtk.gdk.threads_enter()
            main.MainWindow()
            self.window.hide()
            gtk.gdk.threads_leave()

        def adelante(self):
            hilo = threading.Thread(target=adelanteexec, args=(self))
            hilo.start()
            
        def adelanteexec(self, data=None):
            def testconnection(self):
                try:
                    response = urllib2.urlopen(AlwaysOnWebPage, timeout=1)
                    return True
                except urllib2.URLError as err: pass
                return False
                    
            if os.path.isdir(PROFILEDIR+'/'+nombresabor.get_text()):
                boton_siguiente.set_sensitive(False)
                boton_atras.set_sensitive(False)

                gtk.gdk.threads_enter()
                md = gtk.MessageDialog( parent = None,
                                        flags = 0,
                                        type = gtk.MESSAGE_ERROR,
                                        buttons = gtk.BUTTONS_CLOSE,
                                        message_format = ProfileExists )
                md.run()
                md.destroy()
                gtk.gdk.threads_leave()

            elif testconnection(self) == False:
                gtk.gdk.threads_enter()
                md = gtk.MessageDialog( parent = None,
                                        flags = 0,
                                        type = gtk.MESSAGE_ERROR,
                                        buttons = gtk.BUTTONS_CLOSE,
                                        message_format = LooksLikeNoInternetLabel)
                md.set_title(LooksLikeNoInternetTitle)
                md.run()
                md.destroy()
                gtk.gdk.threads_leave()

            else:
                gtk.gdk.threads_enter()
                os.makedirs(PROFILEDIR+'/'+nombresabor.get_text())
                boton_siguiente.set_sensitive(True)
                boton_atras.set_sensitive(True)
                profile2.Profile_2()
                self.window.hide()
                gtk.gdk.threads_leave()    

        botones = gtk.HBox(homogeneous, spacing)
        botones.set_border_width(borderwidth)

        boton_cerrar = gtk.Button(stock=gtk.STOCK_CLOSE)
        boton_cerrar.set_size_request(width, height)
        boton_cerrar.connect("clicked", cerrar)
        botones.pack_start(boton_cerrar, expand, fill, padding)
        boton_cerrar.show()

        boton_ayuda = gtk.Button(stock=gtk.STOCK_HELP)             
        boton_ayuda.connect("clicked", ayuda)
        boton_ayuda.set_size_request(width, height)
        botones.pack_start(boton_ayuda, expand, fill, padding)
        boton_ayuda.show()

        space = gtk.HSeparator()
        botones.pack_start(space, expand, fill, 180)

        boton_atras = gtk.Button(stock=gtk.STOCK_GO_BACK)
        boton_atras.connect("clicked", atras)
        boton_atras.set_size_request(width, height)
        botones.pack_start(boton_atras, expand, fill, padding)
        boton_atras.show()

        boton_adelante = gtk.Button(stock=gtk.STOCK_GO_FORWARD)
        boton_adelante.connect("clicked", adelante)
        boton_adelante.set_size_request(width, height)
        botones.pack_start(boton_adelante, expand, fill, padding)
        boton_adelante.show()

        return botones

    def __init__(self):
        
        self.window = gtk.Window()
        self.window.set_border_width(0)
        self.window.set_title(CreateProfileTitle)
        self.window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        self.window.set_size_request(WindowWidth, WindowHeight)
        self.window.set_resizable(False)
        self.window.connect("destroy", gtk.main_quit)
        self.window.set_icon_from_file(ICONDIR+'/48x48/apps/c-s-gui.png')
        
        self.outbox = gtk.VBox(False, 0)
        self.swindow = gtk.ScrolledWindow()
        self.swindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.swindow.set_border_width(10)
        self.vbox = gtk.VBox(False, 0)
        
        self.box = self.Banner(False, 0, False, False, 0, 0, GUIDIR+'/images/banner.png')
        self.outbox.pack_start(self.box, False, False, 0)
        
        self.box = self.Ask(False, 0, False, False, 0, 5, CreateProfileSaborNameLabel)
        self.vbox.pack_start(self.box, False, False, 0)
        
        self.box = self.Entry(False, 0, False, False, 0, 5, 18, 'nombre-sabor', '^[a-z-]*$')
        self.vbox.pack_start(self.box, False, False, 0)
        
        self.box = self.Description(False, 0, False, False, 0, 5, CreateProfileSaborNameDesc)
        self.vbox.pack_start(self.box, False, False, 0)
        
        self.swindow.add_with_viewport(self.vbox)
        self.outbox.add(self.swindow)
        
        self.separator = gtk.HSeparator()
        self.outbox.pack_start(self.separator, False, False, 0)
        
        self.box = self.Botones(False, 0, False, False, 0, 5, 80, 30)
        self.outbox.pack_start(self.box, False, False, 0)
        
        self.window.add(self.outbox)
        self.window.show_all()

if __name__ == "__main__":
    app = Profile_1()
    gtk.main()
