#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gtk, os, re, urllib2, fnmatch, threading, subprocess, hashlib, random, gobject, tempfile

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
    else:
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

class ThreadGenerator(threading.Thread):
    def __init__(self, reference, function, params,
                    gtk = False, window = False, event = False):
        threading.Thread.__init__(self)
        self._gtk = gtk
        self._window = window
        self._function = function
        self._params = params
        self._event = event
        self.start()

    def run(self):
        if self._gtk:
            gtk.gdk.threads_enter()

        if self._event:
            self._event.wait()

        self._function(**self._params)

        if self._gtk:
            gtk.gdk.threads_leave()

        if self._window:
            self._window.hide()

def ProcessGenerator(command, terminal = False, bar = False):

    filename = '/tmp/cs-command-'+hashlib.sha1(
        str(random.getrandbits(random.getrandbits(10)))
        ).hexdigest()

    if isinstance(command, list):
        strcmd = ' '.join(command)
    elif isinstance(command, str):
        strcmd = command

    cmd = '%s 1>%s 2>&1' % (strcmd, filename)

    try:
        os.mkfifo(filename)
        fifo = os.fdopen(os.open(filename, os.O_RDONLY | os.O_NONBLOCK))

        process = subprocess.Popen(
                cmd, shell = True, stdout = subprocess.PIPE,
                stderr = subprocess.STDOUT
                )

        if bar:
            timer = gobject.timeout_add(100, bar.pulse)

        while process.returncode == None:
            process.poll()
            try:
                line = fifo.readline().strip()
                if terminal:
                    terminal.feed(line)
            except:
                continue

    finally:
        os.unlink(filename)
        if bar:
            gobject.source_remove(timer)

    return process

def KillProcess(reference, shell = [], python = [], terminal = False):
    for s in shell:
        k = ProcessGenerator(['/usr/bin/pkill', s], terminal = terminal)
    for p in python:
        p.kill()
    return True

def GetArch(terminal = False):
    p = ProcessGenerator(['/usr/bin/arch'], terminal = terminal)
    a = p.stdout.read().split('\n')[0]
    return a

def TestIndexes(sourcestext, archlist, progressmessage, download,
                q_bar, q_msg, q_terminal, q_code, q_counter, event):

    bar = q_bar.get()
    message = q_msg.get()
    terminal = q_terminal.get()
    errorcounter = 0
    errorcode = ''
    sourceslist = []
    CleanTempDir(tempdir)

    if not download:
        timer = gobject.timeout_add(100, bar.pulse)

    for line in sourcestext.split('\n'):
        if line:
            parts = line.split(' ')
            url = parts[1]
            branch = parts[2]
            sections = parts[3:]
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
                terminal.feed(requesturl+'\n')

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
    if not download:
        gobject.source_remove(timer)

    q_bar.put(bar)
    q_msg.put(message)
    q_terminal.put(terminal)
    q_code.put(errorcode)
    q_counter.put(errorcounter)
    event.set()

#    return bar, message, errorcounter, errorcode

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
