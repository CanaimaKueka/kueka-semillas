#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import gtk, sys
#import pygtk, gtk, re, os, sys, threading, urllib2, shutil, pango, gobject, Queue, time, tempfile
#from subprocess import Popen, PIPE, STDOUT
#from aptsources.distinfo import DistInfo

## Librerías Locales
#import main
from library.vocabulary import *
from library.creativity import *
from config import *

class CreateProfile():

    def AddExtraReposThread(self, _object, homogeneous, spacing, expand, fill, padding, borderwidth, textbuffer, extrareposurl, extrareposrama, extrareposseccion):
        print self, _object
        q_window = Queue.Queue()
        q_bar = Queue.Queue()
        savefile = tempfile.NamedTemporaryFile(mode='a')
        buffertext = textbuffer.get_text(*textbuffer.get_bounds())
        urltext = extrareposurl.get_text()
        ramatext = extrareposrama.get_text()
        secciontext = extrareposseccion.get_text()
        seccionlist = secciontext.split(' ')
        for section in seccionlist:
            for arch in supported_arch:
                errorcounter = 0
                l_section = section
                if l_section.find('-') != -1:
                    l_section = l_section.replace('-','')
                try:
                    response = urllib2.urlopen(urltext+'/dists/'+ramatext+'/'+section+'/binary-'+arch+'/Packages.gz')
                except urllib2.HTTPError as e:
                    errorcode = str(e.code)
                    errorcounter += 1
                except urllib2.URLError as e:
                    errorcode = str(e.reason)
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
                    hilo = threading.Thread(target=self.ErrorExtraReposThread, args=(PROFILE_OS_EXTRAREPOS_VALIDATE_URL_ERROR+":\n"+errorcode, PROFILE_OS_EXTRAREPOS_VALIDATE_URL_ERROR_TITLE))
                    hilo.start()
                else:
                    hilo = threading.Thread(target=self.DownloadWindow, args=(homogeneous, spacing, expand, fill, padding, borderwidth, q_window, q_bar, arch, section))
                    hilo.start()
                    exec "b_"+l_section+"_"+arch+" = q_bar.get()"
                    exec "w_"+l_section+"_"+arch+" = q_window.get()"

                    bs = 5*10240
                    size = -1
                    read = 0
                    blocknum = 0
                    headers = response.info()
                    if "content-length" in headers:
                        size = int(headers["Content-Length"])

                    while True:
                        block = response.read(bs)
                        if not block: break
                        read += len(block)
                        savefile.seek(0)
                        savefile.write(block)
                        savefile.flush()
                        blocknum += 1
                        exec "hilo = threading.Thread(target=self.DownloadProgress, args=(b_"+l_section+"_"+arch+", blocknum, bs, size))"
                        hilo.start()
        savefile.close()
        response.close()

        for section in seccionlist:
            for arch in supported_arch:
                exec "w_"+l_section+"_"+arch+".hide_all()"

        if buffertext.find('deb '+urltext+' '+ramatext+' '+secciontext) == -1:
            if size >= 0 and read < size:
                hilo = threading.Thread(target=self.ErrorExtraReposThread, args=(PROFILE_OS_EXTRAREPOS_VALIDATE_URL_ERROR_INCOMPLETE+":\n"+errorcode, PROFILE_OS_EXTRAREPOS_VALIDATE_URL_ERROR_TITLE))
                hilo.start()
            else:
                textbuffer.set_text(buffertext+'deb '+urltext+' '+ramatext+' '+secciontext+'\n')

    def UserMessage(self, message, title):
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

    def AddExtraRepos(self, _object, homogeneous, spacing, expand, fill, padding, borderwidth, textbuffer, extrareposurl, extrareposrama, extrareposseccion):
        if is_valid_url(extrareposurl.get_text()):
            hilo = threading.Thread(target=self.AddExtraReposThread, args=(self, homogeneous, spacing, expand, fill, padding, borderwidth, textbuffer, extrareposurl, extrareposrama, extrareposseccion))
            hilo.start()
        else:
            hilo = threading.Thread(target=self.ErrorExtraReposThread, args=(PROFILE_OS_EXTRAREPOS_VALIDATE_URL_ERROR, PROFILE_OS_EXTRAREPOS_VALIDATE_URL_ERROR_TITLE))
            hilo.start()

    def ExtraRepos(self, homogeneous, spacing, expand, fill, padding,
                        borderwidth, maxlength, lengthurl, lengthrama,
                        lengthseccion, regexurl, regexrama, regexseccion,
                        pretextourl, pretextorama, pretextoseccion):
        
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
        boton_limpiar.connect('clicked', self.CleanEntry, textbuffer)

        boton_agregar = gtk.Button(stock=gtk.STOCK_ADD)
        boton_agregar.connect('clicked', self.AddExtraRepos, homogeneous, spacing, expand, fill, padding, borderwidth, textbuffer, extrareposurl, extrareposrama, extrareposseccion)
        entry.pack_start(boton_agregar, expand, fill, padding)
        entry.pack_start(boton_limpiar, expand, fill, padding)

        extrareposbox.pack_start(entry, expand, fill, padding)

        self.OnOff(checkrepos, extrareposbox)
        return extrareposbox

    def AddPackagesThread(class_id, m_url, m_rama, m_section, e_repos, p_list, p_entry):
        q_window = Queue.Queue()
        q_bar = Queue.Queue()
        savefile = open(apt_temp_file, 'w')
        packageslist = packages.get_text(*textbuffer.get_bounds())
        extrareposlist = extrarepos.get_text(*textbuffer.get_bounds())
        packagetext = package.get_text()
        urltext = urlobj.get_text()
        ramatext = extrareposrama.get_text()
        secciontext = extrareposseccion.get_text()
        seccionlist = secciontext.split(' ')
        for section in seccionlist:
            for arch in supported_arch:
                errorcounter = 0
                l_section = section
                if l_section.find('-') != -1:
                    l_section = l_section.replace('-','')
                try:
                    response = urllib2.urlopen(urltext+'/dists/'+ramatext+'/'+section+'/binary-'+arch+'/Packages.gz')
                except urllib2.HTTPError as e:
                    errorcode = str(e.code)
                    errorcounter += 1
                except urllib2.URLError as e:
                    errorcode = str(e.reason)
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
                    hilo = threading.Thread(target=self.ErrorExtraReposThread, args=(PROFILE_OS_EXTRAREPOS_VALIDATE_URL_ERROR+":\n"+errorcode, PROFILE_OS_EXTRAREPOS_VALIDATE_URL_ERROR_TITLE))
                    hilo.start()
                else:
                    hilo = threading.Thread(target=self.DownloadWindow, args=(homogeneous, spacing, expand, fill, padding, borderwidth, q_window, q_bar, arch, section))
                    hilo.start()
                    exec "b_"+l_section+"_"+arch+" = q_bar.get()"
                    exec "w_"+l_section+"_"+arch+" = q_window.get()"

                    bs = 5*10240
                    size = -1
                    read = 0
                    blocknum = 0
                    headers = response.info()
                    if "content-length" in headers:
                        size = int(headers["Content-Length"])

                    while True:
                        block = response.read(bs)
                        if not block: break
                        read += len(block)
                        savefile.seek(0)
                        savefile.write(block)
                        savefile.flush()
                        blocknum += 1
                        exec "hilo = threading.Thread(target=self.DownloadProgress, args=(b_"+l_section+"_"+arch+", blocknum, bs, size))"
                        hilo.start()

        savefile.close()
        response.close()

        for section in seccionlist:
            for arch in supported_arch:
                exec "w_"+l_section+"_"+arch+".hide_all()"

        if buffertext.find('deb '+urltext+' '+ramatext+' '+secciontext) == -1:
            if size >= 0 and read < size:
                hilo = threading.Thread(target=self.ErrorExtraReposThread, args=(PROFILE_OS_EXTRAREPOS_VALIDATE_URL_ERROR_INCOMPLETE+":\n"+errorcode, PROFILE_OS_EXTRAREPOS_VALIDATE_URL_ERROR_TITLE))
                hilo.start()
            else:
                textbuffer.set_text(buffertext+'deb '+urltext+' '+ramatext+' '+secciontext+'\n')

    def AddPackages(class_id, url, branch, section, extra, packagelist, packagename):
        thread = threading.Thread(  target = class_id.AddPackagesDo,
                                    args = (class_id, url, branch, section, extra, packagelist, packagename))
        thread.start()


    def PackagesField(class_id, url, branch, section, extra, mlength, length, regex):

        packagesbox = gtk.VBox(homogeneous, spacing)

        marco, packagelist = class_id.FramedScrolledWindow()
        packagesbox.pack_start(marco, expand, fill, padding)

        entry = gtk.HBox(homogeneous, spacing)
        entry.set_border_width(borderwidth)

        packagename = gtk.Entry()
        packagename.set_width_chars(length)
        packagename.set_max_length(mlength)
        packagename.connect('insert-text', class_id.LimitEntry, regex)
        entry.pack_start(packagename, expand, fill, padding)
        packagename.show()

        space = gtk.HSeparator()
        entry.pack_start(space, expand, fill, borderwidth)

        boton_limpiar = gtk.Button(stock = gtk.STOCK_CLEAR)
        boton_limpiar.connect('clicked', class_id.CleanEntry, packagelist)

        boton_agregar = gtk.Button(stock = gtk.STOCK_ADD)
        boton_agregar.connect('clicked', class_id.AddPackages, url, branch, section, extra, packagelist, packagename)
        entry.pack_start(boton_agregar, expand, fill, padding)
        entry.pack_start(boton_limpiar, expand, fill, padding)

        packagesbox.pack_start(entry, expand, fill, padding)

        return packagesbox

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

        self.banner = Banner(self, GUIDIR+'/images/banner.png')
        self.outbox.pack_start(self.banner, False, False, 0)

        self.profile_name_title = Title(class_id = self, text = PROFILE_PROFILE_NAME_1)
        self.author_name_title = Title(class_id = self, text = PROFILE_AUTHOR_NAME_1)
        self.author_email_title = Title(class_id = self, text = PROFILE_AUTHOR_EMAIL_1)
        self.author_url_title = Title(class_id = self, text = PROFILE_AUTHOR_URL_1)
        self.os_locale_title = Title(class_id = self, text = PROFILE_OS_LOCALE_1)
        self.meta_dist_title = Title(class_id = self, text = PROFILE_META_DIST_1)
        self.meta_codename_title = Title(class_id = self, text = PROFILE_META_CODENAME_1)
        self.meta_repo_title = Title(class_id = self, text = PROFILE_META_REPO_1)
        self.meta_reposections_title = Title(class_id = self, text = PROFILE_META_REPOSECTIONS_1)

        self.profile_name_description = Description(class_id = self, text = PROFILE_PROFILE_NAME_2)
        self.author_name_description = Description(class_id = self, text = PROFILE_AUTHOR_NAME_2)
        self.author_email_description = Description(class_id = self, text = PROFILE_AUTHOR_EMAIL_2)
        self.author_url_description = Description(class_id = self, text = PROFILE_AUTHOR_URL_2)
        self.os_locale_description = Description(class_id = self, text = PROFILE_OS_LOCALE_2)
        self.meta_dist_description = Description(class_id = self, text = PROFILE_META_DIST_2)
        self.meta_codename_description = Description(class_id = self, text = PROFILE_META_CODENAME_2)
        self.meta_repo_description = Description(class_id = self, text = PROFILE_META_REPO_2)
        self.meta_reposections_description = Description(class_id = self, text = PROFILE_META_REPOSECTIONS_2)
        self.os_extrarepos_description = Description(class_id = self, text = PROFILE_OS_EXTRAREPOS_2)

        self.profile_name, self.profilename = TextEntry(
            class_id = self, maxlength = 18, length = 18,
            text = default_profile_name,
            regex = '^[a-z-]*$'
            )

        self.author_name, self.authorname = TextEntry(
            class_id = self, maxlength = 60, length = 60,
            text = default_profile_author,
            regex = '\w'
            )

        self.author_email, self.authoremail = TextEntry(
            class_id = self, maxlength = 60, length = 60,
            text = default_profile_email,
            regex = '^[_.@0-9A-Za-z-]*$'
            )

        self.author_url, self.authorurl = TextEntry(
            class_id = self, maxlength = 60, length = 60,
            text = default_profile_url,
            regex = '^[-A-Za-z0-9+&@#/%?=~_()|!:,.;]*$'
            )

        self.localelist, self.localeactive = LocaleList(
            class_id = self, supported = supported_locales,
            current = os.environ['LC_ALL']
            )

        self.os_locale, self.oslocale = Combo(
            class_id = self, combolist = self.localelist,
            combodefault = self.localeactive, entry = False,
            f_1 = Dummy, f_2 = Dummy, f_3 = Dummy
            )

        self.meta_dist, self.metadist = Combo(
            class_id = self, combolist = cs_distros,
            combodefault = 2, entry = False,
            f_1 = ChangeCodename, f_2 = ChangeRepo, f_3 = ChangeSections
            )

        self.codenamelist, self.codenameactive = CodenameList(
            class_id = self, dist = self.metadist, db = apt_templates
            )

        self.meta_codename, self.metacodename = Combo(
            class_id = self, combolist = self.codenamelist,
            combodefault = self.codenameactive, entry = True,
            f_1 = Dummy, f_2 = Dummy, f_3 = Dummy
            )

        self.meta_repo, self.metarepo = TextEntry(
            class_id = self, maxlength = 60,
            length = 60, text = canaima_repo,
            regex = '^[-A-Za-z0-9+&@#/%?=~_()|!:,.;]*$'
            )

        self.sectionlist = SectionList(class_id = self, dist = self.metadist)

        self.meta_reposections , self.metareposections = CheckList(
            class_id = self, checklist = self.sectionlist, checkdefault = 'main'
            )

        self.os_extrarepos, self.osextrarepos = ScrolledFrame(class_id = self)

        self.os_extrarepos_entries_box = gtk.HBox(homogeneous, spacing)

        self.os_extrarepos_check, self.osextrareposcheck = ActiveCheck(
            class_id = self, text = PROFILE_OS_EXTRAREPOS_CHECK, active = False,
            f_1 = Toggle, p_1 = { 'destination': self.os_extrarepos },
            f_2 = Toggle, p_2 = { 'destination': self.os_extrarepos_entries_box }
            )

        self.os_extrarepos_url, self.osextrareposurl = TextEntry(
            class_id = self, maxlength = 60,
            length = 38, text = PROFILE_OS_EXTRAREPOS_URL,
            regex = '^[-A-Za-z0-9+&@#/%?=~_()|!:,.;]*$'
            )

        self.os_extrarepos_branch, self.osextrareposbranch = TextEntry(
            class_id = self, maxlength = 60,
            length = 10, text = PROFILE_OS_EXTRAREPOS_BRANCH,
            regex = '^[A-Za-z0-9-]*$'
            )

        self.os_extrarepos_sections, self.osextrarepossections = TextEntry(
            class_id = self, maxlength = 60,
            length = 17, text = PROFILE_OS_EXTRAREPOS_SECTIONS,
            regex = '^[A-Za-z0-9\ -]*$'
            )

        self.add_repo_params = {
            'url': self.osextrareposurl,
            'branch': self.osextrareposbranch,
            'sections': self.osextrarepossections,
            'destination': self.osextrarepos
        }

        self.os_extrarepos_add, self.osextrareposadd = ActiveButton(
            class_id = self, text = gtk.STOCK_ADD,
            f_1 = AddExtraRepos, p_1 = self.add_repo_params
            )

        self.os_extrarepos_clean, self.osextrareposclean = ActiveButton(
            class_id = self, text = gtk.STOCK_CLEAR,
            f_1 = CleanEntry, p_1 = { 'destination': self.osextrarepos }
            )

        self.vbox.pack_start(self.profile_name_title, False, False, 0)
        self.vbox.pack_start(self.profile_name, False, False, 0)
        self.vbox.pack_start(self.profile_name_description, False, False, 0)
        self.vbox.pack_start(gtk.HSeparator(), False, False, 0)
        self.vbox.pack_start(self.author_name_title, False, False, 0)
        self.vbox.pack_start(self.author_name, False, False, 0)
        self.vbox.pack_start(self.author_name_description, False, False, 0)
        self.vbox.pack_start(gtk.HSeparator(), False, False, 0)
        self.vbox.pack_start(self.author_email_title, False, False, 0)
        self.vbox.pack_start(self.author_email, False, False, 0)
        self.vbox.pack_start(self.author_email_description, False, False, 0)
        self.vbox.pack_start(gtk.HSeparator(), False, False, 0)
        self.vbox.pack_start(self.author_url_title, False, False, 0)
        self.vbox.pack_start(self.author_url, False, False, 0)
        self.vbox.pack_start(self.author_url_description, False, False, 0)
        self.vbox.pack_start(gtk.HSeparator(), False, False, 0)
        self.vbox.pack_start(self.os_locale_title, False, False, 0)
        self.vbox.pack_start(self.os_locale, False, False, 0)
        self.vbox.pack_start(self.os_locale_description, False, False, 0)
        self.vbox.pack_start(gtk.HSeparator(), False, False, 0)
        self.vbox.pack_start(self.meta_dist_title, False, False, 0)
        self.vbox.pack_start(self.meta_dist, False, False, 0)
        self.vbox.pack_start(self.meta_dist_description, False, False, 0)
        self.vbox.pack_start(gtk.HSeparator(), False, False, 0)
        self.vbox.pack_start(self.meta_codename_title, False, False, 0)
        self.vbox.pack_start(self.meta_codename, False, False, 0)
        self.vbox.pack_start(self.meta_codename_description, False, False, 0)
        self.vbox.pack_start(gtk.HSeparator(), False, False, 0)
        self.vbox.pack_start(self.meta_repo_title, False, False, 0)
        self.vbox.pack_start(self.meta_repo, False, False, 0)
        self.vbox.pack_start(self.meta_repo_description, False, False, 0)
        self.vbox.pack_start(gtk.HSeparator(), False, False, 0)
        self.vbox.pack_start(self.meta_reposections_title, False, False, 0)
        self.vbox.pack_start(self.meta_reposections, False, False, 0)
        self.vbox.pack_start(self.meta_reposections_description, False, False, 0)
        self.vbox.pack_start(gtk.HSeparator(), False, False, 0)
        self.vbox.pack_start(self.os_extrarepos_check, False, False, 0)
        self.vbox.pack_start(self.os_extrarepos, False, False, 0)
        self.os_extrarepos_entries_box.pack_start(self.os_extrarepos_url, False, False, 0)
        self.os_extrarepos_entries_box.pack_start(self.os_extrarepos_branch, False, False, 0)
        self.os_extrarepos_entries_box.pack_start(self.os_extrarepos_sections, False, False, 0)
        self.os_extrarepos_entries_box.pack_start(self.os_extrarepos_add, False, False, 0)
        self.os_extrarepos_entries_box.pack_start(self.os_extrarepos_clean, False, False, 0)
        self.vbox.pack_start(self.os_extrarepos_entries_box, False, False, 0)
        self.vbox.pack_start(self.os_extrarepos_description, False, False, 0)

        Toggle(self.os_extrarepos_check, { 'destination': self.os_extrarepos })
        Toggle(self.os_extrarepos_check, { 'destination': self.os_extrarepos_entries_box })

#        self.separator = gtk.HSeparator()
#        self.vbox.pack_start(self.separator, False, False, 0)
#        
#        self.box = self.ExtraRepos(False, 0, False, False, 0, 3, 60, 37, 10, 17,
#            '^[-A-Za-z0-9+&@#/%?=~_()|!:,.;]*$', '^[A-Za-z0-9-]*$', '^[A-Za-z0-9\ -]*$', PROFILE_OS_EXTRAREPOS_URL,
#            PROFILE_OS_EXTRAREPOS_RAMA, PROFILE_OS_EXTRAREPOS_SECCION)
#        self.vbox.pack_start(self.box, False, False, 0)
#        
#        self.box = self.Description(False, 0, False, False, 0, 5, PROFILE_OS_EXTRAREPOS_2)
#        self.vbox.pack_start(self.box, False, False, 0)
#        
#        self.separator = gtk.HSeparator()
#        self.package_field_title = self.Title(PROFILE_OS_PACKAGES_1)
#        self.package_field = self.PackagesField(
#                                                    url = self.url,
#                                                    branch = self.branch,
#                                                    section = self.section,
#                                                    extra = self.extra,
#                                                    length = 60,
#                                                    mlength = 66,
#                                                    regex = '^[A-Za-z0-9\ -]*$'
#                                                )
#        self.package_field_description = self.Description(PROFILE_OS_PACKAGES_2)

#        self.vbox.pack_start(self.separator, expand, fill, padding)
#        self.vbox.pack_start(self.package_field_title, expand, fill, padding)
#        self.vbox.pack_start(self.package_field, expand, fill, padding)
#        self.vbox.pack_start(self.package_field_description, expand, fill, padding)
#        
#        self.separator = gtk.HSeparator()
#        self.vbox.pack_start(self.separator, False, False, 0)
        
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
    app = CreateProfile()
    gtk.main()
    sys.exit()
