#!/usr/bin/env python3

from os import popen, system

PATTERNS = {'failed': 0,
            'incorrect': 0,
            'root': 0}
LOG_FILE = 'logs'
FLAG_FILE = './flag'
TAIL_LINES = 100
LAST_LOG = None


def find_log():
    form = "tail -n {0} {1} | grep -i '{2}'".format(TAIL_LINES, LOG_FILE, PATTERNS['failed'])
    a = popen(form, 'r').read()
    print(a)

    return 0 if a == '' else 1


def bruteforce_detected():
    system("echo 1 > {0}".format(FLAG_FILE))


print(find_log())
