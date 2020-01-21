#!/usr/local/bin/python3

# dev branch

from os import popen, system
import time

# name of pattern to be searched for : amount of 'safe' occurrences
PATTERNS = {'failed': 20,
            'root': 5
            }

LOG_FILE = 'auth.log'
FLAG_FILE = './flag'
LAST_LOG_LINE = 0
GREP_FORM = None
LAST_LOG_DATE = None
TEMP_FILE = 'temp'


def check():
    global GREP_FORM
    global LAST_LOG_LINE
    global LAST_LOG_DATE

    # prepare searching form
    for i in PATTERNS:
        GREP_FORM += " -e '{0}'".format(i)

    GREP_FORM += " > {0}".format(TEMP_FILE)

    print('executing:', GREP_FORM)  # shite-debug
    # tail -n +LAST_LOG_LINE LOG_FILE | grep -i -e PATTERNS > TEMP_FILE
    system(GREP_FORM)

    # set LAST_LOG_LINE
    LAST_LOG_LINE = popen("wc -l {0} | cut -d ' ' -f 1".format(LOG_FILE)).read()
    print('last log line:', LAST_LOG_LINE)  # shite-debug

    # set LAST_LOG_DATE
    LAST_LOG_DATE = time.strptime(popen("tail -n 1 {0} | cut -d ' ' -f 1-3".format(LOG_FILE)).read()[0:-1], "%b %d %H:%M:%S")
    # print('last date:', LAST_LOG_DATE)  # shite-debug
    LAST_LOG_DATE = popen("tail -n 1 {0} | cut -d ' ' -f 1-3".format(LOG_FILE)).read()

    save()

    # determine if being attacked
    for i in PATTERNS:
        if int(popen("cat {0} | grep -e '{1}' | wc -l".format(TEMP_FILE, i)).read()[:-1]) > PATTERNS[i]:
            bruteforce_detected()


# TODO implement notification
def bruteforce_detected():
    system("echo 1 > {0}".format(FLAG_FILE))
    print("RATUNKU ATAKUJO")  # shite-debug


# save LAST_LOG_LINE
def save():
    with open('last-log', 'w') as f:
        f.write(LAST_LOG_LINE)
        f.write(LAST_LOG_DATE)


# load LAST_LOG_LINE
def load():
    global LAST_LOG_LINE
    try:
        with open('last-log', 'r') as f:
            LAST_LOG_LINE = int(f.readline()[:-1])
    except (ValueError, FileNotFoundError):
        LAST_LOG_LINE = 0


# main function
# handles logic
def run():
    load()
    global GREP_FORM
    GREP_FORM = 'tail -n +{0} {1} | grep -i'.format(LAST_LOG_LINE, LOG_FILE)
    check()


run()