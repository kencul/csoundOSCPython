import cv2 as cv
import numpy as np

import copy


def nothing(x):
    pass

path = "henri_matisse.jpg"

# Reading an image in default mode
image = cv.imread(path)
window_name = "image"

# returns (rows, columns, channels)
# rows, columns, channels = image.shape

# Split rgb channels of img
# b, g, r = cv.split(image)

# Change to grayscale and apply threshold
# imggray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
# ret, mask = cv.threshold(imggray, 70, 255, cv.THRESH_BINARY)


cv.namedWindow("sliders")
# cv.createTrackbar('Threshold',"sliders",0,255,nothing)
cv.createTrackbar('Channel',"sliders",0,3,nothing)

channelPrev = -1
while(1):
    # break out if escape key is pressed
    k = cv.waitKey(1) & 0xFF
    if k == 27:
        break
    
    
    # threshold = cv.getTrackbarPos('Threshold', 'sliders')
    channel = cv.getTrackbarPos('Channel', 'sliders')
    
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
    
    cv.imshow("window_name", imgfiltered)
cv.destroyAllWindows()