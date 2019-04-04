#!/usr/bin/python3.6

import os 
import socket as sck
import time 
import threading

from terminal import Terminal
from serverlistener import ServerListener

class Server:

    def __init__(self, port = 12800, serv_dir = "~/Public"):
        self.host = self.getlocalip()
        self.port = port

        self.nb_client = 1

        self.server_directory = serv_dir

        self.client_list = []

        # Initiate connexion.
        self.connexion = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
        self.listener = ServerListener(self.connexion, self.client_list)

    def getlocalip(self):
        s = sck.socket(sck.AF_INET, sck.SOCK_DGRAM)
        s.connect(('8.8.8.8', 1))  # connect() for UDP doesn't send packets
        ip = s.getsockname()[0]
        s.close()
        return ip

    def infos(self):
        infos = os.uname()
        print("# Server infos #")
        print("hostname: ", sck.gethostname())
        print("ip: ", self.connexion.getsockname()[0])
        print("port: ", self.connexion.getsockname()[1])
        print("hardware: ", infos.machine)
        print("operating system: ", infos.sysname) 
        print("system release: ", infos.release)
        print("system version: ", infos.version)

    def listclient(self):
        id = 0

        for client in self.client_list:
            print("[" + str(id) + "]: ",client[1])
            id += 1

    def set_client_number(self, nb_client):
        self.nb_client = nb_client

    def start(self):
        """ Start the python server """
        bind = False

        while not bind:
            try: 
                self.connexion.bind((self.host,self.port))
                bind = True
            except:
                self.port += 1

                if self.port > 65535:
                    raise Exception("No port found.")

                print("Try another port: " + str(self.port))

        self.listener.start()

    def runterminal(self):
        term = Terminal(self)
        term.run()

    def close(self):
        self.connexion.close()
        print("Server end.")

    def sendfile(self, clientID, file_path):
        file = open(file_path, "rb")
        lines = file.readlines()
        file.close()

        print("Sending file...")

        for l in lines:
            self.client_list[int(clientID)][0].send(l)

        self.client_list[int(clientID)][0].send(b"end")

        print("File transmited.")
