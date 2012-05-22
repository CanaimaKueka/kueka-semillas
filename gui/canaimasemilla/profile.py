#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import pygtk, gtk, re, os, sys, threading, urllib2, shutil, pango, tempfile, gobject
from subprocess import Popen, PIPE, STDOUT

# Librerías Locales
import main
from library.strings import *
from library.localization import *
from config import *

class CreateProfile():

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

        askwidth = window_width - (borderwidth*10)

        descripcion = gtk.Label()
        descripcion.set_markup(textblock)
        descripcion.set_line_wrap(True)
        descripcion.set_size_request(askwidth, -1)
        descripcion.show()
        
        ask.pack_start(descripcion, expand, fill, padding)
        
        return ask

    def NombreSabor(self, homogeneous, spacing, expand, fill, padding, borderwidth, maxlength, pretexto, regex):
        def Limit(editable, new_text, new_text_length, position):
            limit = re.compile(regex)
            if limit.match(new_text) is None:
                editable.stop_emission('insert-text')

        def Clear(editable, new_text):
            content = nombresabor.get_text()
            if content == pretexto:
                nombresabor.set_text('')

        def Fill(editable, new_text):
            content = nombresabor.get_text()
            if content == '':
                nombresabor.set_text(pretexto)

        entry = gtk.HBox(homogeneous, spacing)
        entry.set_border_width(borderwidth)

        global nombresabor

        nombresabor = gtk.Entry()
        nombresabor.connect('insert-text', Limit)
        nombresabor.connect('focus-in-event', Clear)
        nombresabor.connect('focus-out-event', Fill)
        nombresabor.set_width_chars(maxlength)
        nombresabor.set_max_length(maxlength)
        nombresabor.set_text(pretexto)
        nombresabor.set_sensitive(True)
        nombresabor.set_editable(True)
        nombresabor.set_visibility(True)
        entry.pack_start(nombresabor, expand, fill, padding)
        nombresabor.show()

        return entry
        
    def NombreAutor(self, homogeneous, spacing, expand, fill, padding, borderwidth, maxlength, pretexto, regex):
        def Limit(editable, new_text, new_text_length, position):
            limit = re.compile(regex)
            if limit.match(new_text) is None:
                editable.stop_emission('insert-text')

        def Clear(editable, new_text):
            content = nombreautor.get_text()
            if content == pretexto:
                nombreautor.set_text('')

        def Fill(editable, new_text):
            content = nombreautor.get_text()
            if content == '':
                nombreautor.set_text(pretexto)

        entry = gtk.HBox(homogeneous, spacing)
        entry.set_border_width(borderwidth)

        global nombreautor

        nombreautor = gtk.Entry()
        nombreautor.connect('insert-text', Limit)
        nombreautor.connect('focus-in-event', Clear)
        nombreautor.connect('focus-out-event', Fill)
        nombreautor.set_width_chars(maxlength)
        nombreautor.set_max_length(maxlength)
        nombreautor.set_text(pretexto)
        nombreautor.set_sensitive(True)
        nombreautor.set_editable(True)
        nombreautor.set_visibility(True)
        entry.pack_start(nombreautor, expand, fill, padding)
        nombresabor.show()

        return entry

    def CorreoAutor(self, homogeneous, spacing, expand, fill, padding, borderwidth, maxlength, pretexto, regex):
        def Limit(editable, new_text, new_text_length, position):
            limit = re.compile(regex)
            if limit.match(new_text) is None:
                editable.stop_emission('insert-text')

        def Clear(editable, new_text):
            content = correoautor.get_text()
            if content == pretexto:
                correoautor.set_text('')

        def Fill(editable, new_text):
            content = correoautor.get_text()
            if content == '':
                correoautor.set_text(pretexto)

        entry = gtk.HBox(homogeneous, spacing)
        entry.set_border_width(borderwidth)

        global correoautor

        correoautor = gtk.Entry()
        correoautor.connect('insert-text', Limit)
        correoautor.connect('focus-in-event', Clear)
        correoautor.connect('focus-out-event', Fill)
        correoautor.set_width_chars(maxlength)
        correoautor.set_max_length(maxlength)
        correoautor.set_text(pretexto)
        correoautor.set_sensitive(True)
        correoautor.set_editable(True)
        correoautor.set_visibility(True)
        entry.pack_start(correoautor, expand, fill, padding)
        correoautor.show()

        return entry

    def WebAutor(self, homogeneous, spacing, expand, fill, padding, borderwidth, maxlength, pretexto, regex):
        def Limit(editable, new_text, new_text_length, position):
            limit = re.compile(regex)
            if limit.match(new_text) is None:
                editable.stop_emission('insert-text')

        def Clear(editable, new_text):
            content = webautor.get_text()
            if content == pretexto:
                webautor.set_text('')

        def Fill(editable, new_text):
            content = webautor.get_text()
            if content == '':
                webautor.set_text(pretexto)

        entry = gtk.HBox(homogeneous, spacing)
        entry.set_border_width(borderwidth)

        global webautor

        webautor = gtk.Entry()
        webautor.connect('insert-text', Limit)
        webautor.connect('focus-in-event', Clear)
        webautor.connect('focus-out-event', Fill)
        webautor.set_width_chars(maxlength)
        webautor.set_max_length(maxlength)
        webautor.set_text(pretexto)
        webautor.set_sensitive(True)
        webautor.set_editable(True)
        webautor.set_visibility(True)
        entry.pack_start(webautor, expand, fill, padding)
        webautor.show()

        return entry

    def ClearEntry(self, editable, new_text, _object, _string):
        content = _object.get_text()
        if content == _string:
            _object.set_text('')

    def FillEntry(self, editable, new_text, _object, _string):
        content = _object.get_text()
        if content == '':
            _object.set_text(_string)

    def LimitEntry(self, editable, new_text, new_text_length, position, regex):
        limit = re.compile(regex)
        if limit.match(new_text) is None:
            editable.stop_emission('insert-text')

    def OnOff(self, widget, widgetcontainer):
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

    def Repo(self, homogeneous, spacing, expand, fill, padding, borderwidth, maxlength, pretexto, regex):

        entry = gtk.HBox(homogeneous, spacing)
        entry.set_border_width(borderwidth)

        global repo

        repo = gtk.Entry()
        repo.connect('insert-text', self.LimitEntry, regex)
        repo.connect('focus-in-event', self.ClearEntry, repo, pretexto)
        repo.connect('focus-out-event', self.FillEntry, repo, pretexto)
        repo.set_width_chars(maxlength)
        repo.set_max_length(maxlength)
        repo.set_text(pretexto)
        repo.set_sensitive(True)
        repo.set_editable(True)
        repo.set_visibility(True)
        entry.pack_start(repo, expand, fill, padding)
        repo.show()

        return entry

    def ExtraRepos(self, homogeneous, spacing, expand, fill, padding,
                        borderwidth, maxlength, lengthurl, lengthrama,
                        lengthseccion, regexurl, regexrama, regexseccion,
                        pretextourl, pretextorama, pretextoseccion):

        def limpiar(self, textbuffer):
            textbuffer.set_text('')

        def agregar(self, homogeneous, spacing, expand, fill, padding, borderwidth, textbuffer, extrareposurl, extrareposrama, extrareposseccion):
            if is_valid_url(extrareposurl.get_text()):
                hilo = threading.Thread(target=agregarexec, args=(self, homogeneous, spacing, expand, fill, padding, borderwidth, textbuffer, extrareposurl, extrareposrama, extrareposseccion))
                hilo.start()
            else:
                hilo = threading.Thread(target=urlerrorexec, args=(self, PROFILE_OS_EXTRAREPOS_VALIDATE_URL_ERROR, PROFILE_OS_EXTRAREPOS_VALIDATE_URL_ERROR_TITLE))
                hilo.start()

        def urlerrorexec(self, message, title):
                gtk.gdk.threads_enter()
                md = gtk.MessageDialog( parent = None,
                                        flags = 0,
                                        type = gtk.MESSAGE_ERROR,
                                        buttons = gtk.BUTTONS_CLOSE,
                                        message_format = message)
                md.set_title(title)
                md.run()
                md.destroy()
                gtk.gdk.threads_leave()

        def DownloadProgress(self, blocknum, bs, size):
            percent = float(blocknum*bs)/size
            if percent >= 1: percent = 1
            pbar.set_fraction(percent)
            return True

        def DownloadWindow(self, homogeneous, spacing, expand, fill, padding, borderwidth, blocknum, bs, size):
            global downloadwindow, pbar
            gtk.gdk.threads_enter()
            downloadwindow = gtk.Dialog()
            downloadwindowarea = downloadwindow.get_content_area()
            downloadwindow.set_position(gtk.WIN_POS_CENTER_ALWAYS)
            downloadwindow.set_size_request(window_width/2, window_height/2)
            downloadwindow.set_resizable(False)

            progress = gtk.VBox(homogeneous, spacing)
            progress.set_border_width(borderwidth)

            descripcion = gtk.Label()
            descripcion.set_markup('hola')
            progress.pack_start(descripcion, expand, fill, padding)

            pbar = gtk.ProgressBar()
            timer = gobject.timeout_add(100, DownloadProgress, self, blocknum, bs, size)
            progress.pack_start(pbar, expand, fill, padding)

            downloadwindowarea.add(progress)
            downloadwindow.show_all()
            gtk.gdk.threads_leave()

        def agregarexec(self, homogeneous, spacing, expand, fill, padding, borderwidth, textbuffer, extrareposurl, extrareposrama, extrareposseccion):
            errorcounter = 0
            buffertext = textbuffer.get_text(*textbuffer.get_bounds())
            urltext = extrareposurl.get_text()
            ramatext = extrareposrama.get_text()
            secciontext = extrareposseccion.get_text()
            seccionlist = secciontext.split(' ')
            for section in seccionlist:
                for arch in supported_arch:
                    try:
                        exec "r_"+section+"_"+arch+" = urllib2.urlopen(urltext+'/dists/'+ramatext+'/'+section+'/binary-'+arch+'/Packages')"
                        print response
                    except urllib2.HTTPError as e:
                        errorcode = str(e.code)
                        errorcounter += 1
                    except urllib2.URLError as e:
                        errorcode = str(e.code)
                        errorcounter += 1
                    except IOError as e:
                        errorcode = str(e.errno)+': '+str(e.strerror)
                        errorcounter += 1
                    except ValueError as e:
                        errorcode = str(e)
                        errorcounter += 1
                    except TypeError as e:
                        errorcode = str(e)
                        errorcounter += 1
                    except:
                        errorcode = str(sys.exc_info()[0])
                        errorcounter += 1
                    else: pass

            if errorcounter > 0 :
                hilo = threading.Thread(target=urlerrorexec, args=(self, errorcode, 'chao'))
                hilo.start()
            else:
                headers = response.info()
                savefile = tempfile.NamedTemporaryFile(mode='a', delete=False)
                savefilename = savefile.name
                bs = 1024*8
                size = -1
                read = 0
                blocknum = 0
                if "content-length" in headers:
                    size = int(headers["Content-Length"])
                DownloadWindow(self, homogeneous, spacing, expand, fill, padding, borderwidth, blocknum, bs, size)
                while True:
                    block = response.read(bs)
                    if not block: break
                    read += len(block)
                    savefile.seek(0)
                    savefile.write(block)
                    savefile.flush()
                    blocknum += 1
                    DownloadProgress(self, blocknum, bs, size)

                if not re.search(buffertext, 'deb '+urltext+' '+ramatext+' '+secciontext):
                    print 'no esta'
                    if size >= 0 and read < size:
                        raise IOError("incomplete retrieval error", "got only %d bytes out of %d" % (read,size))
                    else:
                        textbuffer.set_text(buffertext+'deb '+urltext+' '+ramatext+' '+secciontext+'\n')
            savefile.close()
            response.close()

        extrareposbox = gtk.VBox(homogeneous, spacing)

        checkrepos = gtk.CheckButton(PROFILE_OS_EXTRAREPOS_CHECK)
        checkrepos.set_border_width(borderwidth)
        checkrepos.connect('toggled', self.OnOff, extrareposbox)
        checkrepos.show()

        extrareposbox.pack_start(checkrepos, expand, fill, padding)

        scrolledwindow = gtk.ScrolledWindow()
        scrolledwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

        global textbuffer
        marco = gtk.Frame()
        marco.set_border_width(borderwidth)
        textview = gtk.TextView()
        textbuffer = textview.get_buffer()
        textview.set_wrap_mode(gtk.WRAP_WORD)
        textview.set_editable(False)
        scrolledwindow.add(textview)
        marco.add(scrolledwindow)

        extrareposbox.pack_start(marco, expand, fill, padding)

        entry = gtk.HBox(homogeneous, spacing)
        entry.set_border_width(borderwidth)

        extrareposurl = gtk.Entry()
        extrareposurl.set_text(pretextourl)
        extrareposurl.set_width_chars(lengthurl)
        extrareposurl.set_max_length(maxlength)
        extrareposurl.connect('insert-text', self.LimitEntry, regexurl)
        extrareposurl.connect('focus-in-event', self.ClearEntry, extrareposurl, pretextourl)
        extrareposurl.connect('focus-out-event', self.FillEntry, extrareposurl, pretextourl)
        entry.pack_start(extrareposurl, expand, fill, padding)
        extrareposurl.show()

        space = gtk.HSeparator()
        entry.pack_start(space, expand, fill, padding)

        extrareposrama = gtk.Entry()
        extrareposrama.set_text(pretextorama)
        extrareposrama.set_width_chars(lengthrama)
        extrareposrama.set_max_length(maxlength)
        extrareposrama.connect('insert-text', self.LimitEntry, regexrama)
        extrareposrama.connect('focus-in-event', self.ClearEntry, extrareposrama, pretextorama)
        extrareposrama.connect('focus-out-event', self.FillEntry, extrareposrama, pretextorama)
        entry.pack_start(extrareposrama, expand, fill, padding)
        extrareposrama.show()

        space = gtk.HSeparator()
        entry.pack_start(space, expand, fill, padding)

        extrareposseccion = gtk.Entry()
        extrareposseccion.set_text(pretextoseccion)
        extrareposseccion.set_width_chars(lengthseccion)
        extrareposseccion.set_max_length(maxlength)
        extrareposseccion.connect('insert-text', self.LimitEntry, regexseccion)
        extrareposseccion.connect('focus-in-event', self.ClearEntry, extrareposseccion, pretextoseccion)
        extrareposseccion.connect('focus-out-event', self.FillEntry, extrareposseccion, pretextoseccion)
        entry.pack_start(extrareposseccion, expand, fill, padding)
        extrareposseccion.show()

        space = gtk.HSeparator()
        entry.pack_start(space, expand, fill, borderwidth)

        boton_limpiar = gtk.Button(stock=gtk.STOCK_CLEAR)
        boton_limpiar.connect('clicked', limpiar, textbuffer)

        boton_agregar = gtk.Button(stock=gtk.STOCK_ADD)
        boton_agregar.connect('clicked', agregar, homogeneous, spacing, expand, fill, padding, borderwidth, textbuffer, extrareposurl, extrareposrama, extrareposseccion)
        entry.pack_start(boton_agregar, expand, fill, padding)
        entry.pack_start(boton_limpiar, expand, fill, padding)

        extrareposbox.pack_start(entry, expand, fill, padding)

        self.OnOff(checkrepos, extrareposbox)
        return extrareposbox

    def Description(self, homogeneous, spacing, expand, fill, padding, borderwidth, textblock):
        description = gtk.HBox(homogeneous, spacing)
        description.set_border_width(borderwidth)

        descriptionwidth = window_width - (borderwidth*10)
        
        attrdescription = pango.AttrList()
        size = pango.AttrSize(8000, 0, -1)
        attrdescription.insert(size)
        
        text = gtk.Label()
        text.set_markup(textblock)
        text.set_line_wrap(True)
        text.set_size_request(descriptionwidth, -1)
        text.set_attributes(attrdescription)
        text.show()
        
        description.pack_start(text, expand, fill, padding)
        
        return description

    def Distro(self, homogeneous, spacing, expand, fill, padding, borderwidth):
        caja = gtk.HBox(homogeneous, spacing)
        caja.set_border_width(borderwidth)

        global distro
        distro = gtk.combo_box_new_text()
        for t in cs_distros:
            distro.append_text(t)
        distro.set_active(2)
        distro.connect('changed', self.Change)
        distro.show()

        caja.pack_start(distro, expand, fill, padding)

        return caja

    def Locale(self, homogeneous, spacing, expand, fill, padding, borderwidth):
        caja = gtk.HBox(homogeneous, spacing)
        caja.set_border_width(borderwidth)

        global locale
        locale = gtk.combo_box_new_text()

        with open(supported_locales, 'r') as localelist:
            for line in localelist:
                localecode = line.split()
                locale.append_text(localecode[0])
        locale.set_active(2)
        locale.connect('changed', self.Change)
        locale.show()

        caja.pack_start(locale, expand, fill, padding)

        return caja

    def Sections(self, homogeneous, spacing, expand, fill, padding, borderwidth):
        
        bigsections = gtk.HBox(homogeneous, spacing)
        bigsections.set_border_width(borderwidth)
        
        space = gtk.HSeparator()
        bigsections.pack_start(space, expand, fill, 30)
        
        global reposections
        
        reposections = gtk.VBox(homogeneous, spacing)
        reposections.set_border_width(borderwidth)
        
        curdistro = distro.get_active_text()
        exec 'cursections = '+curdistro+'_sections'
        for section in cursections:
            label = section
            if section == 'non-free':
                section = 'nonfree'
                label = 'non-free'
            if section == 'main':
                global mainsection
                mainsection = gtk.CheckButton('main')
                mainsection.set_active(True)
                mainsection.set_sensitive(False)
                mainsection.show()
                reposections.pack_start(mainsection, expand, fill, padding)
            else:
                exec 'global '+section+'section\n'+section+'section = gtk.CheckButton(label)\n'+section+'section.set_active(False)\n'+section+'section.show()\nreposections.pack_start('+section+'section, expand, fill, padding)'
        bigsections.pack_start(reposections, expand, fill, padding)
        
        return bigsections

    def Change(self, distro):
        children = reposections.get_children()
        for child in children:
            reposections.remove(child)
        curdistro = distro.get_active_text()
        exec 'currepo = '+curdistro+'_repo'
        repo.set_text(currepo)
        exec 'cursections = '+curdistro+'_sections'
        for section in cursections:
            label = section
            if section == 'non-free':
                section = 'nonfree'
                label = 'non-free'
            if section == 'main':
                global mainsection
                mainsection = gtk.CheckButton('main')
                mainsection.set_active(True)
                mainsection.set_sensitive(False)
                mainsection.show()
                reposections.pack_start(mainsection)
            else:
                exec 'global '+section+'section\n'+section+'section = gtk.CheckButton(label)\n'+section+'section.set_active(False)\n'+section+'section.show()\nreposections.pack_start('+section+'section)'
                
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
        self.window.set_title(PROFILE_TITLE)
        self.window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        self.window.set_size_request(window_width, window_height)
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
        
        self.box = self.Ask(False, 0, False, False, 0, 5, PROFILE_NOMBRE_SABOR_1)
        self.vbox.pack_start(self.box, False, False, 0)
        
        self.box = self.NombreSabor(False, 0, False, False, 0, 0, 18, default_profile_name, '^[a-z-]*$')
        self.vbox.pack_start(self.box, False, False, 0)
        
        self.box = self.Description(False, 0, False, False, 0, 5, PROFILE_NOMBRE_SABOR_2)
        self.vbox.pack_start(self.box, False, False, 0)
        
        self.separator = gtk.HSeparator()
        self.vbox.pack_start(self.separator, False, False, 0)
        
        self.box = self.Ask(False, 0, False, False, 0, 5, PROFILE_NOMBRE_AUTOR_1)
        self.vbox.pack_start(self.box, False, False, 0)
        
        self.box = self.NombreAutor(False, 0, False, False, 0, 0, 60, default_profile_author, '\w')
        self.vbox.pack_start(self.box, False, False, 0)
        
        self.box = self.Description(False, 0, False, False, 0, 5, PROFILE_NOMBRE_AUTOR_2)
        self.vbox.pack_start(self.box, False, False, 0)
        
        self.separator = gtk.HSeparator()
        self.vbox.pack_start(self.separator, False, False, 0)
        
        self.box = self.Ask(False, 0, False, False, 0, 5, PROFILE_CORREO_AUTOR_1)
        self.vbox.pack_start(self.box, False, False, 0)
        
        self.box = self.CorreoAutor(False, 0, False, False, 0, 0, 60, default_profile_email, '^[_.@0-9A-Za-z-]*$')
        self.vbox.pack_start(self.box, False, False, 0)
        
        self.box = self.Description(False, 0, False, False, 0, 5, PROFILE_CORREO_AUTOR_2)
        self.vbox.pack_start(self.box, False, False, 0)
        
        self.separator = gtk.HSeparator()
        self.vbox.pack_start(self.separator, False, False, 0)
        
        self.box = self.Ask(False, 0, False, False, 0, 5, PROFILE_WEB_AUTOR_1)
        self.vbox.pack_start(self.box, False, False, 0)
        
        self.box = self.WebAutor(False, 0, False, False, 0, 0, 60, default_profile_url, '[-A-Za-z0-9+&@#/%?=~_()|!:,.;]')
        self.vbox.pack_start(self.box, False, False, 0)
        
        self.box = self.Description(False, 0, False, False, 0, 5, PROFILE_WEB_AUTOR_2)
        self.vbox.pack_start(self.box, False, False, 0)
        
        self.separator = gtk.HSeparator()
        self.vbox.pack_start(self.separator, False, False, 0)
        
        self.box = self.Ask(False, 0, False, False, 0, 5, PROFILE_META_DISTRO_1)
        self.vbox.pack_start(self.box, False, False, 0)
        
        self.box = self.Distro(False, 0, False, False, 0, 0)
        self.vbox.pack_start(self.box, False, False, 0)
        
        self.box = self.Description(False, 0, False, False, 0, 5, PROFILE_META_DISTRO_2)
        self.vbox.pack_start(self.box, False, False, 0)
        
        self.separator = gtk.HSeparator()
        self.vbox.pack_start(self.separator, False, False, 0)
        
        self.box = self.Ask(False, 0, False, False, 0, 5, PROFILE_META_REPO_1)
        self.vbox.pack_start(self.box, False, False, 0)
        
        self.box = self.Repo(False, 0, False, False, 0, 0, 60, canaima_repo, '^[-A-Za-z0-9+&@#/%?=~_()|!:,.;]*$')
        self.vbox.pack_start(self.box, False, False, 0)
        
        self.box = self.Description(False, 0, False, False, 0, 5, PROFILE_META_REPO_2)
        self.vbox.pack_start(self.box, False, False, 0)
        
        self.separator = gtk.HSeparator()
        self.vbox.pack_start(self.separator, False, False, 0)
        
        self.box = self.Ask(False, 0, False, False, 0, 5, PROFILE_META_REPOSECTIONS_1)
        self.vbox.pack_start(self.box, False, False, 0)
        
        self.box = self.Sections(False, 0, False, False, 0, 0)
        self.vbox.pack_start(self.box, False, False, 0)
        
        self.box = self.Description(False, 0, False, False, 0, 5, PROFILE_META_REPOSECTIONS_2)
        self.vbox.pack_start(self.box, False, False, 0)
        
        self.separator = gtk.HSeparator()
        self.vbox.pack_start(self.separator, False, False, 0)
        
        self.box = self.Ask(False, 0, False, False, 0, 5, PROFILE_OS_LOCALE_1)
        self.vbox.pack_start(self.box, False, False, 0)
        
        self.box = self.Locale(False, 0, False, False, 0, 0)
        self.vbox.pack_start(self.box, False, False, 0)
        
        self.box = self.Description(False, 0, False, False, 0, 5, PROFILE_OS_LOCALE_2)
        self.vbox.pack_start(self.box, False, False, 0)
        
        self.separator = gtk.HSeparator()
        self.vbox.pack_start(self.separator, False, False, 0)
        
        self.box = self.ExtraRepos(False, 0, False, False, 0, 3, 60, 37, 10, 17,
            '^[-A-Za-z0-9+&@#/%?=~_()|!:,.;]*$', '^[A-Za-z0-9-]*$', '^[A-Za-z0-9\ -]*$', PROFILE_OS_EXTRAREPOS_URL,
            PROFILE_OS_EXTRAREPOS_RAMA, PROFILE_OS_EXTRAREPOS_SECCION)
        self.vbox.pack_start(self.box, False, False, 0)
        
        self.box = self.Description(False, 0, False, False, 0, 5, PROFILE_OS_EXTRAREPOS_2)
        self.vbox.pack_start(self.box, False, False, 0)
        
        self.separator = gtk.HSeparator()
        self.vbox.pack_start(self.separator, False, False, 0)
        
        self.swindow.add_with_viewport(self.vbox)
        self.outbox.add(self.swindow)

        self.separator = gtk.HSeparator()
        self.outbox.pack_start(self.separator, False, False, 0)

        self.box = self.Botones(False, 0, False, False, 0, 5, 80, 30)
        self.outbox.pack_start(self.box, False, False, 0)
        
        self.window.add(self.outbox)
        self.window.show_all()

if __name__ == "__main__":
    gtk.gdk.threads_init()
    init_localization()
    app = CreateProfile()
    gtk.main()
    sys.exit()
