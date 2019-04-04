#!/usr/bin/python3.6

import socket as sck
import threading

class ServerListener (threading.Thread):

    def __init__(self, connexion, client_list):
        threading.Thread.__init__(self)

        self.connexion = connexion
        self.client_list = client_list

    def run(self):
        self.connexion.listen()

        print("Starting listening.")

        while (True):
            client, addr = self.connexion.accept()
            self.client_list.append((client, addr))
            print("New client: ", addr)
