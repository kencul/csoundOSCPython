import cv2 as cv
import numpy as np
import ctcsound

# dummy callback func to pass to trackbar
def nothing(x):
    pass

# Get webcam video
cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Failed to open camera!")
    exit()
    
# Init trackbar window
cv.namedWindow("sliders")
cv.createTrackbar('Threshold',"sliders",0,255,nothing)
cv.createTrackbar('Mode',"sliders",0,1,nothing)
cv.createTrackbar('Volume',"sliders",0,255,nothing)

# Get init frame from webcam
ret, frame = cap.read()

# Get screen resolution and num color channels
rows, columns, channels = frame.shape

# Process init frame
r = frame[:,:,2]
ret, mask = cv.threshold(r, 0, 255, cv.THRESH_BINARY)

# setup initial location of window
x, y, w, h = 300, 200, 70, 70 # simply hardcoded the values
track_window = (x, y, w, h)
 
# set up the ROI for tracking
roi = mask[y:y+h, x:x+w]
roi_hist = cv.calcHist([roi], [0], None, [256], [0, 256])
cv.normalize(roi_hist, roi_hist, 0, 255, cv.NORM_MINMAX)
 
# Setup the termination criteria, either 10 iteration or move by at least 1 pt
term_crit = ( cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 1 )

# --------------------------------------------
# Csound init

# Create the Csound engine instance
cs = ctcsound.Csound()
csd = f'''
        <CsoundSynthesizer>
        <CsOptions>
        -odac -W
        </CsOptions>
        <CsInstruments>
        sr = 44100
        ksmps = 64
        nchnls = 2
        0dbfs = 1
        seed 0
        
        instr 1
        kX init 0
        kX chnget "x"
        if kX > 0 then
            kfreq = portk(kX, 0.1)
        endif
        
        kY init 0
        kY chnget "y"
        if kY > 0 then
            kfilt = portk(kY, 0.1)
        endif
        
        kVol init 0
        kVol chnget "vol"
        kAmp = portk(kVol, 0.1)
        
        asig = vco2(0.7 * kAmp, 440 * (1 + kfreq))
        asig = moogladder(asig, kfilt * 11000, 0.5)
        outs asig, asig
        endin
        
        </CsInstruments>
        <CsScore>
        i1 0 60000
        </CsScore>
        </CsoundSynthesizer>
        '''
        
ret = cs.compile_csd(csd, 1)
if ret is not ctcsound.CSOUND_SUCCESS:
    print("Csound init failed!")
    exit()
    
csound_performance_thread = ctcsound.CsoundPerformanceThread(cs.csound())
# Start engine
res = cs.start()
if ret is not ctcsound.CSOUND_SUCCESS:
    print("Csound failed to start!")
    exit()

# start performance thread
csound_performance_thread.play()

while(1):
    # Check if Csound is running
    if not csound_performance_thread.is_running():
        print("Csound no longer running! Exiting...")
        break
    
    # Capture frame-by-frame
    ret, frame = cap.read()
 
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    
    # Get trackbar values
    threshold = cv.getTrackbarPos('Threshold', 'sliders')
    mode = cv.getTrackbarPos('Mode', 'sliders')
    vol = cv.getTrackbarPos('Volume', 'sliders')
    
    # Process image mask
    r = frame[:,:,2]
    ret, mask = cv.threshold(r, threshold, 255, cv.THRESH_BINARY)
    
    # Calculate back projection using grayscale histogram
    dst = cv.calcBackProject([mask], [0], roi_hist, [0, 256], 1)
    
    # Apply MeanShift
    ret, track_window = cv.meanShift(dst, track_window, term_crit)
    
    # Show mask if mode set to 1
    if mode == 1:
        frame[:,:,2] = mask
        frame[:,:,0:2] = 0

    # Draw it on image
    x,y,w,h = track_window
    img2 = cv.rectangle(frame, (x,y), (x+w,y+h), (0, 255, 0), 2)
    
    # Show result image
    cv.imshow('MeanShift Tracking',img2)
    
    # Csound input
    csX = (x + w/2)/ columns
    csY = (y + h/2)/ rows
    
    # Send control signal to Csound
    cs.set_control_channel("x", csX)
    cs.set_control_channel("y", csY)
    cs.set_control_channel("vol", vol/255)
    
    if cv.waitKey(1) == ord('q'):
        break
 
# End program
cs.event_string('e 0')
# Join thread an wait for it to finish
csound_performance_thread.join()
# When everything done, release the capture
cap.release()
cv.destroyAllWindows()