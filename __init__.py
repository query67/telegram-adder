#!./venv/Scripts/python

from time import sleep
from telegram_parser import parse_data
import pyautogui as auto
import subprocess
import configparser
import os


config = configparser.ConfigParser()
config.read('./settings.ini')
width, height = auto.size()


def start_telegram(path):
    subprocess.Popen([fr"{path}"], stdin=subprocess.PIPE)
    sleep(1)
    for i in range(5):
        sleep(0.1)
        auto.hotkey('Win', 'up')
    sleep(1)
    active = get_active_window()
    if 'telegram' not in active.lower():
        auto.alert('Cannot open Telegram')
    sleep(2)


def add_contact():
    print('\n')
    os.chdir('./find_pic')
    for img in ['menu.png', 'contacts.png', 'add-contact-btn.png']:
        pos = auto.locateOnScreen(img)
        print(pos)
        if pos is None and img == 'add-contact-btn.png':
            pos = (int(width * 5.2 // 12), int(height * 0.76))
            print(pos)
        auto.moveTo(pos, duration=0.1)
        auto.click(button='left', clicks=1, interval=0.05)
        sleep(0.03)
    os.chdir('../')


def get_active_window():
    import sys
    active_window_name = None
    if sys.platform in ['Windows', 'win32', 'cygwin']:
        import win32gui
        window = win32gui.GetForegroundWindow()
        active_window_name = win32gui.GetWindowText(window)
    else:
        print("\nsys.platform={platform} is not windows. Please report."
              .format(platform=sys.platform))
        print(sys.version)
    print("Active window: %s" % str(active_window_name))
    return active_window_name


if __name__ == '__main__':
    telegram_path = config['PATH']['telegram']
    auto.alert('After u do not touch the computer, because of starting this program')
    parse_data()
    start_telegram(telegram_path)
    add_contact()


