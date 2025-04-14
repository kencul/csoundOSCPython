# OSC to Python to Csound

### Usage
Ensure all dependencies are installed and python environment is activated (see root directory [README.md](../../README.md))

Run [`oscServer.py`](oscServer.py):  
```
python oscServer.py
```

Change active directory to the `OSC/` directory
```
cd src/OSC/
```

The script will detect your device IP automatically, and prompt to start the osc server.  
Change the port by changing the variable value in `oscServer.py` line 127  
Press enter to start the server.

### Sending OSC messages

For development, the iOS app [Data OSC](https://apps.apple.com/us/app/data-osc/id6447833736) was used, but any form of OSC messaging will work.

Data OSC can send gyroscope data from an iPhone over OSC.  
The x axis rotation affects wavetable position between sine and saw.  
The y axis rotation affects vibrato and panning.

### Changing Csound

Modify [`osc.csd`](osc.csd) to change the audio output

Uses Csound7 API function calls, incompatible with Csound6

### oscClient
[`oscClient.py`](oscClient.py) is a basic python script that sends OSC messages.

Can be used to debug OSC messages by sending to local IP (127.0.0.1)

### Issues

Terminating the program still takes mutliple keyboard interrupt commands