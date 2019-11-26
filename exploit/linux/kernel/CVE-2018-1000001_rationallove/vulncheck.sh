#!/bin/bash
# Vulnerability check shell script for CVE-2018-1000001
# written by zc00l

error() {
    echo -ne "\033[091m[!]\033[00m Error: $1\n";
}

success() {
    echo -ne "\033[092m[+]\033[00m Success: $1\n";
}

vuln() {
    success "This $1 is vulnerable to CVE-2018-1000001\n";
    exit 0;
}

check_ns() {
    if [[ $(cat /proc/sys/kernel/unprivileged_userns_clone) != "1" ]]; then
        success "You are not vulnerable!"
        exit 0;
    fi
}

DPKG_PATH=$(which dpkg);
if [[ $DPKG_PATH == "" ]]; then
    error "Could not find dpkg binary.";
    exit 1;
fi

check_ns

libc6=$($DPKG_PATH --list | grep -i libc6:amd64 | awk {'print $3'});
if [[ $libc6 == "2.24-11+deb9u1" ]]; then
    vuln "Debian";
fi
if [[ $libc6 == "2.23-0ubuntu9" ]]; then
    vuln "Ubuntu";
fi

success "You are not vulnerable!";
