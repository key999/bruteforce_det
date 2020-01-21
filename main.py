#!/usr/local/bin/python3

# dev branch

from os import popen, system

# name of pattern to be searched for : amount of 'safe' occurrences
PATTERNS = {'failed': 100,
            'root': 10
            }

LOG_FILE = 'auth.log'
FLAG_FILE = './flag'
TEMP_FILE = 'temp'

LAST_LOG_LINE = 0
LAST_LOG_DATE = ''

GREP_FORM = None


def check():
    global GREP_FORM
    global LAST_LOG_LINE
    global LAST_LOG_DATE

    # prepare grep form
    for i in PATTERNS:
        GREP_FORM += " -e '{0}'".format(i)
    GREP_FORM += " > {0}".format(TEMP_FILE)

    # execute grep form
    print('executing:', GREP_FORM)  # shite-debug
    # tail -n +LAST_LOG_LINE LOG_FILE | grep -i -e PATTERNS > TEMP_FILE
    system(GREP_FORM)

    # set LAST_LOG_LINE
    LAST_LOG_LINE = popen("wc -l {0} | cut -d ' ' -f 1".format(LOG_FILE)).read()[:-1]
    print('last log line:', LAST_LOG_LINE)  # shite-debug

    # set LAST_LOG_DATE
    LAST_LOG_DATE = popen("tail -n 1 {0} | cut -d ' ' -f 1-3".format(LOG_FILE)).read()[:-1]
    print('last date:', LAST_LOG_DATE)  # shite-debug

    save()

    # determine if being attacked
    # TODO improve detection
    for i in PATTERNS:
        if int(popen("cat {0} | grep -ie '{1}' | wc -l".format(TEMP_FILE, i)).read()[:-1]) > PATTERNS[i]:
            bruteforce_detected()


# TODO implement notification
def bruteforce_detected():
    system("echo 1 > {0}".format(FLAG_FILE))
    print("RATUNKU ATAKUJO")  # shite-debug


# save last log date and line
def save():
    with open('last-log', 'w') as f:
        f.write(str(LAST_LOG_LINE))
        f.write(LAST_LOG_DATE)


# handle start point of check()
def load():
    global LAST_LOG_LINE
    global LAST_LOG_DATE
    try:
        with open('last-log', 'r') as f:
            LAST_LOG_LINE = int(f.readline()[:-1])
            LAST_LOG_DATE = f.readline()[:-1]
    except (ValueError, FileNotFoundError) as e:
        # set LAST_LOG_DATE to first date from LOG_FILE
        # needed for 'finally' to work
        LAST_LOG_DATE = popen("head -n 1 {0} | cut -d ' ' -f 1-3".format(LOG_FILE)).read()[:-1]
        print('caught exception:', e)  # shite-debug
    finally:
        # make sure LAST_LOG_LINE is actually a last checked line in the LOG_FILE
        # in case something happens to the log (for example another process trims the beginning of log)
        last_log_line = int(popen("cat {0} | grep -ine '{1}' | cut -d ':' -f 1 | tail -n 1"
                                  .format(LOG_FILE, LAST_LOG_DATE)).readline()[:-1])
        if last_log_line != LAST_LOG_LINE:
            LAST_LOG_LINE = last_log_line


# main function
# handles logic
# not actually necessary
def run():
    load()
    global GREP_FORM
    GREP_FORM = 'tail -n +{0} {1} | grep sshd | grep -i'.format(LAST_LOG_LINE, LOG_FILE)
    check()


run()
