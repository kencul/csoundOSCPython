import cv2 as cv
import numpy as np
import copy
from matplotlib import pyplot as plt


imgPath = "henri_matisse.jpg"
# imgPath = "KafuBackground.jpg"
windowName = "image"

rowDiv = 50
colDiv = 6

image = cv.imread(imgPath)
assert image is not None, "file could not be read, check with os.path.exists()"
rows, columns, channels = image.shape

roiWidth = (int)(columns / colDiv)
roiLength = (int)(rows / rowDiv)

# color = ('b','g','r')
# for i,col in enumerate(color):
#     histr = cv.calcHist([image],[i],None,[256],[0,256])
#     plt.plot(histr,color = col)
#     plt.xlim([0,256])
# plt.ion()
# plt.show(block=False)
# plt.draw()
# plt.pause(0.001)

xCoord = 0
yCoord = 0
while 1:
    outImg = copy.deepcopy(image)
    cv.rectangle(outImg,(xCoord * roiWidth,yCoord * roiLength),((xCoord+1) * roiWidth, (yCoord+1) * roiLength),(0,255,0),3)
    
    # end process when end of picture is reached
    if yCoord == rowDiv:
        break
    # iterate roi location
    xCoord = (xCoord+1) % (colDiv)
    # iterate down a row when x coord loops back
    if xCoord == 0:
        yCoord += 1
    cv.imshow(windowName, outImg)
    # break out if escape key is pressed
    k = cv.waitKey(1000) & 0xFF
    if k == 27:
        break

cv.destroyAllWindows()