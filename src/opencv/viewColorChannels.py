import cv2 as cv
import numpy as np
from pathlib import Path

import copy


def nothing(x):
    pass

base_dir = Path(__file__).parent  # Script's directory
img_dir = base_dir / "imgs"
img_paths = [
    img_dir / "still_life.jpg",
    img_dir / "still_life2.jpg",
    img_dir / "starrynight.jpg"
]

imgPath = img_paths[2]

# Reading an image in default mode
image = cv.imread(str(imgPath.absolute()))
imgfiltered = copy.deepcopy(image)
# Initialize windows with proper flags
cv.namedWindow("sliders", cv.WINDOW_NORMAL | cv.WINDOW_GUI_EXPANDED)
cv.namedWindow("window_name", cv.WINDOW_NORMAL | cv.WINDOW_GUI_EXPANDED)
cv.createTrackbar('Channels', "sliders", 0, 3, nothing)

channelPrev = -1
while(1):
    # Display images first
    cv.imshow("window_name", imgfiltered)
    cv.imshow("sliders", np.zeros((100, 400, 3), dtype=np.uint8))  # Dummy image for slider window

    # break out if escape key is pressed
    k = cv.waitKey(1) & 0xFF
    if k == 27:
        break
    
    
    # threshold = cv.getTrackbarPos('Threshold', 'sliders')
    channel = cv.getTrackbarPos('Channels', 'sliders')
    
    # if new color channel is selected
    if channel != channelPrev:
        # save choice
        channelPrev = channel
        # reset image to reference
        imgfiltered = copy.deepcopy(image)
    
        # filter out other 3 color channels outside the selected one
        # 0 - blue, 1 - green, 2 - red, 3 - bgr
        match channel:
            case 0:
                imgfiltered[:,:,1:3] = 0
            case 1:
                imgfiltered[:,:,0] = 0
                imgfiltered[:,:,2] = 0
            case 2:
                imgfiltered[:,:,0:2] = 0
            case 3:
                pass
        
            
    #ret, mask = cv.threshold(imgfiltered, threshold, 255, cv.THRESH_BINARY)
    
    #cv.imshow("window_name", imgfiltered)
cv.destroyAllWindows()