#!/usr/bin/env python3

from os import popen, system
import time

PATTERNS = {'failed': 0,
            'root': 0
            }
LOG_FILE = 'logs'
FLAG_FILE = './flag'
TAIL_LINES = 100
LAST_LOG = None
SEARCH_FORM = 'cat {0} | grep -i'.format(LOG_FILE)


def initial_check():
    global SEARCH_FORM
    # prepare searching form
    for i in PATTERNS:
        SEARCH_FORM += " -e '{0}'".format(i)

    SEARCH_FORM += " > temp"
    print('search form:', SEARCH_FORM)  # shite-debug
    system(SEARCH_FORM)

    LAST_LOG = time.strptime(popen("tail -n 1 {0} | cut -d ' ' -f 1-3".format(LOG_FILE)).read()[0:-1], "%b %d %H:%M:%S")
    print(LAST_LOG)


# TODO improve detection system
def find_log():
    pass


# action on detecting a possible attack
# DONE set flag file
# TODO implement notification
def bruteforce_detected():
    system("echo 1 > {0}".format(FLAG_FILE))


# saving last log date
# for detection purposes
def save():
    # TODO implement this
    pass


# load LAST_LOG time
def load():
    # TODO implement this
    pass


# main function
# handles logic
def run():
    try:
        load()
    except FileNotFoundError:
        pass

    if LAST_LOG is None:
        initial_check()
    # if find_log() == 1:
    #     bruteforce_detected()


run()
