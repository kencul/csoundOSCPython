# Open CV with Csound

Examples that uses computer vision to get data from pictures or video feeds to send to Csound.

## viewColorChannel.py

Example with no Csound implementation showcasing basic operations on the color channels of images.

### Usage

Place image files in the [imgs](src/opencv/imgs/) directory.

Run the program with dependencies installed.

Two windows will pop up: one with the image and another with a silder.

Moving the slider will change the color channel that is shown of the image.

Slider values:

0. Blue
1. Red
2. Green
3. All (normal)

## webcam.py

Opens the webcam feed and tracks red spots, and sends the xy coordinate of the box to csound as channel values.

### Usage

Run program, ensuring it has webcam access.

Two windows will open: one with the webcam feed and another with sliders.

By default, there will be no/bad tracking. You must set the color threshold to the environment through the sliders.

(todo: finish docs)

## playImage.py

Opens a image, and randomly selects a area of the image to analyze, and send analysis data to Csound for generative music piece.

Csound code inspired from Dr. B's "Trapped"

### Usage

Place image file(s) in imgs directory.

Run program. A random image found in the directory will be selected.

Two windows will open: one shows the image with a red square showing the area being analyzed, another showing the numerical color analysis data.

### Modifications

Basic changes to the performance can be made in the first section of code in `playImage.py` labeled `PERFORMANCE INITS`

- noteLength: the time between each note in seconds
- amp: the volume of each note played (0-1)
- noteOverlap: How long each note lasts, with 1 = noteLength
- numInstr: the number of instruments in the CSD which will be chosen randomly from