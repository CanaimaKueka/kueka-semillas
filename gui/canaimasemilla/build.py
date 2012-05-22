#!/usr/bin/env python
#-*- coding: UTF-8 -*-

# Librerías Globales
import os, sys, pygtk, gtk, threading, gobject, urllib2, pango
from subprocess import Popen, PIPE, STDOUT

# Librerías Locales
import main
from library.strings import *
from library.localization import *
from config import *

class BuildImage():

    def Banner(self, homogeneous, spacing, expand, fill, padding, borderwidth, imagefile):
        banner = gtk.HBox(homogeneous, spacing)
        banner.set_border_width(borderwidth)

        image = gtk.Image()
        image.set_from_file(imagefile)
        image.show()
        
        banner.pack_start(image, expand, fill, padding)

        return banner

    def Intro(self, homogeneous, spacing, expand, fill, padding, borderwidth, textblock):
        intro = gtk.HBox(homogeneous, spacing)
        intro.set_border_width(borderwidth)

        introwidth = window_width - (borderwidth*2)

        attrintro = pango.AttrList()
        size = pango.AttrSize(8500, 0, -1)
        attrintro.insert(size)

        descripcion = gtk.Label()
        descripcion.set_markup(textblock)
        descripcion.set_line_wrap(True)
        descripcion.set_size_request(introwidth, -1)
        descripcion.set_attributes(attrintro)
        descripcion.show()
        
        intro.pack_start(descripcion, expand, fill, padding)
        
        return intro
        
    def Title(self, homogeneous, spacing, expand, fill, padding, borderwidth, textblock):
        title = gtk.HBox(homogeneous, spacing)
        title.set_border_width(borderwidth)

        titlewidth = window_width - (borderwidth*2)
        
        attrtitle = pango.AttrList()
        size = pango.AttrSize(15000, 0, -1)
        attrtitle.insert(size)
        
        descripcion = gtk.Label()
        descripcion.set_markup(textblock)
        descripcion.set_line_wrap(True)
        descripcion.set_size_request(titlewidth, -1)
        descripcion.set_attributes(attrtitle)
        descripcion.show()
        
        title.pack_start(descripcion, expand, fill, padding)
        
        return title

    def Ask(self, homogeneous, spacing, expand, fill, padding, borderwidth, textblock):
        ask = gtk.HBox(homogeneous, spacing)
        ask.set_border_width(borderwidth)

        askwidth = window_width - (borderwidth*2)

        descripcion = gtk.Label()
        descripcion.set_markup(textblock)
        descripcion.set_line_wrap(True)
        descripcion.set_size_request(askwidth, -1)
        descripcion.show()
        
        ask.pack_start(descripcion, expand, fill, padding)
        
        return ask

    def Medio(self, homogeneous, spacing, expand, fill, padding, borderwidth):
    
        global img
        global iso
        global hybrid

        bigmedio = gtk.HBox(homogeneous, spacing)
        bigmedio.set_border_width(borderwidth)
        
        space = gtk.HSeparator()
        bigmedio.pack_start(space, expand, fill, 30)

        medio = gtk.VBox(homogeneous, spacing)
        medio.set_border_width(borderwidth)
        
        iso = gtk.RadioButton(None, MedioOptionIso)
        iso.set_active(False)
        medio.pack_start(iso, expand, fill, padding)
        iso.show()

        img = gtk.RadioButton(iso, MedioOptionImg)
        img.set_active(False)
        medio.pack_start(img, expand, fill, padding)
        img.show()

        hybrid = gtk.RadioButton(iso, MedioOptionHybrid)
        hybrid.set_active(True)
        medio.pack_start(hybrid, expand, fill, padding)
        hybrid.show()
        
        bigmedio.pack_start(medio, expand, fill, padding)

        return bigmedio
    
    def Arch(self, homogeneous, spacing, expand, fill, padding, borderwidth):
    
        global i386
        global amd64
        
        bigarch = gtk.HBox(homogeneous, spacing)
        bigarch.set_border_width(borderwidth)
        
        space = gtk.HSeparator()
        bigarch.pack_start(space, expand, fill, 30)

        arch = gtk.VBox(homogeneous, spacing)
        arch.set_border_width(borderwidth)
        
        i386 = gtk.RadioButton(None, ArchOptionI386)
        i386.set_active(True)
        arch.pack_start(i386, expand, fill, padding)
        i386.show()

        amd64 = gtk.RadioButton(i386, ArchOptionAmd64)
        amd64.set_active(False)
        arch.pack_start(amd64, expand, fill, padding)
        amd64.show()
        
        bigarch.pack_start(arch, expand, fill, padding)

        return bigarch

    def listarperfiles(self):
        global perfil
        
        perfil = gtk.combo_box_new_text()
        perfil.get_model().clear()
        text = next(os.walk(PROFILEDIR))[1]
        
        for t in text:
            perfil.append_text(t)

    def Sabor(self, homogeneous, spacing, expand, fill, padding, borderwidth):
        sabor = gtk.HBox(homogeneous, spacing)
        sabor.set_border_width(borderwidth)
        
        space = gtk.HSeparator()
        sabor.pack_start(space, expand, fill, 30)
        
        sabor.pack_start(perfil, expand, fill, padding)
        perfil.show()
        
        return sabor
    
    def Progress(self, homogeneous, spacing, expand, fill, padding, borderwidth):
        global pbar
        progress = gtk.HBox(homogeneous, spacing)
        progress.set_border_width(borderwidth)
        pbar = gtk.ProgressBar()
        progress.pack_start(pbar, expand, fill, padding)
        pbar.show()

        return progress

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
                                    message_format = ConfirmCancelBuildImageLabel )
            md.set_title(CancelLabel)
            respuesta = md.run()
            md.destroy()
            gtk.gdk.threads_leave()

            if respuesta == gtk.RESPONSE_YES:          
                x2 = Popen(['/usr/bin/pkill', 'lb'], shell=False, stdout=PIPE)
                x3 = Popen(['/usr/bin/pkill', 'live-build'], shell=False, stdout=PIPE)
                x1 = Popen(['/usr/bin/pkill', 'c-s'], shell=False, stdout=PIPE)
                self.window.destroy()
                gtk.main_quit()

        def ayuda(self):
            hilo = threading.Thread(target=ayudaexec, args=(self))
            hilo.start()

        def ayudaexec(self, widget=None):            
            x = Popen(['/usr/bin/yelp', DOCDIR+'/index.html'], shell=False, stdout=PIPE)
            
        def cancelar(self):
            hilo = threading.Thread(target=cancelarexec, args=(self))
            hilo.start()
        
        def cancelarexec(self):
            gtk.gdk.threads_enter()
            md = gtk.MessageDialog( parent = None,
                                    flags = 0,
                                    type = gtk.MESSAGE_QUESTION,
                                    buttons = gtk.BUTTONS_YES_NO,
                                    message_format = ConfirmCancelBuildImageLabel )
            md.set_title(CancelLabel)
            respuesta = md.run()
            md.destroy()
            gtk.gdk.threads_leave()

            if respuesta == gtk.RESPONSE_YES:          
                x2 = Popen(['/usr/bin/pkill', 'lb'], shell=False, stdout=PIPE)
                x3 = Popen(['/usr/bin/pkill', 'live-build'], shell=False, stdout=PIPE)
                x1 = Popen(['/usr/bin/pkill', 'c-s'], shell=False, stdout=PIPE)
                gtk.gdk.threads_enter()
                main.MainWindow()
                self.window.hide()
                gtk.gdk.threads_leave()
            
        def generar(self):
            hilo = threading.Thread(target=generarexec, args=(self))
            hilo.start()
            
        def generarexec(self, data=None):
            def progressbar(self):
                pbar.pulse()
                return True
                
            def testconnection(self):
                try:
                    response = urllib2.urlopen(AlwaysOnWebPage, timeout=1)
                    return True
                except urllib2.URLError as err: pass
                return False
                
            def testarch(self):
                process = Popen(['/usr/bin/arch'], shell=False, stdout=PIPE)
                nativearch = process.stdout.read().split('\n')[0]
                return nativearch

            if iso.get_active() == True:
                medio = 'iso'
            elif img.get_active() == True:
                medio = 'usb'
            else:
                medio = 'hybrid'
            
            if i386.get_active() == True:
                arquitectura = 'i386'
            else:
                arquitectura = 'amd64'
                
            if perfil.get_active_text():
                sabor = perfil.get_active_text()
            else:
                sabor = ''
                
            if testarch(self) == 'i386' and arquitectura == 'amd64':
                gtk.gdk.threads_enter()
                md = gtk.MessageDialog( parent = None,
                                        flags = 0,
                                        type = gtk.MESSAGE_ERROR,
                                        buttons = gtk.BUTTONS_CLOSE,
                                        message_format = MustSelectArchLabel)
                md.set_title(MustSelectArchTitle)
                md.run()
                md.destroy()
                gtk.gdk.threads_leave()

            elif sabor == '':
                gtk.gdk.threads_enter()
                md = gtk.MessageDialog( parent = None,
                                        flags = 0,
                                        type = gtk.MESSAGE_ERROR,
                                        buttons = gtk.BUTTONS_CLOSE,
                                        message_format = MustSelectSaborLabel)
                md.set_title(MustSelectSaborTitle)
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
            
                timer_1 = gobject.timeout_add(100, progress, self)
                pbar.set_text(BuildingImage)

                iso.set_sensitive(False)
                img.set_sensitive(False)
                i386.set_sensitive(False)
                amd64.set_sensitive(False)
                perfil.set_sensitive(False)
                boton_siguiente.set_sensitive(False)
                boton_cancelar.set_sensitive(True)
                boton_ayuda.set_sensitive(False)
                boton_cerrar.set_sensitive(True)

                buildimage = Popen([BINDIR+'/'+CSBIN, '-a', arquitectura, '-m', medio, '-s', sabor], shell=False, stdout=PIPE)

                if buildimage == 0:
                    pbar.set_fraction(1)
                    pbar.set_text(DoneLabel)
                    timer_2 = gobject.source_remove(timer_1)
                    gtk.gdk.threads_enter()
                    md = gtk.MessageDialog( parent = None,
                                            flags = 0,
                                            buttons = gtk.BUTTONS_OK,
                                            message_format = ImageBuiltSuccessfully % (sabor, sabor))
                    md.set_title(DoneLabel)
                    md.run()
                    md.destroy()
                    gtk.gdk.threads_leave()
                    pbar.set_text(" ")
                                
                if buildimage == 256:
                    pbar.set_fraction(0.0)
                    pbar.set_text(ErrorLabel)
                    timer_2 = gobject.source_remove(timer_1)
                    gtk.gdk.threads_enter()
                    md = gtk.MessageDialog( parent = None,
                                            flags = 0,
                                            type = gtk.MESSAGE_ERROR,
                                            buttons = gtk.BUTTONS_CLOSE,
                                            message_format = ImageBuiltError)
                    md.set_title(ErrorLabel)
                    md.run()
                    md.destroy()
                    gtk.gdk.threads_leave()
                    pbar.set_text(" ")

                if buildimage == 36608:
                    pbar.set_fraction(0.0)
                    pbar.set_text(CancelledLabel)
                    timer_2 = gobject.source_remove(timer_1)
                    gtk.gdk.threads_enter()
                    md = gtk.MessageDialog( parent = None,
                                            flags = 0,
                                            type = gtk.MESSAGE_ERROR,
                                            buttons = gtk.BUTTONS_CLOSE,
                                            message_format = ImageBuiltCancelled % sabor)
                    md.set_title(CancelledLabel)
                    md.run()
                    md.destroy()
                    gtk.gdk.threads_leave()
                    pbar.set_text(" ")
                        
                iso.set_sensitive(True)
                img.set_sensitive(True)
                i386.set_sensitive(True)
                amd64.set_sensitive(True)
                perfil.set_sensitive(True)
                boton_siguiente.set_sensitive(True)
                boton_cancelar.set_sensitive(True)
                boton_ayuda.set_sensitive(True)
                boton_cerrar.set_sensitive(True)

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

        boton_cancelar = gtk.Button(stock=gtk.STOCK_CANCEL)
        boton_cancelar.connect("clicked", cancelar)
        boton_cancelar.set_size_request(width, height)
        botones.pack_start(boton_cancelar, expand, fill, padding)
        boton_cancelar.show()

        boton_generar = gtk.Button(stock=gtk.STOCK_GO_FORWARD)
        boton_generar.connect("clicked", generar)
        boton_generar.set_size_request(width, height)
        botones.pack_start(boton_generar, expand, fill, padding)
        boton_generar.show()
        
        return botones

    def __init__(self):
        self.window = gtk.Window()
        self.window.set_border_width(0)
        self.window.set_title(BuildImageTitle)
        self.window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        self.window.set_size_request(window_width, window_height)
        self.window.set_resizable(False)
        self.window.connect("destroy", gtk.main_quit)
        self.window.set_icon_from_file(ICONDIR+'/48x48/apps/c-s-gui.png')

        self.listarperfiles()
        
        self.vbox = gtk.VBox(False, 5)
        
        self.box = self.Banner(False, 0, False, False, 0, 0, GUIDIR+'/images/banner.png')
        self.vbox.pack_start(self.box, False, False, 0)
        
        self.box = self.Ask(False, 0, False, False, 0, 5, SaborOptionLabel)
        self.vbox.pack_start(self.box, False, False, 0)
        
        self.box = self.Sabor(False, 0, False, False, 0, 0)
        self.vbox.pack_start(self.box, False, False, 0)
        
        self.box = self.Ask(False, 0, False, False, 0, 5, MedioOptionLabel)
        self.vbox.pack_start(self.box, False, False, 0)
        
        self.box = self.Medio(False, 0, False, False, 0, 0)
        self.vbox.pack_start(self.box, False, False, 0)
        
        self.box = self.Ask(False, 0, False, False, 0, 5, ArchOptionLabel)
        self.vbox.pack_start(self.box, False, False, 0)
        
        self.box = self.Arch(False, 0, False, False, 0, 0)
        self.vbox.pack_start(self.box, False, False, 0)
        
        self.separator = gtk.HSeparator()
        self.vbox.pack_start(self.separator, False, False, 0)

        self.box = self.Intro(False, 0, False, False, 0, 5, BuildImageTimeLabel)
        self.vbox.pack_start(self.box, False, False, 0)
        
        self.box = self.Progress(True, 0, True, True, 0, 5)
        self.vbox.pack_start(self.box, True, True, 0)
        
        self.box = self.Intro(False, 0, False, False, 0, 5, BuildImageEndLabel)
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
    app = BuildImage()
    gtk.main()
    sys.exit()
