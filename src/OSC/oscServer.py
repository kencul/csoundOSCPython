#!/usr/bin/python3
# REF: (pythonOSC docs)[https://python-osc.readthedocs.io/en/latest/server.html]

import threading
import time
import sys
import socket

from pathlib import Path

import asyncio

from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import AsyncIOOSCUDPServer
import numpy as np
import ctcsound

# REF: (csound python docs)[https://github.com/csound/ctcsound/blob/master/cookbook/02-performing.ipynb]
cs = ctcsound.Csound()
base_dir = Path(__file__).parent  # Script's directory
csd_dir = base_dir / "osc.csd"
result = cs.compile_csd(str(csd_dir.absolute()), 0)

if result is not ctcsound.CSOUND_SUCCESS:
    print("Failed to compile csd!")
    exit()


# function that returns device's LAN IP (REF: deepseek)
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Doesn't need to be reachable; just fetches local IP
        s.connect(("8.8.8.8", 80))  # Google's DNS
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = "127.0.0.1"  # Fallback to localhost
    finally:
        s.close()
    return local_ip



# Handler functions for OSC message addresses
def xGyroHandler(_, *args):
    # print(f"{address}: {args}") 
    
    val = abs(args[0]) * 0.1
    
    # clamp incoming value between 0 and 1
    if val > 1:
        val = 1
    
    cs.set_control_channel('x', val)
    
def yGyroHandler(_, *args):
    #print(f"{address}: {args}") 
    val = abs(args[0]) * 0.1
    
    # clamp incoming value between 0 and 1
    if val > 1:
        val = 1
        
    cs.set_control_channel('vib', val)

def default_handler(address, *args):
    #print(f"DEFAULT {address}: {args}")
    pass # do nothing


# FILTERING OSC ADDRESSES TO CALLBACK FUNCTIONS
dispatcher = Dispatcher()
dispatcher.map("/data/motion/gyroscope/x", xGyroHandler)
dispatcher.map("/data/motion/gyroscope/y", yGyroHandler)
# default funciton called when message doesnt match any addresses
dispatcher.set_default_handler(default_handler)


# CHANGE IP TO MATCH DEVICE IP
ip = get_local_ip()
port = 8787


# Print the local IP
print(f"\nLocal IP Address: {ip}")

# Wait for user to press Enter
input("Press Enter to continue...")


# loop to handle osc messages
async def main():
    # start async osc server
    server = AsyncIOOSCUDPServer((ip, port), dispatcher, asyncio.get_event_loop())
    transport, protocol = await server.create_serve_endpoint()
    
    print("OSC server started on IP: " + ip)

    # start csound
    cs.start()
    pt = ctcsound.CsoundPerformanceThread(cs.csound())
    pt.play()
    
    # eternally loop until ctl+c
    try:
        while True:
            await asyncio.sleep(1)  # Keep the server alive
    except asyncio.CancelledError:
        print("\nShutdown signal received...")
    finally:
        print("Cleaning up...")
        cs.event_string('e')
        transport.close()  # Stop OSC server
        pt.stop()         # Stop Csound
        pt.join()        # Wait for Csound to finish
        print("Exit complete")
        sys.exit()



# # if script is run direclty (not imported as a library), run loop
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass  # Already handled by asyncio.CancelledError