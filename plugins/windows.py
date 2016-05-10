import os
from util import hook


@hook.command('ow')
def open_windows():
    open_windows =  os.popen('DISPLAY=:0 wmctrl -l').readlines()
    if len(open_windows) == 0:
        return 'No open windows'
    for line in open_windows:
        title = line.split('ATXBawt')[1]
        return title


@hook.command('cw')
def close_window(inp):
    target = inp.lower().strip()
    if target == 'all':
        open_windows =  os.popen('DISPLAY=:0 wmctrl -l').readlines()
        for line in open_windows:
            hex_val = line.split('0 ATXBawt')[0].strip()
            os.popen('DISPLAY=:0 wmctrl -ic "%s"' % hex_val)
        return 'Closing all windows'
    else:
        os.popen('DISPLAY=:0 wmctrl -c "%s"' % target)
        return 'Closing %s' % target


@hook.command('ls')
def launch_site(inp):
    os.popen('DISPLAY=:0 chromium-browser -new-window %s &' % inp)
    return 'Launching site %s' % inp


@hook.command('lyt')
def launch_youtube(inp):
    url_pieces = inp.split('/watch')
    new_url = '%s/tv#/watch%s' % (url_pieces[0], url_pieces[1])
    os.popen('DISPLAY=:0 chromium-browser -new-window %s &' % new_url)
    return 'Launching YouTube in TV MODE'


@hook.command('fw')
def focus_window(inp):
    os.popen('DISPLAY=:0 wmctrl -a %s &' % inp)
    return 'Focusing window %s' % inp


@hook.command('max')
def maximize_window(inp):
    os.popen('DISPLAY=:0 wmctrl -r :ACTIVE: -b toggle,maximized_vert,maximized_horz &')
    return 'Maximizing current window'


@hook.command('kp', 'k')
def key_press(inp):
    os.popen('DISPLAY=:0 xdotool key %s' % inp)
    return 'Pressing key: %s' % inp