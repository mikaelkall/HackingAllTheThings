# Password cracking decryption

## Good page for password cracking search

https://hashes.org
https://hashkiller.co.uk
https://quipqiup.com/
http://rumkin.com/tools/cipher/

## Cracking ssh files

if id_rsa says encrypted as bellow you need to crack the passphrase

```sh 
-----BEGIN RSA PRIVATE KEY-----
Proc-Type: 4,ENCRYPTED
DEK-Info: AES-128-CBC,7265FC656C429769E4C1EEFC618E660C
```

This command to start cracking.

```sh 
ssh2john ./id_rsa > id_rsa.hash
john --wordlist=/home/nighter/SecLists/Passwords/Leaked-Databases/rockyou.txt ./id_rsa.hash
```

## Crack keepass

```sh
keepass2john DB.kdbx > DB.hash
john --wordlist=/home/nighter/SecLists/Passwords/Leaked-Databases/rockyou.txt ./DB.hash
```

### Crack password protected zip

```sh
fcrackzip -v -D -u -p ./rockyou.txt ./backup.zip
```

## Get private key from weak publickey

```sh
python2 /usr/share/rsactftool/RsaCtfTool.py --publickey ./rootauthorizedsshkey.pub --private > rootkey.rsa
```

## Crack pwdump windows LM / NT hashes.

Extract hashes from pwdump.txt and run this command

```
hashcat -m 1000 -a 0 -o results.txt --remove ./hashes.hash /usr/share/wordlists/SecLists/Passwords/Leaked-Databases/rockyou.txt
```

