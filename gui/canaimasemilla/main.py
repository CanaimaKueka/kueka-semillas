#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Librerías Globales
import gtk, sys, threading, pango
from subprocess import Popen, PIPE, STDOUT

# Librerías Locales
#import build, profile, test, save
from library.strings import *
from library.localization import *
from config import *

class MainWindow():

    def Banner(self, homogeneous, spacing, expand, fill, padding, borderwidth, imagefile):
        banner = gtk.HBox(homogeneous, spacing)
        banner.set_border_width(borderwidth)
        
        image = gtk.Image()
        image.set_from_file(imagefile)

        banner.pack_start(image, expand, fill, padding)
        image.show()

        return banner
    
    def Intro(self, homogeneous, spacing, expand, fill, padding, borderwidth, width, height, textblock, linewrap):
        intro = gtk.HBox(homogeneous, spacing)
        intro.set_border_width(borderwidth)
        
        descripcion = gtk.Label()
        descripcion.set_markup(textblock)
        descripcion.set_line_wrap(linewrap)
        descripcion.set_size_request(width, height)
        descripcion.set_justify(gtk.JUSTIFY_CENTER)
        
        intro.pack_start(descripcion, expand, fill, padding)
        descripcion.show()
        
        return intro
        
    def Opciones(self, homogeneous, spacing, expand, fill, padding):
    
        def crearperfil(self):
            hilo = threading.Thread(target=crearperfilexec, args=(self))
            hilo.start()

        def crearimagen(self):
            hilo = threading.Thread(target=crearimagenexec, args=(self))
            hilo.start()
            
        def probarimagen(self):
            hilo = threading.Thread(target=probarimagenexec, args=(self))
            hilo.start()

        def grabarimagen(self):
            hilo = threading.Thread(target=grabarimagenexec, args=(self))
            hilo.start()
            
        def crearperfilexec(self, widget=None):
            gtk.gdk.threads_enter()
            #build.BuildImage()
            self.window.hide()
            gtk.gdk.threads_leave()

        def crearimagenexec(self, widget=None):
            gtk.gdk.threads_enter()
            #profile.CreateProfile()
            self.window.hide()
            gtk.gdk.threads_leave()
            
        def probarimagenexec(self, widget=None):
            gtk.gdk.threads_enter()
            #test.TestImage()
            self.window.hide()
            gtk.gdk.threads_leave()

        def grabarimagenexec(self, widget=None):
            gtk.gdk.threads_enter()
            #save.SaveImage()
            self.window.hide()
            gtk.gdk.threads_leave()

        def botoncontenido(self, icono, texto, titulo):
            button = gtk.VBox(False, 0)
            button.set_border_width(2)
            
            image = gtk.Image()
            image.set_from_file(icono)
            image.show()

            attr = pango.AttrList()
            size = pango.AttrSize(20000, 0, -1)
            weight = pango.AttrWeight(700, 0, -1)
            attr.insert(size)
            attr.insert(size)
            
            title = gtk.Label()
            title.set_markup(titulo)
            title.set_justify(gtk.JUSTIFY_CENTER)
            title.set_attributes(attr)
            title.show()
            
            line = gtk.HSeparator()
            line.show()
            
            label = gtk.Label()
            label.set_markup(texto)
            label.set_line_wrap(True)
            label.set_size_request(300, -1)
            label.set_justify(gtk.JUSTIFY_CENTER)
            label.show()
            
            button.pack_start(image, False, False, 0)
            button.pack_start(title, False, False, 0)
            button.pack_start(line, False, False, 0)
            button.pack_start(label, False, False, 0)

            return button

        caja = gtk.VBox(homogeneous, spacing)
        caja.set_border_width(10)

        fila1 = gtk.HBox(homogeneous, spacing)
        fila1.set_border_width(0)
        
        fila2 = gtk.HBox(homogeneous, spacing)
        fila2.set_border_width(0)
        
        boton_cp = gtk.Button()             
        boton_cp.connect("clicked", crearperfil)
        boton_cp.set_size_request(330, 170)
        contenido_cp = botoncontenido(self, GUIDIR+'/images/crear-perfil.png', CrearPerfilLabel, CrearPerfilTitle)
        boton_cp.add(contenido_cp)
        fila1.pack_start(boton_cp, False, False, 5)
        boton_cp.show()
                
        boton_ci = gtk.Button()             
        boton_ci.connect("clicked", crearimagen)
        boton_ci.set_size_request(330, 170)
        contenido_ci = botoncontenido(self, GUIDIR+'/images/crear-imagen.png', CrearImagenLabel, CrearImagenTitle)
        boton_ci.add(contenido_ci)
        fila1.pack_start(boton_ci, False, False, 5)
        boton_ci.show()

        boton_pi = gtk.Button()             
        boton_pi.connect("clicked", probarimagen)
        boton_pi.set_size_request(330, 170)
        contenido_pi = botoncontenido(self, GUIDIR+'/images/probar-imagen.png', ProbarImagenLabel, ProbarImagenTitle)
        boton_pi.add(contenido_pi)
        fila2.pack_start(boton_pi, False, False, 5)
        boton_pi.show()
                
        boton_gi = gtk.Button()             
        boton_gi.connect("clicked", grabarimagen)
        boton_gi.set_size_request(330, 170)
        contenido_gi = botoncontenido(self, GUIDIR+'/images/grabar-imagen.png', GrabarImagenLabel, GrabarImagenTitle)
        boton_gi.add(contenido_gi)
        fila2.pack_start(boton_gi, False, False, 5)
        boton_gi.show()
        
        caja.pack_start(fila1, False, False, 5)
        caja.pack_start(fila2, False, False, 5)
        
        return caja

    def Botones(self, homogeneous, spacing, expand, fill, padding):

        def ayuda(self):
            hilo = threading.Thread(target=ayudaexec, args=(self))
            hilo.start()

        def ayudaexec(self, widget=None):            
            x = Popen(['/usr/bin/yelp', DOCDIR+'/index.html'], shell=True, stdout=PIPE)

        caja = gtk.HBox(homogeneous, spacing)
        caja.set_border_width(5)
        
        boton_cerrar = gtk.Button(stock=gtk.STOCK_CLOSE)
        boton_cerrar.set_size_request(80, 30)
        boton_cerrar.connect("clicked", gtk.main_quit)
        caja.pack_start(boton_cerrar, False, False, 5)
        boton_cerrar.show()

        boton_ayuda = gtk.Button(stock=gtk.STOCK_HELP)             
        boton_ayuda.connect("clicked", ayuda)
        boton_ayuda.set_size_request(80, 30)
        caja.pack_start(boton_ayuda, False, False, 5)
        boton_ayuda.show()
        
        return caja

    def __init__(self):
            
        self.window = gtk.Window()
        self.window.set_border_width(0)
        self.window.set_title(MainWindowTitle)
        self.window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        self.window.set_size_request(WindowWidth, WindowHeight)
        self.window.set_resizable(False)
        self.window.connect("destroy", gtk.main_quit)
        self.window.set_icon_from_file(ICONDIR+'/48x48/apps/c-s-gui.png')
        
        self.vbox = gtk.VBox(False, 5)
        
        self.box = self.Banner(False, 0, False, False, 0, 0, GUIDIR+'/images/banner.png')
        self.vbox.pack_start(self.box, False, False, 0)

        self.separator = gtk.HSeparator()
        self.vbox.pack_start(self.separator, False, False, 0)

        self.box = self.Opciones(False, 0, False, False, 0)
        self.vbox.pack_start(self.box, False, False, 0)
         
        self.separator = gtk.HSeparator()
        self.vbox.pack_start(self.separator, False, False, 0)
        
        self.box = self.Botones(False, 0, False, False, 0)
        self.vbox.pack_start(self.box, False, False, 0)
        
        self.window.add(self.vbox)
        self.window.show_all()

if __name__ == "__main__":
    gtk.gdk.threads_init()
    init_localization()
    app = MainWindow()
    gtk.main()
    sys.exit()
