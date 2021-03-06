import socket as sck
from terminal import Terminal
import json
import os
import sys

from src.utils import *

class Client:

    def __init__(self):
        self.path_save_file = "./"
        self.connexion = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
        self.term = Terminal(self)

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
        self.term.run()

    def recv(self, file_name = ""):
        metadata_tmp = self.connexion.recv(4096).decode()

        metadata = json.loads(metadata_tmp)

        if file_name != "":
            metadata["name"] = file_name

        print("Do you want to receive this " + metadata["type"] + ":\n" + metadata["name"])

        test = False

        while not test:
            ans = input("\n[Y/n]")
            if ans.lower() == "yes"  or ans.lower() == "y":
                if os.path.exists(os.path.join(self.path_save_file, metadata["name"])):
                    print("The received " + metadata["type"] +
                        " already exists. Do you want to delete it ?")
                    
                    self.askconfirmdel(metadata)

                self.connexion.send(b"Y")
                test = True

                if metadata["type"] == "file":
                    self.recvfile(metadata, os.path.join(self.path_save_file, metadata["name"]))
                    print("File received!")

                elif metadata["type"] == "dir":
                    self.recvdir(metadata, self.path_save_file)
                    print("Folder received!")

                else:
                    print("Error: Wrong data type sent")

            elif ans.lower() == "no" or ans.lower() == "n":
                self.connexion.send(b"N")
                test = True

                return

    def askconfirmdel(self, metadata):
        test2 = False

        while not test2:
            ans = input("\n[Y/n]")

            if ans.lower() == "yes"  or ans.lower() == "y":
                self.deldir(os.path.join(self.path_save_file, metadata["name"]))
                print("Directory deleted!")
                test2 = True 

            elif ans.lower() == "no" or ans.lower() == "n":
                self.connexion.send(b"N")
                test2= True

                return

    def deldir(self, path):
        if os.path.isdir(path):
            for name in os.listdir(path):
                self.deldir(os.path.join(path, name))
            os.rmdir(path)
        else:
            os.remove(path)

    def recvfile(self, metadata, path):
        f = open(path, "wb")
        data = b" "

        file_size = int(metadata["size"])
        count = 0
        tmp = 0

        while count < file_size:
            if tmp % 100 == 0:
                printprogress(count, file_size)

            data = self.connexion.recv(16384)
            count += len(data)
            tmp += 1

            f.write(data)

        printprogress(count, file_size)
        print("")

        f.close()

    def recvdir(self, metadata, path):
        if metadata != {}:
            if metadata["type"] == "dir":
                content = metadata["content"]

                path = os.path.join(path, metadata["name"])
                os.makedirs(path)

                for o in content:
                    self.recvdir(content[o], path)
            elif metadata["type"] == "file":
                path = os.path.join(path, metadata["name"])
                self.recvfile(metadata, path)
            else:
                print("Error: Wrong data type sent")
