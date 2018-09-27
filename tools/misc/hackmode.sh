#!/bin/bash
# My byobu hackmode script.
# Split in 4 panes and prepare terminal for hacking

STARTFOLDER='~/dev/HackingAllTheThings'

byobu new-session -d
byobu split-window -d -t 0 -v
tmux selectp -t 0
tmux send-keys "cd ${STARTFOLDER}" C-m
byobu split-window -d -t 0 -h
byobu split-window -d -t 2 -h
tmux selectp -t 2
tmux send-keys "cd ${STARTFOLDER}" C-m
tmux selectp -t 1
tmux send-keys "cd ${STARTFOLDER}" C-m
tmux selectp -t 3
tmux send-keys "cd ${STARTFOLDER}" C-m
byobu attach
