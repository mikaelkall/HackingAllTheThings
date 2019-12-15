    
## Finding weak directory permissions

```sh
accesschk.exe /accepteula
accesschk.exe -uwdqs users c:\
accesschk.exe -uwdqs “Authenticated Users” c:\
``` 


## Finding weak file permissions

```sh
accesschk.exe /accepteula
accesschk.exe -uwdqs users c:\
accesschk.exe -uwdqs “Authenticated Users” c:\
```

## Weak Service permissions

```sh
accesschk.exe -uwcqv *
```

## Weak service path

```sh
wmic service get name,pathname,starmode
wmic service get name,pathname,startmode | findstr /i /v "c:\Windows\\"
wmic service get name,pathname,startmode | findstr /i /v "c:\Windows\\" |findstr /i /v """
```


