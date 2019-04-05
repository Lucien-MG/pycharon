#!/usr/bin/python3.6

import readline
from completer import MyCompleter

class Terminal:

    def __init__(self, python_class, history_name = "./.history", history_length = 100):
        self.python_class = python_class
        self.completer = MyCompleter(dir(python_class))
        self.history_name = history_name
        self.history_length = history_length

        readline.set_completer(self.completer.complete)
        readline.parse_and_bind('tab: complete')

        readline.set_history_length(history_length)

        try:
            readline.read_history_file(history_name)
        except:
            readline.write_history_file(history_name)


    def run(self):
        exit = False
        cmd = ""

        while exit != True:
            cmd = input("> ")
            exit = self.handler(cmd + "\n")

        readline.append_history_file(self.history_length, self.history_name)

    def parse(self, cmd):
        args = []
        arg = ""

        for l in cmd:
            if l != " " and l != "\n":
                arg += l
            elif arg != "":
                args.append(arg)
                arg = ""

        return args

    def handler(self, cmd):
        args = self.parse(cmd)

        if len(args) == 0:
            return 0

        command = args.pop(0)
        args = tuple(args)

        try:
            if command == "q":
                return 1
            else:
                getattr(self.python_class, command) (*args)
                return 0
        except Exception as e:
            print(e)

