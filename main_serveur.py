#!/usr/bin/python3.6

import sys
sys.path.insert(0, 'src/')

from server import Server

serv = Server(port = 12800, serv_dir = "../../../Public")

serv.runterminal()



