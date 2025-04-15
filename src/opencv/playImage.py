import cv2 as cv
import numpy as np
import copy
from matplotlib import pyplot as plt

import random
from datetime import datetime
random.seed(datetime.now().timestamp())

import ctcsound
import sys

# Csound init
cs = ctcsound.Csound()
csd = "src\CSD\playImg.csd"

# Compile csd
result = cs.compile_csd(csd, 0)
if result != ctcsound.CSOUND_SUCCESS:
    print(f"Error compiling csd!", file=sys.stderr)
    sys.exit(1)

# Start performance thread
csThread = ctcsound.CsoundPerformanceThread(cs.csound())

# Start the engine    
result = cs.start()

if result != ctcsound.CSOUND_SUCCESS:
    print(f"Error starting Csound!", file=sys.stderr)
    sys.exit(1)

# Start thread
csThread.play()

# --------------------------------------------------------------------------------------
# openCV init

def analyzeSquare(square):
    """Analyze an image square and return features of the square"""
    features = {}
    
    # Convert to different color spaces
    hsv = cv.cvtColor(square, cv.COLOR_BGR2HSV)
    lab = cv.cvtColor(square, cv.COLOR_BGR2LAB)
    gray = cv.cvtColor(square, cv.COLOR_BGR2GRAY)
    
    # Color features (simple averages)
    features['avg_bgr'] = np.mean(square, axis=(0,1)) # bgr values from 0-255
    features['avg_hsv'] = np.mean(hsv, axis=(0,1)) # hue values from 0-179
    features['brightness'] = np.mean(gray)/255 # Scaled between 0-1
    
    # Texture features
    features['contrast'] = min(np.std(gray) / 127.5, 1.0) # Find standard deviation of grayscale image (contrast), scaled between 0-1 and clipped
    edges = cv.Canny(gray, 100, 200) # Find edges in the square
    features['edge_density'] = np.sum(edges) / (edges.size * 255) # Find how much of the square the edges occupy percentage wise in the square
    
    # Dominant color via k-means
    pixels = square.reshape((-1,3)) # 2D array of bgr values of each pixel (50x50x3) -> (2500, 3)
    pixels = np.float32(pixels) # Convert values to float to prepare for cv.kmeans()
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 10, 1.0) # Run kmeans for 10 iterations or until no movement
    _, labels, centers = cv.kmeans(pixels, 1, None, criteria, 10, cv.KMEANS_RANDOM_CENTERS) # Find cluster of most dominant color in square
    dominant_bgr = centers[0].astype(int)
    features['dominant_color_bgr'] = dominant_bgr

    # Convert dominant BGR to HSV
    dominant_hsv = cv.cvtColor(np.uint8([[dominant_bgr]]), cv.COLOR_BGR2HSV)[0][0]
    features['dominant_color_hsv'] = dominant_hsv
    
    return features

def create_feature_window(features, window_name="Features"):
    """Creates a feature display with guaranteed color swatches"""
    feature_display = np.zeros((600, 700, 3), dtype=np.uint8)
    y_offset = 60  # Starting Y position

    # Ensure consistent key names (match your analyze_square() output)
    bgr_key = 'avg_bgr' if 'avg_bgr' in features else 'average_color_bgr'
    dominant_key = 'dominant_color' if 'dominant_color' in features else 'dominant_color_bgr'

    # Draw all features
    for key, value in features.items():
        # Format text
        if isinstance(value, (list, np.ndarray)):
            text = f"{key}: {[int(x) for x in value]}"
        else:
            text = f"{key}: {value:.2f}" if isinstance(value, float) else f"{key}: {value}"
        
        cv.putText(feature_display, text, (10, y_offset), 
                  cv.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)

        # Draw swatches (regardless of iteration order)
        if key == bgr_key:
            color = [int(x) for x in value] if isinstance(value, np.ndarray) else value
            cv.rectangle(feature_display, (450, y_offset-25), (500, y_offset+25), color, -1)
            cv.putText(feature_display, "Avg", (510, y_offset+10), 
                      cv.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 1)
        
        elif key == dominant_key:
            color = [int(x) for x in value] if isinstance(value, np.ndarray) else value
            cv.rectangle(feature_display, (450, y_offset-25), (500, y_offset+25), color, -1)
            cv.putText(feature_display, "Dom", (510, y_offset+10),
                      cv.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 1)

        y_offset += 60  # Spacing

    cv.imshow(window_name, feature_display)

def hueToInstr(hue, numInstruments):
    """CCasts hue to a instrument number based on the number of instruments (returns 0 index)"""
    hueScale = hue/179.0 # convert 0-179 scale to 0-1
    instrIndex = int(hueScale * numInstruments) # floor rounding to instrument number
    return min(instrIndex, instrIndex) # clamp to highest instr number

imgPaths = ["src\opencv\img\henri_matisse.jpg", "src\opencv\img\starrynight.jpg"]
imgPath = imgPaths[0]
windowName = "image"

rowDiv = 20
colDiv = 20

image = cv.imread(imgPath)
assert image is not None, "file could not be read, check with os.path.exists()"
rows, columns, channels = image.shape

roiWidth = (int)(columns / colDiv)
roiLength = (int)(rows / rowDiv)

xCoord = random.randrange(0, colDiv)
yCoord = random.randrange(0, rowDiv)

# ------------------------------------------------------------------------
# PERFORMANCE INITS
noteLength = 10
amp = 0.2
noteOverlap = 0.8
numInstr = 2

while 1:
    outImg = copy.deepcopy(image)
    square = image[yCoord*roiLength:(yCoord+1)*roiLength, xCoord*roiWidth:(xCoord+1)*roiWidth]
    features = analyzeSquare(square)
    
    cv.rectangle(outImg,(xCoord * roiWidth,yCoord * roiLength),((xCoord+1) * roiWidth, (yCoord+1) * roiLength),(0,255,0),2)
    
    # # end process when end of picture is reached
    # if yCoord == rowDiv:
    #     break
    # # iterate roi location
    # xCoord = (xCoord+1) % (colDiv)
    # # iterate down a row when x coord loops back
    # if xCoord == 0:
    #     yCoord += 1
    
    ## randomly select a box
    xCoord = random.randrange(0, colDiv)
    yCoord = random.randrange(0, rowDiv)
        
    # Display windows
    cv.imshow(windowName, outImg) # Image
    create_feature_window(features) # Feature data
    
    
    # Play note in csound
    randInstr = hueToInstr(features['avg_hsv'][0], numInstr) + 1
    msg = f"i{randInstr} 0 {noteLength * noteOverlap} {features['brightness']} {features['dominant_color_hsv'][0]/255} {amp} {features['contrast']}"
    # print(msg)
    cs.event_string(msg)
    
    # break out if escape key is pressed
    k = cv.waitKey(noteLength * 1000) & 0xFF
    if k == 27:
        break
cs.event_string('e 0')
csThread.join()
cv.destroyAllWindows()