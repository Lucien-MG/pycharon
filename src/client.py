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

        metadata = self.connexion.recv(4096).decode()

        file_data = metadata.split('/')

        if file_name == "":
            file_name = file_data[0]

        print("Do you want to receive this " + file_data[1] + ":\n" + file_data[0])

        test = input("\n[Y/n]")

        if test.lower() == "yes"  or test.lower() == "y":
            self.connexion.send(b"Y")
        else:
            self.connexion.send(b"N")
            return

        f = open(self.path_save_file + file_name, "wb")

        file_size = int(file_data[2])

        if file_data[1] == "file":
            while file_size > 0:
                print(data)
                data = self.connexion.recv(4096)
                file_size -= len(data)
                f.write(data)

        f.close()
        print("File received!")
