# tmux cheat sheet

(C-x means ctrl+x, M-x means alt+x)


## Prefix key

The default prefix is C-b. If you (or your muscle memory) prefer C-a, you need to add this to `~/.tmux.conf`:

    # remap prefix to Control + a
    set -g prefix C-a
    # bind 'C-a C-a' to type 'C-a'
    bind C-a send-prefix
    unbind C-b

I'm going to assume that C-a is your prefix.


## Sessions, windows, panes

Session is a set of windows, plus a notion of which window is current.

Window is a single screen covered with panes. (Once might compare it to a ‘virtual desktop’ or a ‘space’.)

Pane is a rectangular part of a window that runs a specific command, e.g. a shell.


## Getting help

Display a list of keyboard shortcuts:

    C-a ?

Navigate using Vim or Emacs shortcuts, depending on the value of `mode-keys`. Emacs is the default, and if you want Vim shortcuts for help and copy modes (e.g. j, k, C-u, C-d), add the following line to `~/.tmux.conf`:

    setw -g mode-keys vi

Any command mentioned in this list can be executed as `tmux something` or `C-a :something` (or added to `~/.tmux.conf`).


## Managing sessions

Creating a session:

    tmux new-session -s work

Create a new session that shares all windows with an existing session, but has its own separate notion of which window is current:

    tmux new-session -s work2 -t work

Attach to a session:

    tmux attach -t work

Detach from a session: `C-a d`.

Switch between sessions:

    C-a (          previous session
    C-a )          next session
    C-a L          ‘last’ (previously used) session
    C-a s          choose a session from a list

Other:

    C-a $          rename the current session
    C-a


## Managing windows

Create a window:

    C-a c          create a new window

Switch between windows:

    C-a 1 ...      switch to window 1, ..., 9, 0
    C-a 9
    C-a 0
    C-a p          previous window
    C-a n          next window
    C-a l          ‘last’ (previously used) window
    C-a w          choose window from a list

Switch between windows with a twist:

    C-a M-n        next window with a bell, activity or
                   content alert
    C-a M-p        previous such window


Other:

    C-a ,          rename the current window
    C-a &          kill the current window


## Managing split panes

Creating a new pane by splitting an existing one:

    C-a "          split vertically (top/bottom)
    C-a %          split horizontally (left/right)

Switching between panes:

    C-a left       go to the next pane on the left
    C-a right      (or one of these other directions)
    C-a up
    C-a down
    C-a o          go to the next pane (cycle through all of them)
    C-a ;          go to the ‘last’ (previously used) pane

Moving panes around:

    C-a {          move the current pane to the previous position
    C-a }          move the current pane to the next position
    C-a C-o        rotate window ‘up’ (i.e. move all panes)
    C-a M-o        rotate window ‘down’
    C-a !          move the current pane into a new separate
                   window (‘break pane’)
    C-a :move-pane -t :3.2
                   split window 3's pane 2 and move the current pane there

Resizing panes:

    C-a M-up, C-a M-down, C-a M-left, C-a M-right
                   resize by 5 rows/columns
    C-a C-up, C-a C-down, C-a C-left, C-a C-right
                   resize by 1 row/column

Applying predefined layouts:

    C-a M-1        switch to even-horizontal layout
    C-a M-2        switch to even-vertical layout
    C-a M-3        switch to main-horizontal layout
    C-a M-4        switch to main-vertical layout
    C-a M-5        switch to tiled layout
    C-a space      switch to the next layout


Other:

    C-a x          kill the current pane
    C-a q          display pane numbers for a short while


## Other config file settings

Force a reload of the config file on C-a r:

    unbind r
    bind r source-file ~/.tmux.conf

Some other settings that I use:

    setw -g xterm-keys on
