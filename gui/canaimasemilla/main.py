#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Librerías Globales
import gtk, sys, threading, pango
from subprocess import Popen, PIPE, STDOUT

# Librerías Locales
import build, profile, test, save
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

    def Opciones(self, homogeneous, spacing, expand, fill, padding, width, height):
    
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
            profile.CreateProfile()
            self.window.hide()
            gtk.gdk.threads_leave()

        def crearimagenexec(self, widget=None):
            gtk.gdk.threads_enter()
            build.BuildImage()
            self.window.hide()
            gtk.gdk.threads_leave()
            
        def probarimagenexec(self, widget=None):
            gtk.gdk.threads_enter()
            test.TestImage()
            self.window.hide()
            gtk.gdk.threads_leave()

        def grabarimagenexec(self, widget=None):
            gtk.gdk.threads_enter()
            save.SaveImage()
            self.window.hide()
            gtk.gdk.threads_leave()

        def botoncontenido(self, homogeneous, spacing, expand, fill, padding, icono, texto, titulo):
            button = gtk.VBox(homogeneous, spacing)
            button.set_border_width(5)
            
            image = gtk.Image()
            image.set_from_file(icono)
            image.show()

            attrtitle = pango.AttrList()
            size = pango.AttrSize(20000, 0, -1)
            attrtitle.insert(size)
            
            title = gtk.Label()
            title.set_markup(titulo)
            title.set_justify(gtk.JUSTIFY_CENTER)
            title.set_attributes(attrtitle)
            title.show()
            
            line = gtk.HSeparator()
            line.show()

            label = gtk.Label()
            label.set_markup(texto)
            label.set_line_wrap(True)
            label.set_justify(gtk.JUSTIFY_CENTER)
            label.show()
            
            button.pack_start(image, expand, fill, padding)
            button.pack_start(title, expand, fill, padding)
            button.pack_start(line, expand, fill, padding)
            button.pack_start(label, expand, fill, padding)

            return button

        caja = gtk.VBox(homogeneous, spacing)
        caja.set_border_width(10)

        fila1 = gtk.HBox(homogeneous, spacing)
        fila1.set_border_width(0)
        
        fila2 = gtk.HBox(homogeneous, spacing)
        fila2.set_border_width(0)
        
        boton_cp = gtk.Button()             
        boton_cp.connect("clicked", crearperfil)
        boton_cp.set_size_request(width, height)
        contenido_cp = botoncontenido(self, False, 0, False, False, 0, GUIDIR+'/images/crear-perfil.png', CrearPerfilLabel, CrearPerfilTitle)
        boton_cp.add(contenido_cp)
        fila1.pack_start(boton_cp, expand, fill, padding)
        boton_cp.show()
                
        boton_ci = gtk.Button()             
        boton_ci.connect("clicked", crearimagen)
        boton_ci.set_size_request(width, height)
        contenido_ci = botoncontenido(self, False, 0, False, False, 0, GUIDIR+'/images/crear-imagen.png', CrearImagenLabel, CrearImagenTitle)
        boton_ci.add(contenido_ci)
        fila1.pack_start(boton_ci, expand, fill, padding)
        boton_ci.show()

        boton_pi = gtk.Button()             
        boton_pi.connect("clicked", probarimagen)
        boton_pi.set_size_request(width, height)
        contenido_pi = botoncontenido(self, False, 0, False, False, 0, GUIDIR+'/images/probar-imagen.png', ProbarImagenLabel, ProbarImagenTitle)
        boton_pi.add(contenido_pi)
        fila2.pack_start(boton_pi, expand, fill, padding)
        boton_pi.show()
                
        boton_gi = gtk.Button()             
        boton_gi.connect("clicked", grabarimagen)
        boton_gi.set_size_request(width, height)
        contenido_gi = botoncontenido(self, False, 0, False, False, 0, GUIDIR+'/images/grabar-imagen.png', GrabarImagenLabel, GrabarImagenTitle)
        boton_gi.add(contenido_gi)
        fila2.pack_start(boton_gi, expand, fill, padding)
        boton_gi.show()
        
        caja.pack_start(fila1, expand, fill, padding)
        caja.pack_start(fila2, expand, fill, padding)
        
        return caja

    def Botones(self, homogeneous, spacing, expand, fill, padding, borderwidth, width, height):

        def ayuda(self):
            hilo = threading.Thread(target=ayudaexec, args=(self))
            hilo.start()

        def ayudaexec(self, widget=None):
            x = Popen(['/usr/bin/yelp', DOCDIR+'/index.html'], shell = False, stdout = PIPE)

        botones = gtk.HBox(homogeneous, spacing)
        botones.set_border_width(borderwidth)
        
        boton_cerrar = gtk.Button(stock=gtk.STOCK_CLOSE)
        boton_cerrar.set_size_request(width, height)
        boton_cerrar.connect("clicked", gtk.main_quit)
        botones.pack_start(boton_cerrar, expand, fill, padding)
        boton_cerrar.show()

        boton_ayuda = gtk.Button(stock=gtk.STOCK_HELP)             
        boton_ayuda.connect("clicked", ayuda)
        boton_ayuda.set_size_request(width, height)
        botones.pack_start(boton_ayuda, expand, fill, padding)
        boton_ayuda.show()
        
        return botones

    def __init__(self):
            
        self.window = gtk.Window()
        self.window.set_border_width(0)
        self.window.set_title(MainWindowTitle)
        self.window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        self.window.set_size_request(window_width, window_height)
        self.window.set_resizable(False)
        self.window.connect("destroy", gtk.main_quit)
        self.window.set_icon_from_file(ICONDIR+'/48x48/apps/c-s-gui.png')
        
        self.vbox = gtk.VBox(False, 5)
        
        self.box = self.Banner(False, 0, False, False, 0, 0, GUIDIR+'/images/banner.png')
        self.vbox.pack_start(self.box, False, False, 0)

        self.box = self.Opciones(False, 0, False, False, 5, 330, 170)
        self.vbox.pack_start(self.box, False, False, 0)
         
        self.separator = gtk.HSeparator()
        self.vbox.pack_start(self.separator, False, False, 0)
        
        self.box = self.Botones(False, 0, False, False, 0, 5, 80, 30)
        self.vbox.pack_start(self.box, False, False, 0)
        
        self.window.add(self.vbox)
        self.window.show_all()

if __name__ == "__main__":
    gtk.gdk.threads_init()
    init_localization()
    app = MainWindow()
    gtk.main()
    sys.exit()
