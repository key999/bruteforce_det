#!/usr/bin/env python3
# dev branch

from os import popen, system

# name of pattern to be searched for : amount of 'safe' occurrences
PATTERNS = {'failed': 100,
            'root': 100
            }

LOG_FILE = 'logs'
FLAG_FILE = './flag'
LAST_LOG_LINE = 0
FORM = None


def check():
    global FORM
    global LAST_LOG_LINE

    # prepare searching form
    for i in PATTERNS:
        FORM += " -e '{0}'".format(i)

    FORM += " > temp"

    print('executing:', FORM)  # shite-debug
    # tail -n +LAST_LOG_LINE LOG_FILE | grep -i -e PATTERNS > temp
    system(FORM)

    # set LAST_LOG_LINE
    LAST_LOG_LINE = popen("wc -l {0} | cut -d ' ' -f 1".format(LOG_FILE)).read()
    print('last log line:', LAST_LOG_LINE)  # shite-debug
    save()

    # determine if being attacked
    for i in PATTERNS:
        if int(popen("cat {0} | grep -e '{1}' | wc -l".format('temp', i)).read()[:-1]) > PATTERNS[i]:
            bruteforce_detected()


# TODO implement notification
def bruteforce_detected():
    system("echo 1 > {0}".format(FLAG_FILE))


# save LAST_LOG_LINE
def save():
    with open('last-log', 'w') as f:
        f.write(LAST_LOG_LINE)


# load LAST_LOG_LINE
def load():
    global LAST_LOG_LINE
    try:
        with open('last-log', 'r') as f:
            LAST_LOG_LINE = int(f.read()[:-1])
    except (ValueError, FileNotFoundError):
        LAST_LOG_LINE = 0


# main function
# handles logic
def run():
    load()
    global FORM
    FORM = 'tail -n +{0} {1} | grep -i'.format(LAST_LOG_LINE, LOG_FILE)
    check()


run()
