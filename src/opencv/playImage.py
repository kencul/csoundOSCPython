import cv2 as cv
import numpy as np
import copy
from matplotlib import pyplot as plt

def analyzeSquare(square):
    """Analyze an image square and return features of the square"""
    features = {}
    
    # Convert to different color spaces
    hsv = cv.cvtColor(square, cv.COLOR_BGR2HSV)
    lab = cv.cvtColor(square, cv.COLOR_BGR2LAB)
    gray = cv.cvtColor(square, cv.COLOR_BGR2GRAY)
    
    # Color features (simple averages)
    features['avg_bgr'] = np.mean(square, axis=(0,1))
    features['avg_hsv'] = np.mean(hsv, axis=(0,1))
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
    features['dominant_color'] = centers[0].astype(int) # Record BGR value of the most dominant color in the square
    
    return features

def create_feature_window(features, window_name="Features"):
    """Creates a feature display with color swatches"""
    # Create a blank black image (600x700 pixels for more space)
    feature_display = np.zeros((600, 700, 3), dtype=np.uint8)
    
    y_offset = 60  # Starting vertical position for text

    # Display each feature
    for key, value in features.items():
        if isinstance(value, (list, np.ndarray)):
            text = f"{key}: {[int(x) for x in value]}"
        else:
            text = f"{key}: {value:.2f}" if isinstance(value, float) else f"{key}: {value}"
        
        # Draw text
        cv.putText(feature_display, text, (10, y_offset), 
                   cv.FONT_HERSHEY_SIMPLEX, 0.8, (255, 50, 150), 1)
        
        # Draw color swatches for BGR and dominant color
        if key == 'avg_bgr':
            # Swatch for average BGR (size: 50x50 pixels)
            cv.rectangle(feature_display, (450, y_offset - 30), (500, y_offset + 20), 
                         [int(x) for x in value], -1)  # -1 = filled rectangle
            cv.putText(feature_display, "Avg Color", (510, y_offset), 
                       cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        
        elif key == 'dominant_color':
            # Swatch for dominant color
            cv.rectangle(feature_display, (450, y_offset - 30), (500, y_offset + 20), 
                         [int(x) for x in value], -1)
            cv.putText(feature_display, "Dominant", (510, y_offset), 
                       cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        
        y_offset += 60  # Extra spacing for swatches AKA indent

    cv.imshow(window_name, feature_display)

imgPaths = ["src\opencv\img\henri_matisse.jpg", "src\opencv\img\starrynight.jpg"]
imgPath = imgPaths[1]
windowName = "image"

rowDiv = 20
colDiv = 20

image = cv.imread(imgPath)
assert image is not None, "file could not be read, check with os.path.exists()"
rows, columns, channels = image.shape

roiWidth = (int)(columns / colDiv)
roiLength = (int)(rows / rowDiv)

xCoord = 0
yCoord = 0
while 1:
    outImg = copy.deepcopy(image)
    square = image[yCoord*roiLength:(yCoord+1)*roiLength, xCoord*roiWidth:(xCoord+1)*roiWidth]
    features = analyzeSquare(square)
    
    cv.rectangle(outImg,(xCoord * roiWidth,yCoord * roiLength),((xCoord+1) * roiWidth, (yCoord+1) * roiLength),(0,255,0),2)
    
    # end process when end of picture is reached
    if yCoord == rowDiv:
        break
    # iterate roi location
    xCoord = (xCoord+1) % (colDiv)
    # iterate down a row when x coord loops back
    if xCoord == 0:
        yCoord += 1
        
    # Display windows
    cv.imshow(windowName, outImg) # Image
    create_feature_window(features) # Feature data
    
    # break out if escape key is pressed
    k = cv.waitKey(1000) & 0xFF
    if k == 27:
        break

cv.destroyAllWindows()