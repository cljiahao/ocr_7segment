import cv2
import numpy as np
from PIL import Image

# filepath = r"C:\Users\MES21106\Desktop\test\tesseract\GP machine\images\WIN_20230718_10_15_37_Pro.jpg" 
# filepath = r"C:\Users\MES21106\Desktop\test\tesseract\GP machine\images\WIN_20230713_08_51_17_Pro.jpg"
# filepath = r"C:\Users\MES21106\Desktop\test\tesseract\GP machine\images\WIN_20230718_10_18_58_Pro.jpg"
# filepath = r"C:\Users\MES21106\Desktop\test\tesseract\GP machine\images\WIN_20230718_10_19_10_Pro.jpg"
filepath = r"C:\Users\MES21106\Desktop\test\tesseract\GP machine\images\WIN_20230718_10_18_58_Pro.jpg"
# filepath = r"C:\Users\MES21106\Desktop\test\tesseract\GP machine\images\WIN_20230718_10_16_31_Pro.jpg"

cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)

DIGITS_LOOKUP = {
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

cv2.namedWindow("img",cv2.WINDOW_FREERATIO)
while True:
    image = cv2.imread(filepath)
    # ret,image = cap.read()
    copy = image.copy()
    img = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(img,(3,3),0)
    ret,thresh = cv2.threshold(blur,150,255,cv2.THRESH_BINARY)
    morph = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,np.ones((11,11),np.uint8))
    dilate = cv2.dilate(morph,np.ones((27,27),np.uint8))

    # cv2.imshow("img",dilate)
    # cv2.waitKey(0)

    cont,hier = cv2.findContours(dilate,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    dContArr = []

    for c in cont:
        if cv2.contourArea(c) < 3000: continue
        # extract the digit ROI
        (x, y, w, h) = cv2.boundingRect(c)
        if h < w*1.1: continue
        dContArr.append([x,y,w,h,c])

    digits = []
    # loop over each of the digits
    for x,y,w,h,c in sorted(dContArr,key=lambda k: k[0]):
        # print(cv2.contourArea(c))

        print(cv2.contourArea(c))
        if cv2.contourArea(c) < 50000: 
                digit = 1
                digits.append(digit) 
        else:
            roi = dilate[y:y + h, x:x + w]
            
            # cv2.imshow("img",roi)
            # cv2.waitKey(0)
            # compute the width and height of each of the 7 segments
            # we are going to examine
            (roiH, roiW) = roi.shape
            (dW, dH) = (int(roiW * 0.35), int(roiH * 0.2))
            dHC = int(roiH * 0.075)
            # define the set of 7 segments
            segments = [
                ((0, 0), (w, dH)),	# top
                ((0, 0), (dW, h // 2)),	# top-left 
                ((w - dW, 0), (w, h // 2)),	# top-right
                ((0, (h // 2) - dHC) , (w, (h // 2) + dHC)), # center
                ((0, h // 2), (dW, h)),	# bottom-left
                ((w - dW, h // 2), (w, h)),	# bottom-right
                ((0, h - dH), (w, h))	# bottom
            ]
            on = [0] * len(segments)

                # loop over the segments
            for (i, ((xA, yA), (xB, yB))) in enumerate(segments):
                # extract the segment ROI, count the total number of
                # thresholded pixels in the segment, and then compute
                # the area of the segment
                segROI = roi[yA:yB, xA:xB]
                # cv2.imshow("test",segROI)
                # cv2.waitKey(0)
                total = cv2.countNonZero(segROI)
                area = (xB - xA) * (yB - yA)
                # if the total number of non-zero pixels is greater than
                # 50% of the area, mark the segment as "on"
                if total / float(area) > 0.5:
                    on[i]= 1
            # lookup the digit and draw it on the image
            try:
                digit = DIGITS_LOOKUP[tuple(on)]
                digits.append(digit)
            except: continue
        print(digits)
        cv2.rectangle(copy, (x, y), (x + w, y + h), (0, 255, 0), 1)
        cv2.putText(copy, str(digit), (x - 10, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0), 2)

    cv2.imshow("img",copy)
    # cv2.waitKey(0)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    
