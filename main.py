#!/usr/bin/env python3

from os import popen, system


class Foo:
    def __init__(self):
        self.PATTERNS = {'failed': 0,
                         'incorrect': 0,
                         'root': 0}
        self.LOG_FILE = 'logs'
        self.FLAG_FILE = './flag'
        self.TAIL_LINES = 100
        self.LAST_LOG = None

    def find_log(self):
        form = "tail -n {0} {1} | grep -i '{2}'".format(self.TAIL_LINES, self.LOG_FILE, self.PATTERNS['failed'])
        a = popen(form, 'r').read()

        return 0 if a == '' else 1

    @staticmethod
    def bruteforce_detected(self):
        system("echo 1 > {0}".format(self.FLAG_FILE))


x = Foo()
x.find_log()