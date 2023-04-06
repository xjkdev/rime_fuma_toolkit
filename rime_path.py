import os
import sys

def get_rime_userdata():
    if sys.platform == 'win32' or sys.platform =='cygwin':
        return os.path.join(os.getenv('APPDATA'), 'RIME')
    elif sys.platform == 'darwin':
        return os.path.expanduser('~/Library/Rime/')
    elif sys.platform == 'linux':
        paths = [
            os.path.expanduser('~/.config/ibus/rime'),
            os.path.expanduser('~/.ibus/rime'),
            os.path.expanduser('~/.local/share/fcitx5/rime')
        ]
        for path in paths:
            if os.path.exists(path):
                return path
