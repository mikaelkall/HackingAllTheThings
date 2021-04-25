# JWT tokens

If public key is known and RSA is used we can try convert token to use RSA256 instead.
That can be done simpliest with this command.

```
RsaToHmac.py -t <JWT TOKEN> -p public.pem
```

See this link for manual method: https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/JSON%20Web%20Token