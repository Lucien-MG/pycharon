#!/usr/bin/python3.6

import os 
import socket as sck
import json

from src.serverprocess import ServerProcess
from src.utils import *

import time 
import threading

from terminal import Terminal
from serverlistener import ServerListener

class Server:

    def __init__(self, port = 12800, serv_dir = "~/Public"):
        self.host = self.getlocalip()
        self.port = port

        self.server_directory = serv_dir
        self.client_list = []

        # Initiate connexion.
        self.connexion = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
        self.serverlistener = ServerListener(self.connexion, self.client_list)
        #self.process = ServerProcess(self.connexion)

    def getlocalip(self):
        s = sck.socket(sck.AF_INET, sck.SOCK_DGRAM)
        # connect() for UDP doesn't send packets
        s.connect(('8.8.8.8', 1)) 
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

        self.serverlistener.start()
        #self.process.run(p_name="listener", p_args = (self.connexion, self.client_list))

    def runterminal(self):
        term = Terminal(self)
        term.run()

    def close(self):
        self.process.close("listener")
        self.connexion.close()
        print("Server end.")

    def buildmetadata(self, path):
        metadata  = {}
        metadata["name"] = os.path.basename(path)

        if os.path.isdir(path):
            metadata["type"] = "dir"
            underdata = {}
            for o in os.listdir(path):
                underdata[o] = self.buildmetadata(os.path.join(path,o))

            metadata["content"] = underdata
        else:
            metadata["type"] = "file"
            metadata["size"] = str(os.path.getsize(path))

        return metadata

    def send(self, clientID = "all", path = "./"):
        clientID = int(clientID)

        objectdata = self.buildmetadata(path)
        metadata = json.dumps(objectdata).encode()

        self.client_list[clientID][0].send(metadata)
        response = self.client_list[clientID][0].recv(4096)
    
        if response == b"N":
            return 

        if objectdata["type"] == "dir":
            self.senddir(clientID, path, objectdata)
        else:
            self.sendfile(clientID, path, objectdata["size"])
        return 

    def senddir(self, clientID, path, objectdata):
        content = objectdata["content"]

        for o in content:
            if content[o]["type"] == "file":
                self.sendfile(clientID, os.path.join(path, content[o]["name"]), content[o]["size"])
            else:
                self.senddir(clientID, os.path.join(path, content[o]["name"]), content[o])

    def sendfile(self, clientID, file_path, size):                                               
        print("Sending file: ", file_path)
        size = int(size)
        chunksize = calculatechunk(size)
        nbsend = int(size / chunksize) + 1                                     

        with open(file_path, "rb") as f:
            for i in range(1,nbsend+1):
                byte = f.read(chunksize)
                try:                                                         
                    self.client_list[clientID][0].send(byte)
                except BrokenPipeError:
                    print("Connection interrupted.")
                    f.close()
                    return

                printprogress(i, nbsend, status="sending")

            f.close()  

        # Needed to print after printprogress:
        print("")

        time.sleep(0.1)           
        print("File transmited.")
