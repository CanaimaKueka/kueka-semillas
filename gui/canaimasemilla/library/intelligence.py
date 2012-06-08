#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gtk, os, re, urllib2, fnmatch, threading, subprocess

from aptsources.distinfo import DistInfo
from config import *

def Dummy(*args, **kwargs):
    pass

def ProfileList(class_id, profiledir):
    profilelist = []
    items = next(os.walk(profiledir))[1]

    for i in items:
        profilelist.append(i)

    return profilelist, 0

def LocaleList(class_id, supported, current):
    localecount = 0
    localeactive = 0
    localelist = []
    with open(supported, 'r') as supportedlocales:
        for item in supportedlocales:
            localecode = item.split()
            localelist.append(localecode[0])
            if localecode[0].upper().replace('-','') == current.upper().replace('-',''):
                localeactive = localecount
            localecount += 1

    return localelist, localeactive

def CodenameList(class_id, dist, db):
    codenamelist = []
    codenameactive = 0
    udist = dist.get_active_text().title()
    d = DistInfo(udist, db)

    for template in d.templates:
        if not template.name in codenamelist:
            codenamelist.append(template.name)

    return codenamelist, codenameactive

def SectionList(class_id, dist):
    text = dist.get_active_text()
    exec "sectionlist = "+text+"_sections"
    return sectionlist

def listdirfullpath(d):
    return [os.path.join(d, f) for f in os.listdir(d)]

def is_valid_url(url):
    regex = re.compile(
        r'^(http|ftp|file):///?'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|[a-zA-Z0-9-]*|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return regex.search(url)

def CleanTempDir(tempdir):
    if not os.path.exists(tempdir):
        mktempdir = os.mkdir(tempdir)

    for path in os.listdir(tempdir):
        if os.path.isfile(tempdir+path) and fnmatch.fnmatch(tempdir+path, '*.gz'):
            os.unlink(tempdir+path)

    return True

class HeadRequest(urllib2.Request):
    def get_method(self):
        return "HEAD"

def replace_all(text, dic):
    for i, j in dic.iteritems():
        text = text.replace(i, j)
    return text
    
def ThreadGenerator(reference, dic):
    if dic['gtk']:
        function = GTKThreadReceiver
        params = dic['function'], dic['params'], dic['hide']
    else:
        function = dic['function']
        params = dic['params']

    thread = threading.Thread(
        target = function,
        args = params
        )
    thread.start()

    return thread

def GTKThreadReceiver(function, params, window):
    gtk.gdk.threads_enter()

    if params:
        fexec = function(*params)
    else:
        fexec = function()

    if window:
        window.hide()

    gtk.gdk.threads_leave()

def ProcessGenerator(command):
    process = subprocess.Popen(command, shell = False, stdout = subprocess.PIPE)
    return process

def KillProcess(process):
    for killed in process:
        murder = subprocess.Popen(['/usr/bin/pkill', killed], shell = False, stdout = subprocess.PIPE)

def GetArch():
    process = subprocess.Popen(['/usr/bin/arch'], shell = False, stdout = subprocess.PIPE)
    arch = process.stdout.read().split('\n')[0]
    return arch

def TestIndexes(sourcestext, archlist, bar, message, progressmessage, download):
    print 'hola'
    print bar.qsize(), message.qsize()
    bar = bar.get()
    message = message.get()
    errorcounter = 0
    sourceslist = []

    for line in sourcestext.split('\n'):
        if line:
            parts = line.split(' ')
            url = parts[1]
            branch = parts[2]
            sections = parts[2:]
            repo = [url, branch, sections]
            sourceslist.append(repo)

    for url, branch, sections in sourceslist:
        for section in sections:
            for arch in archlist:
                read = 0
                blocknum = 0
                contentheader = 0
                message.set_markup(progressmessage % (arch, section))
                requesturl = url+'/dists/'+branch+'/'+section+'/binary-'+arch+'/Packages.gz'

                if download:
                    urlname = replace_all(url, forbidden_filename_chars)
                    pkgcache = tempfile.NamedTemporaryFile(
                        prefix = urlname+'-'+branch+'-',
                        suffix = '-'+section+'_'+arch+'.gz',
                        dir = tempdir, delete = False
                        )

                try:
                    if download:
                        response = urllib2.urlopen(requesturl)
                    else:
                        response = urllib2.urlopen(HeadRequest(requesturl))
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
                    headers = response.info()
                    contentheader = int(headers["Content-Length"])

                if contentheader == 0:
                    errorcode = ''
                    errorcounter += 1

                if download:
                    if errorcounter == 0:
                        while True:
                            block = response.read(bs)
                            if not block:
                                break
                            pkgcache.write(block)
                            pkgcache.flush()
                            os.fsync(pkgcache.fileno())
                            read += len(block)
                            blocknum += 1
                            percent = float(blocknum*bs)/contentheader
                            if percent >= 1:
                                percent = 1
                            bar.set_fraction(percent)

                        pkgcache.close()
                        response.close()

                    if read < contentheader:
                        errorcode = ''
                        errorcounter += 1
                else:
                    bar.pulse()

    return errorcounter, errorcode

def ParseProfileConfig(profile, get):
    conffile = PROFILEDIR+'/'+profile+'/profile.conf'
    f = open(conffile, 'r')
    ask = []
    give = []
    for line in f.readlines():
        for variable in get:
            if line.find(variable+'=') != -1:
                value = replace_all(line, {variable+'=':'', '"':'', '\n':''})
                ask.append(variable)
                give.append(value)
    f.close()
    return dict(zip(ask, give))
