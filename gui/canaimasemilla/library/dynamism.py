#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gtk, re, threading, Queue, tempfile, urllib2

from config import *
from library.intelligence import *

def Dummy(signaled, class_id):
    pass

def LimitEntry(editable, new_text, new_text_length, position, regex):
    limit = re.compile(regex)
    if limit.match(new_text) is None:
        editable.stop_emission('insert-text')

def CleanEntry(editable, destination):
    textbuffer = destination['destination']
    textbuffer.set_text('')

def ClearEntry(editable, new_text, text):
    content = editable.get_text()
    if content == text:
        editable.set_text('')

def FillEntry(editable, new_text, text):
    content = editable.get_text()
    if content == '':
        editable.set_text(text)

def Toggle(widget, destination):
    widgetcontainer = destination['destination']
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

def ChangeCodename(signaled, class_id):
    dist = class_id.metadist
    db = apt_templates
    codenamecombo = class_id.metacodename
    codenamelist, codenameactive = CodenameList(class_id, dist, db)
    codenamecombo.get_model().clear()
    for item in codenamelist:
        codenamecombo.append_text(item)
    codenamecombo.set_active(codenameactive)

def ChangeRepo(signaled, class_id):
    dist = class_id.metadist.get_active_text()
    repoentry = class_id.metarepo
    exec "newrepotext = "+dist+"_repo"
    repoentry.set_text(newrepotext)

def ChangeSections(signaled, class_id):
    sections = class_id.metareposections
    checklist = SectionList(class_id, class_id.metadist)
    checkdefault = section_default
    children = sections.get_children()
    for child in children:
        sections.remove(child)
    for item in checklist:
        check = gtk.CheckButton(item)
        if item == checkdefault:
            check.set_active(True)
            check.set_sensitive(False)
        check.show()
        sections.pack_start(check, expand, fill, padding)

def AddExtraRepos(signaled, params):
    url = params['url'].get_text()
    branch = params['branch'].get_text()
    sections = params['sections'].get_text().split(' ')
    repo = params['destination'].get_text(*params['destination'].get_bounds())

    if is_valid_url(url):
        thread = threading.Thread(
            target = AddExtraReposThread,
            args = (url, branch, sections, repo)
            )
    else:
        thread = threading.Thread(
            target = ErrorMessage,
            args = (
                PROFILE_OS_EXTRAREPOS_VALIDATE_URL_ERROR,
                PROFILE_OS_EXTRAREPOS_VALIDATE_URL_ERROR_TITLE
                )
            )
    thread.start()

def AddExtraReposThread(url, branch, sections, repo):
    q_window = Queue.Queue()
    q_bar = Queue.Queue()
    savefile = tempfile.NamedTemporaryFile(mode='a')
    for section in sections:
        for arch in supported_arch:
            errorcounter = 0
            l_section = section
            if l_section.find('-') != -1:
                l_section = l_section.replace('-','')
            try:
                response = urllib2.urlopen(url+'/dists/'+branch+'/'+section+'/binary-'+arch+'/Packages.gz')
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
                thread = threading.Thread(
                    target = ErrorMessage,
                    args = (
                        PROFILE_OS_EXTRAREPOS_VALIDATE_URL_ERROR+":\n"+errorcode,
                        PROFILE_OS_EXTRAREPOS_VALIDATE_URL_ERROR_TITLE
                        )
                    )
                thread.start()
            else:
                thread = threading.Thread(
                    target = ProgressWindow,
                    args = (q_window, q_bar, arch, section)
                    )
                thread.start()
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
    
    
    
    
    
    
