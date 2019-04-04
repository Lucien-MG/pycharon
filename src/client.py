#!/usr/bin/python3.6

import socket as sck
from terminal import Terminal

class Client:

    def __init__(self):
        self.path_save_file = "./test_recv/"
        self.connexion = sck.socket(sck.AF_INET, sck.SOCK_STREAM)

    def setPathToSaveFile(self, path):
        self.path_save_file = path

    def connect(self, host, port):
        try:
            self.connexion.connect((str(host),int(port)))
            print("Connected")
        except ConnectionRefusedError:
            print("No server responding.")
        except OSError:
            print("Invalid arguments.")

    def runterminal(self):
        term = Terminal(self)
        term.run()

    def recvfile(self, file_name = ""):
        data = b" "
        f = open(self.path_save_file + file_name, "wb")

        filesize = int(self.connexion.recv(4096).decode())

        while filesize > 0:
            print(data)
            data = self.connexion.recv(4096)
            filesize -= len(data)
            f.write(data)

        f.close()
        print("File recieve!")
