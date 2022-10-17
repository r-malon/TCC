#!/usr/bin/env python3

import cv2
import numpy

# read image
img = cv2.imread('omr_sheet.jpg')
h, w = img.shape[:2]

# trim 15 from bottom to remove partial answer
img = img[0:(h-15), 0:w]

# threshold on color
lower = (120, 60, 80)
upper = (160, 100, 120)
thresh = cv2.inRange(img, lower, upper)

# apply morphology close
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
morph = cv2.morphologyEx(morph, cv2.MORPH_OPEN, kernel)

# get contours
result = img.copy()
centers = []
contours = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
contours = contours[0] if len(contours) == 2 else contours[1]
print('count: ', len(contours))

i = 1
for cntr in contours:
	M = cv2.moments(cntr)
	cx = int(M['m10'] / M['m00'])
	cy = int(M['m01'] / M['m00'])
	centers.append((cx, cy))
	cv2.circle(result, (cx, cy), 20, (0, 255, 0), -1)
	pt = (cx, cy)
	print('circle #:', i, 'center:', pt)
	i = i + 1

# print list of centers
#print(centers)

# save results
cv2.imwrite('omr_sheet_thresh.png', thresh)
cv2.imwrite('omr_sheet_morph.png', morph)
cv2.imwrite('omr_sheet_result.png', result)
# show results
cv2.imshow('thresh', thresh)
cv2.imshow('morph', morph)
cv2.imshow('result', result)

cv2.waitKey(0)
cv2.destroyAllWindows()
