# REF: https://python-osc.readthedocs.io/en/latest/server.html

# FOR USE WITH "DATAOSC" IOS APP

from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
import numpy as np
import ctcsound

cs = ctcsound.Csound()

def print_handler(address, *args):
    print(f"{address}: {args}")

def default_handler(address, *args):
    print(f"DEFAULT {address}: {args}")

# dispatcher assigns function callback to certain osc addresses
dispatcher = Dispatcher()
dispatcher.map("/data/motion/gyroscope/*", print_handler)
# default funciton called when message doesnt match any addresses
dispatcher.set_default_handler(default_handler)


# CHANGE IP TO MATCH DEVICE IP
ip = "192.168.0.134"
port = 8000

server = BlockingOSCUDPServer((ip, port), dispatcher)
server.serve_forever()  # Blocks forever