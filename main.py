#!./venv/Scripts/python

from time import sleep
import pyautogui
import sys


def get_active_window():
    import sys
    active_window_name = None
    if sys.platform in ['Windows', 'win32', 'cygwin']:
        # http://stackoverflow.com/a/608814/562769
        import win32gui
        window = win32gui.GetForegroundWindow()
        active_window_name = win32gui.GetWindowText(window)
    else:
        print("sys.platform={platform} is not windows. Please report."
              .format(platform=sys.platform))
        print(sys.version)
    return active_window_name


print("Active window: %s" % str(get_active_window()))

