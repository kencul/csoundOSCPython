# REF: (pythonOSC docs)[https://python-osc.readthedocs.io/en/latest/server.html]

# FOR USE WITH "DATAOSC" IOS APP

import threading
import time

import asyncio

from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import AsyncIOOSCUDPServer
import numpy as np
import ctcsound

# REF: (csound python docs)[https://github.com/csound/ctcsound/blob/master/cookbook/02-performing.ipynb]
cs = ctcsound.Csound()
# ret = cs.compileCsd("csound.csd")
# if ret != ctcsound.CSOUND_SUCCESS:
#     exit()
csd = '''
<CsoundSynthesizer>
<CsOptions>
-odac
</CsOptions>
<CsInstruments>
sr = 44100
ksmps = 64
nchnls = 2
0dbfs = 1
seed 0

instr 1
 iPch random 60, 72
 chnset iPch, "pch"
 kPch init iPch
 kNewPch chnget "new_pitch"
 if kNewPch > 0 then
  kPch = portk(kNewPch, 0.1)
 endif
 aTone poscil .2, mtof(kPch)
 out aTone, aTone
endin

</CsInstruments>
<CsScore>
i 1 0 60000
</CsScore>
</CsoundSynthesizer>
'''
cs.compileCsdText(csd)

cs.start()
pt = ctcsound.CsoundPerformanceThread(cs.csound())
pt.play()


def print_handler(address, *args):
    #print(f"{address}: {args}") 
    val = args[0]
    cs.setControlChannel('new_pitch',73 + val)

def default_handler(address, *args):
    #print(f"DEFAULT {address}: {args}")
    pass # do nothing

# FILTERING OSC ADDRESSES TO CALLBACK FUNCTIONS
dispatcher = Dispatcher()
dispatcher.map("/data/motion/gyroscope/x", print_handler)
# default funciton called when message doesnt match any addresses
dispatcher.set_default_handler(default_handler)


# CHANGE IP TO MATCH DEVICE IP
ip = "192.168.0.134"
port = 8000

# loop to handle osc messages
async def main():
    # start async osc server
    server = AsyncIOOSCUDPServer((ip, port), dispatcher, asyncio.get_event_loop())
    transport, protocol = await server.create_serve_endpoint()

    # eternally loop until ctl+c
    try:
        while True:
            await asyncio.sleep(1)  # Keep the server alive
    except asyncio.CancelledError:
        print("\nShutdown signal received...")
    finally:
        print("Cleaning up...")
        transport.close()  # Stop OSC server
        pt.stop()         # Stop Csound
        pt.join()        # Wait for Csound to finish
        cs.reset()       # Release Csound resources
        print("Exit complete")


# if script is run direclty (not imported as a library), run loop
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass  # Already handled by asyncio.CancelledError