#!/usr/bin/python3.6

import readline
from completer import MyCompleter

class Terminal:

    def __init__(self, python_class):
        self.pc = python_class

    def run(self):
        exit = False
        cmd = ""

        completer = MyCompleter(dir(self.pc))
        readline.set_completer(completer.complete)
        readline.parse_and_bind('tab: complete')
        readline.set_history_length(100)

        try:
            readline.read_history_file("./.history")
        except:
            readline.write_history_file("./.history")
            print("Create history.")

        while exit != True:
            cmd = input("> ")
            exit = self.handler(cmd + "\n")

        readline.append_history_file(50, "./.history")

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
        nbarg = len(args)

        try:
            if nbarg == 0:
                return 0
            elif args[0] == "q":
                return 1
            elif nbarg == 1:
                getattr(self.pc, args[0]) ()
                return 0
            elif nbarg == 2:
                getattr(self.pc, args[0]) (args[1])
                return 0
            elif nbarg == 3:
                getattr(self.pc, args[0]) (args[1], args[2])
                return 0
        except Exception as e:
            print(e.errno)
            print(e.filename)
            print(e.strerror)

