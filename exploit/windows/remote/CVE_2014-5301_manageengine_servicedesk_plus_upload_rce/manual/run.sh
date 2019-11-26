#!/bin/bash
check=$(uname)
if [ "$check" == 'Darwin' ];
then
    /Applications/Firefox.app/Contents/MacOS/firefox-bin -new-window ./upload.html
else
    firefox -new-window ./upload.html
fi

