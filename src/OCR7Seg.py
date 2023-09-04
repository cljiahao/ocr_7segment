import cv2
import numpy as np

####################################################################################################
# Initialization
digitsArr= {
    (1, 1, 1, 0, 1, 1, 1): 0,
    (0, 0, 1, 0, 0, 1, 0): 1,
    (1, 0, 1, 1, 1, 0, 1): 2,
    (1, 0, 1, 1, 0, 1, 1): 3,
    (0, 1, 1, 1, 0, 1, 0): 4,
    (1, 1, 0, 1, 0, 1, 1): 5,
    (1, 1, 0, 1, 1, 1, 1): 6,
    (1, 0, 1, 0, 0, 1, 0): 7,
    (1, 1, 1, 1, 1, 1, 1): 8,
    (1, 1, 1, 1, 0, 1, 1): 9
}
####################################################################################################

def threshold():
    segWidth = 0.35
    segHeight = 0.2
    segCenter = 0.075
    segArea = 0.5

    return [segWidth,segHeight,segCenter,segArea]

def debug(img):
    cv2.namedWindow('img',cv2.WINDOW_FREERATIO)
    cv2.imshow("img",img)
    cv2.waitKey(0)

# Mask the image to return the 7 segment digits
def masking(img):

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(3,3),0)
    ret,thresh = cv2.threshold(blur,150,255,cv2.THRESH_BINARY)
    morph = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,np.ones((11,11),np.uint8))
    dilate = cv2.dilate(morph,np.ones((27,27),np.uint8))

    return dilate

def segment(img,mask,th):
    
    copy = img.copy()
    cont,hier = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    digits,dContArr = [],[]

    for c in cont:
        if cv2.contourArea(c) < 3000: continue
        # extract the digit ROI
        (x, y, w, h) = cv2.boundingRect(c)
        if h < w*1.1: continue
        dContArr.append([x,y,w,h,c])

    for x,y,w,h,c in sorted(dContArr,key=lambda k: k[0]):
        if cv2.contourArea(c) < 50000: 
                digit = 1
                digits.append(digit) 
        else:
            roi = mask[y:y+h, x:x+w]
            #####
            # debug(roi)
            #####
            # Get the digit's height and width and 7 segment relative height and width
            (roiH, roiW) = roi.shape
            (segW, segH) = (int(roiW * th[0]), int(roiH * th[1]))
            segC = int(roiH * th[2])

            # Coordinates for each segments of the 7 segments
            segments = [
                ((0, 0), (w, segH)),	                            # top
                ((0, 0), (segW, h // 2)),	                        # top-left 
                ((w - segW, 0), (w, h // 2)),	                    # top-right
                ((0, (h // 2) - segC) , (w, (h // 2) + segC)),      # center
                ((0, h // 2), (segW, h)),	                        # bottom-left
                ((w - segW, h // 2), (w, h)),	                    # bottom-right
                ((0, h - segH), (w, h))	                            # bottom
            ]

            segArr = []

            for ((xA, yA), (xB, yB)) in segments:
                
                # Get individual segment, area exists more than certain % 
                segROI = roi[yA:yB, xA:xB]
                total = cv2.countNonZero(segROI)
                area = (xB - xA) * (yB - yA)
                #####
                # debug(segROI)
                #####
                segArr.append(1) if total / float(area) > th[3] else segArr.append(0)
            try:
                digit = digitsArr[tuple(segArr)]
                digits.append(str(digit))
            except: continue
        cv2.rectangle(copy, (x, y), (x + w, y + h), (0, 255, 0), 3)
        cv2.putText(copy, str(digit), (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
        #####
        # debug(copy)
        #####
        
    
    digits.insert(1,".")

    return copy, digits

def OCR7Seg(img):
    th = threshold()
    mask = masking(img)
    return segment(img,mask,th)