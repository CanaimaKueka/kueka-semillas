#!/usr/bin/env python
#-*- coding: UTF-8 -*-

# Librerías Globales
import os, pygtk, gtk, threading, gobject, urllib2
from subprocess import Popen, PIPE, STDOUT

# Librerías Locales
import main
from library.strings import *
from library.localization import *
from config import *

gtk.gdk.threads_init()

class BuildImage():

    def cs_build_banner(self, homogeneous, spacing, expand, fill, padding):
        banner = gtk.HBox(homogeneous, spacing)
        banner.set_border_width(0)
        imagen = gtk.Image()
        imagen.set_from_file(GUIDIR+'/images/banner.png')
        banner.pack_start(imagen, False, False, 0)
        imagen.show()

        return banner

    def cs_build_intro(self, homogeneous, spacing, expand, fill, padding):
        caja = gtk.HBox(homogeneous, spacing)
        descripcion = gtk.Label()
        descripcion.set_use_markup(True)
        descripcion.set_markup(BuildImageIntro)
        descripcion.set_line_wrap(True)
        descripcion.set_size_request(700, -1)
        caja.pack_start(descripcion, False, False, 0)
        descripcion.show()
        
        return caja
            
    def cs_build_medio_label(self, homogeneous, spacing, expand, fill, padding):
        caja = gtk.HBox(homogeneous, spacing)
        descripcion = gtk.Label()
        descripcion.set_use_markup(True)
        descripcion.set_markup(MedioOptionLabel)
        caja.pack_start(descripcion, False, False, 0)
        descripcion.show()
        
        return caja

    def cs_build_medio(self, homogeneous, spacing, expand, fill, padding):
    
        global img
        global iso
        global hybrid
        
        caja = gtk.VBox(homogeneous, spacing)
        
        iso = gtk.RadioButton(None, MedioOptionIso)
        iso.set_active(True)
        caja.pack_start(iso, True, True, 0)
        iso.show()

        img = gtk.RadioButton(iso, MedioOptionImg)
        img.set_active(False)
        caja.pack_start(img, True, True, 0)
        img.show()

        hybrid = gtk.RadioButton(iso, MedioOptionHybrid)
        hybrid.set_active(False)
        caja.pack_start(hybrid, True, True, 0)
        hybrid.show()

        return caja
    
    def cs_build_arch_label(self, homogeneous, spacing, expand, fill, padding):
        caja = gtk.HBox(homogeneous, spacing)
        descripcion = gtk.Label()
        descripcion.set_use_markup(True)
        descripcion.set_markup(ArchOptionLabel)
        caja.pack_start(descripcion, False, False, 0)
        descripcion.show()
        
        return caja

    def cs_build_arch(self, homogeneous, spacing, expand, fill, padding):
    
        global i386
        global amd64
        
        caja = gtk.VBox(homogeneous, spacing)
        
        i386 = gtk.RadioButton(None, ArchOptionI386)
        i386.set_active(True)
        caja.pack_start(i386, True, True, 0)
        i386.show()

        amd64 = gtk.RadioButton(i386, ArchOptionAmd64)
        amd64.set_active(False)
        caja.pack_start(amd64, True, True, 0)
        amd64.show()

        return caja

    def cs_build_sabor_label(self, homogeneous, spacing, expand, fill, padding):
        caja = gtk.HBox(homogeneous, spacing)
        descripcion = gtk.Label()
        descripcion.set_use_markup(True)
        descripcion.set_markup(SaborOptionLabel)
        caja.pack_start(descripcion, False, False, 0)
        descripcion.show()
        
        return caja
    
    def listarperfiles(self):
        global perfil
        
        perfil = gtk.combo_box_new_text()
        perfil.get_model().clear()
        text = next(os.walk(PROFILEDIR))[1]
        
        for t in text:
            perfil.append_text(t)

    def cs_build_sabor(self, homogeneous, spacing, expand, fill, padding):
        caja = gtk.HBox(homogeneous, spacing)
        caja.pack_start(perfil, False, False, 0)
        perfil.show()
        
        return caja

    def cs_build_end_label(self, homogeneous, spacing, expand, fill, padding):
        caja = gtk.HBox(homogeneous, spacing)
        descripcion = gtk.Label()
        descripcion.set_use_markup(True)
        descripcion.set_markup(BuildImageEndLabel)
        descripcion.set_justify(gtk.JUSTIFY_CENTER)
        caja.pack_start(descripcion, True, True, 0)
        descripcion.show()

        return caja
    
    def cs_build_progress_bar(self, homogeneous, spacing, expand, fill, padding):
        global pbar
        caja = gtk.HBox(homogeneous, spacing)
        pbar = gtk.ProgressBar()
        caja.pack_start(pbar, True, True, 0)
        pbar.show()

        return caja

    def cs_build_botones(self, homogeneous, spacing, expand, fill, padding):
    
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
                x2 = Popen(['/usr/bin/pkill', 'lb'], shell=True, stdout=PIPE)
                x3 = Popen(['/usr/bin/pkill', 'live-build'], shell=True, stdout=PIPE)
                x1 = Popen(['/usr/bin/pkill', 'c-s'], shell=True, stdout=PIPE)
                self.window.destroy()
                gtk.main_quit()

        def ayuda(self):
            hilo = threading.Thread(target=ayudaexec, args=(self))
            hilo.start()

        def ayudaexec(self, widget=None):            
            x = Popen(['/usr/bin/yelp', DOCDIR+'/index.html'], shell=True, stdout=PIPE)
            
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
                x2 = Popen(['/usr/bin/pkill', 'lb'], shell=True, stdout=PIPE)
                x3 = Popen(['/usr/bin/pkill', 'live-build'], shell=True, stdout=PIPE)
                x1 = Popen(['/usr/bin/pkill', 'c-s'], shell=True, stdout=PIPE)
            
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
                process = Popen(['/usr/bin/arch'], shell=True, stdout=PIPE)
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

                buildimage = Popen([BINDIR+'/'+CSBIN, '-a', arquitectura, '-m', medio, '-s', sabor], shell=True, stdout=PIPE)

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

        caja = gtk.HBox(homogeneous, spacing)
        caja.set_border_width(5)
        
        # === BOTÓN CERRAR ===================================================
        # --------------------------------------------------------------------
        boton_cerrar = gtk.Button(stock=gtk.STOCK_CLOSE)
        boton_cerrar.set_size_request(80, 30)
        boton_cerrar.connect("clicked", cerrar)
        caja.pack_start(boton_cerrar, False, False, 5)
        boton_cerrar.show()
        
        # === BOTÓN AYUDA ====================================================
        # --------------------------------------------------------------------
        boton_ayuda = gtk.Button(stock=gtk.STOCK_HELP)             
        boton_ayuda.connect("clicked", ayuda)
        boton_ayuda.set_size_request(80, 30)
        caja.pack_start(boton_ayuda, False, False, 5)
        boton_ayuda.show()        
                
        # === BOTÓN CANCELAR =================================================
        # --------------------------------------------------------------------
        boton_cancelar = gtk.Button(stock=gtk.STOCK_CANCEL)             
        boton_cancelar.connect("clicked", cancelar)
        boton_cancelar.set_size_request(80, 30)
        caja.pack_start(boton_cancelar, False, False, 5)
        boton_cancelar.show()
        
        # === BOTÓN GENERAR ==================================================
        # --------------------------------------------------------------------
        boton_generar = gtk.Button(stock=gtk.STOCK_GO_FORWARD)             
        boton_generar.connect("clicked", generar)
        boton_generar.set_size_request(80, 30)
        caja.pack_start(boton_generar, False, False, 5)
        boton_generar.show()
        
        return caja

    def __init__(self):
        self.window = gtk.Window()
        self.window.set_border_width(0)
        self.window.set_title(BuildImageTitle)
        self.window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        self.window.set_size_request(700, 550)
        self.window.set_resizable(False)
        self.window.connect("destroy", gtk.main_quit)
        self.window.set_icon_from_file(ICONDIR+'/48x48/apps/c-s-gui.png')

        self.listarperfiles()
        
        self.vbox = gtk.VBox(False, 5)
        
        self.box = self.cs_build_banner(False, 0, False, False, 0)
        self.vbox.pack_start(self.box, False, False, 0)
        
        self.box = self.cs_build_intro(False, 0, False, False, 0)
        self.vbox.pack_start(self.box, False, False, 0)
        
        self.box = self.cs_build_medio_label(False, 0, False, False, 0)
        self.vbox.pack_start(self.box, False, False, 0)
        
        self.box = self.cs_build_medio(False, 0, False, False, 0)
        self.vbox.pack_start(self.box, False, False, 0)
        
        self.box = self.cs_build_arch_label(False, 0, False, False, 0)
        self.vbox.pack_start(self.box, False, False, 0)
        
        self.box = self.cs_build_arch(False, 0, False, False, 0)
        self.vbox.pack_start(self.box, False, False, 0)
        
        self.box = self.cs_build_sabor_label(False, 0, False, False, 0)
        self.vbox.pack_start(self.box, False, False, 0)
        
        self.box = self.cs_build_sabor(False, 0, False, False, 0)
        self.vbox.pack_start(self.box, False, False, 0)
                
        self.box = self.cs_build_end_label(False, 0, False, False, 0)
        self.vbox.pack_start(self.box, False, False, 0)
        
        self.box = self.cs_build_progress_bar(False, 0, False, False, 0)
        self.vbox.pack_start(self.box, True, True, 0)
        
        self.separator = gtk.HSeparator()
        self.vbox.pack_start(self.separator, False, False, 0)
        
        self.box = self.cs_build_botones(False, 0, False, False, 0)
        self.vbox.pack_start(self.box, False, False, 0)
        
        self.window.add(self.vbox)
        self.window.show_all()

if __name__ == "__main__":
    app = BuildImage()
    gtk.main()
