import pyautogui as auto
import configparser
import os
from __init__ import start_telegram

config = configparser.ConfigParser()
config.read('./settings.ini')


def calibration():
    pass


if __name__ == '__main__':
    telegram_path = config['PATH']['telegram']
    start_telegram(telegram_path)
