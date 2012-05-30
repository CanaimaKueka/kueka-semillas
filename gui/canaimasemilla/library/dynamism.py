#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gtk, sys, re, threading, Queue, gzip, urllib2

from config import *

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
    sections = params['sections'].get_text()
    repolist = params['repolist'].get_text(*params['repolist'].get_bounds())
    repolistframe = params['repolist']
    fvalidation = params['fvalidation']
    fok = params['fok']
    ferror = params['ferror']
    fprogresswindow = params['fprogresswindow']
    fprogress = params['fprogress']
    errormessage = params['errormessage']
    errortitle = params['errortitle']
    progressmessage = params['progressmessage']
    progresstitle = params['progresstitle']

    if fvalidation(url):
        thread = threading.Thread(
            target = fok, args = (
                url, branch, sections, repolist, repolistframe,
                ferror, fprogresswindow, fprogress, errormessage,
                errortitle, progressmessage, progresstitle
                )
            )
    else:
        thread = threading.Thread(
            target = ferror,
            args = (errormessage, errortitle)
            )
    thread.start()

def AddExtraReposThread(url, branch, sections, repolist, repolistframe,
                ferror, fprogresswindow, fprogress, errormessage,
                errortitle, progressmessage, progresstitle):

    q_window = Queue.Queue()
    q_bar = Queue.Queue()

    if repolist.find('deb '+url+' '+branch+' '+sections) == -1:
        for section in sections.split(' '):
            for arch in supported_arch:
                bs = 5*10240
                size = -1
                read = 0
                blocknum = 0
                errorcounter = 0
                tempfile = open(apt_extra_tempfile+'.tmp', 'wb')
                print apt_extra_tempfile+'.tmp'

                if section.find('-') != -1:
                    l_section = l_section.replace('-','')
                else:
                    l_section = section

                try:
                    response = urllib2.urlopen(url+'/dists/'+branch+'/'+section+'/binary-'+arch+'/Packages.gz')
                    headers = response.info()
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
                else:
                    pass

                if errorcounter > 0 :
                    thread = threading.Thread(
                        target = ferror,
                        args = (errormessage+":\n"+errorcode, errortitle)
                        )
                    thread.start()
                else:
                    thread = threading.Thread(
                        target = fprogresswindow,
                        args = (
                            q_window, q_bar, arch, section,
                            progressmessage, progresstitle
                            )
                        )
                    thread.start()

                    exec "b_"+l_section+"_"+arch+" = q_bar.get()"
                    exec "w_"+l_section+"_"+arch+" = q_window.get()"

                    if "content-length" in headers:
                        size = int(headers["Content-Length"])

                    while True:
                        block = response.read(bs)
                        if not block: break
                        read += len(block)
                        tempfile.seek(0)
                        tempfile.write(block)
                        tempfile.flush()
                        blocknum += 1
                        exec "thread = threading.Thread(target=fprogress, args=(b_"+l_section+"_"+arch+", blocknum, bs, size))"
                        thread.start()

                    tempfile.close()
                    response.close()

                    tempfile = gzip.open(apt_extra_tempfile+'.tmp', 'rb')
                    savefile = open(apt_extra_tempfile, 'ab')
                    savefile.writelines(tempfile.read())
                    tempfile.close()
                    savefile.close()

    for section in sections:
        for arch in supported_arch:
            exec "w_"+l_section+"_"+arch+".hide_all()"

    if size >= 0 and read < size:
            thread = threading.Thread(
                target = fmessage,
                args = (errormessage+":\n"+errorcode, errortitle)
                )
            thread.start()
    else:
        repolistframe.set_text(repolist+'deb '+url+' '+branch+' '+sections+'\n')

def AddPackages(signaled, params):
    packages = params['packages'].get_text()
    packageslist = params['packageslist'].get_text(*params['packageslist'].get_bounds())
    packageslistframe = params['packageslist']
    fok = params['fok']
    fprogresswindow = params['fprogresswindow']
    fprogress = params['fprogress']
    errormessage = params['errormessage']
    errortitle = params['errortitle']
    progressmessage = params['progressmessage']
    progresstitle = params['progresstitle']

    thread = threading.Thread(
        target = fok, args = (
            packages, packageslist, packageslistframe,
            fprogresswindow, fprogress, errormessage,
            errortitle, progressmessage, progresstitle
            )
        )

def AddPackagesThread(packages, packageslist, packageslistframe,
            fprogresswindow, fprogress, errormessage,
            errortitle, progressmessage, progresstitle):

    q_window = Queue.Queue()
    q_bar = Queue.Queue()

#    for package in packages.split(' '):
#        if packageslist.find(package) == -1:
#            bs = 5*10240
#            size = -1
#            read = 0
#            blocknum = 0
#            errorcounter = 0
#            tempfile = open(apt_extra_tempfile+'.tmp', 'wb')

#                if l_section.find('-') != -1:
#                    l_section = l_section.replace('-','')
#                else:
#                    l_section = section

#                try:
#                    response = urllib2.urlopen(url+'/dists/'+branch+'/'+section+'/binary-'+arch+'/Packages.gz')
#                    headers = response.info()
#                except urllib2.HTTPError as e:
#                    errorcode = str(e.code)
#                    errorcounter += 1
#                except urllib2.URLError as e:
#                    errorcode = str(e.reason)
#                    errorcounter += 1
#                except IOError as e:
#                    errorcode = str(e.errno)+': '+str(e.strerror)
#                    errorcounter += 1
#                except ValueError as e:
#                    errorcode = str(e)
#                    errorcounter += 1
#                except TypeError as e:
#                    errorcode = str(e)
#                    errorcounter += 1
#                except:
#                    errorcode = str(sys.exc_info()[0])
#                    errorcounter += 1
#                else:
#                    pass

#                if errorcounter > 0 :
#                    thread = threading.Thread(
#                        target = ferror,
#                        args = (errormessage+":\n"+errorcode, errortitle)
#                        )
#                    thread.start()
#                else:
#                    thread = threading.Thread(
#                        target = fprogresswindow,
#                        args = (
#                            q_window, q_bar, arch, section,
#                            progressmessage, progresstitle
#                            )
#                        )
#                    thread.start()

#                    exec "b_"+l_section+"_"+arch+" = q_bar.get()"
#                    exec "w_"+l_section+"_"+arch+" = q_window.get()"

#                    if "content-length" in headers:
#                        size = int(headers["Content-Length"])

#                    while True:
#                        block = response.read(bs)
#                        if not block: break
#                        read += len(block)
#                        tempfile.seek(0)
#                        tempfile.write(block)
#                        tempfile.flush()
#                        blocknum += 1
#                        exec "thread = threading.Thread(target=fprogress, args=(b_"+l_section+"_"+arch+", blocknum, bs, size))"
#                        thread.start()

#                    tempfile.close()
#                    response.close()

#                    tempfile = gzip.open(apt_extra_tempfile+'.tmp', 'rb')
#                    savefile = open(apt_extra_tempfile, 'ab')
#                    savefile.writelines(tempfile.read())
#                    tempfile.close()
#                    savefile.close()

#    for section in sections:
#        for arch in supported_arch:
#            exec "w_"+l_section+"_"+arch+".hide_all()"

#    if size >= 0 and read < size:
#            thread = threading.Thread(
#                target = fmessage,
#                args = (errormessage+":\n"+errorcode, errortitle)
#                )
#            thread.start()
#    else:
#        repoframe.set_text(repo+'deb '+url+' '+branch+' '+sections+'\n')
    
    
    
    
    
    
