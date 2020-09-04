#!./venv/Scripts/python

from time import sleep
from telegram_parser import parse_data
import pyautogui as auto
import subprocess
import configparser
import os
import sys


config = configparser.ConfigParser()
config.read('./settings.ini')
PAUSE = int(config['Delay']['sleep'])
width, height = auto.size()


def start_telegram(path):
    subprocess.Popen([fr"{path}"], stdin=subprocess.PIPE)
    sleep(5)
    for i in range(5):
        sleep(0.4)
        auto.hotkey('Win', 'up')
    sleep(1)
    active = get_active_window()
    if 'telegram' not in active.lower():
        auto.alert('Cannot open Telegram')
    sleep(2)


def restart_telegram():
    sleep(1)
    print('\n')
    os.system("TASKKILL /F /IM telegram.exe")
    print('\n')
    sleep(1)


def add_contact(name, number):
    os.chdir('./find_pic')
    for img in ['menu.png', 'contacts.png', 'add-contact-btn.png']:
        pos = auto.locateOnScreen(img, grayscale=True)
        if pos is None and img == 'add-contact-btn.png':
            pos = (int(width * 5.2 // 12), int(height * 0.76))
        if pos is None and img == 'menu.png':
            pos = auto.locateOnScreen('menu1.png', grayscale=True)
        auto.moveTo(pos, duration=0.1)
        auto.click(button='left', clicks=1, interval=0.05)
        sleep(0.03)
    auto.typewrite(name, interval=0.1)
    [auto.press('tab') for i in range(2)]
    auto.typewrite(number, interval=0.1)
    pos = auto.locateOnScreen('create.png', grayscale=True)
    auto.moveTo(pos, duration=0.1)
    auto.click(button='left', clicks=1, interval=0.05)
    os.chdir('../')


def set_contact_list():
    os.chdir('database')
    print('\nStart adding contacts')
    with open('phonenumbers.txt', 'r') as fin:
        data = list(map(lambda x: x.replace('\n', '').replace(' ', ''), fin.readlines()))
    os.chdir('../')
    for i in range(len(data)):
        if data[i] == '' or data[i] == '\n':
            continue
        add_contact(f'{i + 1} person', data[i])
        print(f'\tAdded {i + 1} persons\t')
        sleep(0.02)
    print('\nFinish adding contacts')


def open_group_subscribers(part=True):
    if part:
        sleep(3)
        global width, height
        auto.press('down')
        auto.press('enter')
        pos = width // 2, 30
        auto.moveTo(pos, duration=0.05)
        auto.click(button='left', clicks=1)
    sleep(5)
    os.chdir('find_pic')
    pos = auto.locateCenterOnScreen('add-subscriber.png', grayscale=True)
    os.chdir('../')
    auto.moveTo(pos)
    auto.click(button='left', clicks=1)
    sleep(2)


def focus_on_telegram():
    titles = auto.getAllTitles()
    main = None
    for i in titles:
        if 'telegram' in i.lower():
            main = i
            break
    if main is not None:
        telegram = auto.getWindowsWithTitle(main)
        telegram[0].activate()
        sleep(0.02)
        auto.press('down')
        auto.press('enter')
        print('Pressed')
        sleep(0.02)


def add_contact_list_to_group():
    global PAUSE
    open_group_subscribers()
    os.chdir('database')
    with open('phonenumbers.txt', 'r') as fin:
        data = [i for i in map(lambda x: x.replace('\n', '').replace(' ', ''), fin.readlines()) if i != '']
    os.chdir('../')
    for queue in range(0, len(data), 100):
        for item in range(queue, queue + 100 if queue + 100 <= len(data) else len(data)):
            auto.press('down')
            auto.press('enter')
            sleep(0.05)
        os.chdir('find_pic')
        pos = auto.locateCenterOnScreen('add-to-group.png', grayscale=True)
        if pos is None:
            pos = auto.locateCenterOnScreen('add-to-group1.png', grayscale=True)
        os.chdir('../')
        sleep(0.005)
        auto.moveTo(pos)
        auto.click(button='left', clicks=2, interval=0.02)
        sleep(PAUSE)
        open_group_subscribers(part=False)
        sleep(4)


def add_users():
    global PAUSE
    open_group_subscribers()
    os.chdir('database')
    with open('nicknames.txt', 'r') as fin:
        data = [i for i in map(lambda x: x.replace('\n', '').replace(' ', ''), fin.readlines()) if i != '']
    os.chdir('../')
    for queue in range(0, len(data), 100):
        for item in range(queue, queue + 100 if queue + 100 <= len(data) else len(data)):
            auto.typewrite(data[item])
            sleep(4)
            if auto.locateCenterOnScreen('./find_pic/not-found.png', grayscale=True) is not None:
                for i in range(len(data[item])):
                    auto.press('backspace')
                    sleep(0.01)
            else:
                auto.press('down')
                auto.press('enter')
            sleep(0.1)
        os.chdir('find_pic')
        pos = auto.locateCenterOnScreen('add-to-group.png', grayscale=True)
        os.chdir('../')
        sleep(0.005)
        auto.moveTo(pos)
        auto.click(button='left', clicks=1, interval=0.02)
        sleep(PAUSE)
        open_group_subscribers(part=False)
        sleep(4)


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
    auto.alert('Warning! The program starts. Do not turn off it.')
    if '-A' in sys.argv:
        start_telegram(telegram_path)
        sleep(2)
        set_contact_list()
    elif '-C' in sys.argv:
        start_telegram(telegram_path)
        sleep(2)
        add_contact_list_to_group()
    elif '-U' in sys.argv:
        start_telegram(telegram_path)
        sleep(2)
        add_users()
    elif '-P' in sys.argv:
        parse_data()
    else:
        parse_data()
        start_telegram(telegram_path)
        set_contact_list()
        # Add all contacts
        restart_telegram()
        start_telegram(telegram_path)
        add_contact_list_to_group()
        # Add all users
        restart_telegram()
        start_telegram(telegram_path)
        add_users()
    auto.alert('The program finished')
