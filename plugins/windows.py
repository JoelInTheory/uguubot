import os
import re
import time
import socket
from util import hook


# TODO: make this autodetect either google-chrome or chromium-browser
CHROME_CMD = 'google-chrome'
HOSTNAME = socket.gethostname()
MRSKELTAL = ['▒▒▒░░░░░░░░░░▄▐░░░░',
             '▒░░░░░░▄▄▄░░▄██▄░░░',
             '░░░░░░▐▀█▀▌░░░░▀█▄░',
             '░░░░░░▐█▄█▌░░░░░░▀█▄',
             '░░░░░░░▀▄▀░░░▄▄▄▄▄▀▀',
             '░░░░░▄▄▄██▀▀▀▀░░░░░',
             '░░░░█▀▄▄▄█░▀▀░░░░░░',
             '░░░░▌░▄▄▄▐▌▀▀▀░░░░░',
             '░▄░▐░░░▄▄░█░▀▀░░░░░',
             '░▀█▌░░░▄░▀█▀░▀░░░░░',
             '░░░░░░░░▄▄▐▌▄▄░░░░░',
             '░░░░░░░░▀███▀█░▄░░░',
             '░░░░░░░▐▌▀▄▀▄▀▐▄░░░',
             '░░░░░░░▐▀░░░░░░▐▌░░',
             '░░░░░░░█░░░░░░░░█░░',
             '░░░░░░▐▌░░░░░░░░░█░']

SPOOKY_RE = (r"\bgentle spooks\b", re.I)


def send(conn, chan, line):
    out = "PRIVMSG %s :\x01ACTION %s\x01" % (chan, line)
    conn.send(out)


def spooky_spam(conn, chan):
    for line in MRSKELTAL:
        out = "PRIVMSG %s : %s " % (chan, line.decode('utf-8'))
        conn.send(out)
        time.sleep(.3)


@hook.command('ow')
def open_windows(inp, conn=None, chan=None):
    open_windows = os.popen('DISPLAY=:0 wmctrl -l').readlines()
    if len(open_windows) == 0:
        return 'No open windows'
    for line in open_windows:
        title = line.split(HOSTNAME)[1]
        send(conn, chan, title)


@hook.command('cw')
def close_window(inp):
    target = inp.lower().strip()
    if target == 'all':
        open_windows = os.popen('DISPLAY=:0 wmctrl -l').readlines()
        for line in open_windows:
            hex_val = line.split('0 %s' % HOSTNAME)[0].strip()
            os.popen('DISPLAY=:0 wmctrl -ic "%s"' % hex_val)
        return 'Closing all windows'
    else:
        os.popen('DISPLAY=:0 wmctrl -c "%s"' % target)
        return 'Closing %s' % target


@hook.command('ls')
def launch_site(inp):
    os.popen('DISPLAY=:0 %s -new-window %s &' % (CHROME_CMD, inp))
    return 'Launching site %s' % inp


@hook.command('lyt')
def launch_youtube(inp):
    url_pieces = inp.split('/watch')
    new_url = '%s/tv#/watch%s' % (url_pieces[0], url_pieces[1])
    os.popen('DISPLAY=:0 %s -new-window %s &' % (CHROME_CMD, new_url))
    return 'Launching YouTube in TV MODE'


@hook.command('fw')
def focus_window(inp):
    os.popen('DISPLAY=:0 wmctrl -a %s &' % inp)
    return 'Focusing window %s' % inp


@hook.command('max')
def maximize_window(inp):
    os.popen(('DISPLAY=:0 wmctrl -r :ACTIVE: -b '
              'toggle,maximized_vert,maximized_horz &'))
    return 'Maximizing current window'


@hook.command('kp')
def key_press(inp):
    os.popen('DISPLAY=:0 xdotool key %s' % inp)
    return 'Pressing key: %s' % inp


@hook.regex(*SPOOKY_RE)
def gentle_doot(match, conn=None, chan=None):
    spooks = 'https://youtu.be/dMXBwKOfULY'
    os.popen('DISPLAY=:0 %s -new-window %s &' % (CHROME_CMD, spooks))
    spooky_spam(conn, chan)
