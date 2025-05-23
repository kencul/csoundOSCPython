# Csound with OSC Control With Python
## Ken Kobayashi - April 8th, 2025

### Set-up

Create python environment:
~~~
python -m venv env  # (or `python3` if needed)
source env/bin/activate  # (Mac/Linux)
.\env\Scripts\activate # (Windows)
~~~

### Install dependencies:
~~~
pip install -r requirements.txt
~~~

Copy `ctcsound.py` file from csound installation (csound/bin/ctcsound.py) into `/env/Lib/site-packages`.  
**EXAMPLES USE CSOUND7: PLEASE BUILD FROM THE DEVELOPMENT BRANCH FROM THE CSOUND GITHUB**

Download `MikTeX` from their [website](https://miktex.org/download) for typeset support in `manim`

Download `ffmpeg` from this [website](https://www.gyan.dev/ffmpeg/builds/) for video output from `manim`