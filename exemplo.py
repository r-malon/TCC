import numpy as np
import cv2
import imutils
from imutils import contours
from imutils.perspective import four_point_transform

correct = ct = 0
gb = [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]

ct = 0
image = cv2.imread('./out/gabarito.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (3, 3), 0)
edged = cv2.Canny(blurred, 20, 150)
cv2.imshow('Camera', edged)
cv2.moveWindow('Camera', 0, 0)
cnts = cv2.findContours(edged.copy(), 
	cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
cnts = cnts[0] if imutils.is_cv2() else cnts[1]
docCnt = None

if len(cnts) > 0:
	cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
	for c in cnts:
		peri = 0.02 * cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, peri, True)
		if len(approx) == 4:
			ct = 1
			docCnt = approx

if ct == 1:
	paper = four_point_transform(image, docCnt.reshape(4, 2))
	warped = four_point_transform(gray, docCnt.reshape(4, 2))
	width, height = paper.shape[0] // 2.95, paper.shape[0] // 11
	paper = paper[height:paper.shape[0], width:paper.shape[1]]
	thresh = cv2.threshold(warped, 0, 255, 
		cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
	thresh = thresh[height:thresh.shape[0], width:thresh.shape[1]]
	if thresh.shape[0] > 0 and thresh.shape[1] > 0:
		cnts = cv2.findContours(thresh.copy(), 
			cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
		cnts = cnts[0] if imutils.is_cv2() else cnts[1]
		questionCnts = []
		for c in cnts:
			size = thresh.shape[1] / 5
			(x, y, w, h) = cv2.boundingRect(c)
			ar = w / float(h)
			approx = cv2.approxPolyDP(c, peri, True)
			if (w <= size and h < size) and \
				(ar >= 1.6 and ar <= 2.6) and \
				(w > size/10 and h > size/10):
				questionCnts.append(c) 
			print(len(questionCnts))

x = y = cont = 0
res = bubbled = question = questionCnts = []

for (q, i) in enumerate(np.arange(0, len(questionCnts), 5)):
	cont = 0
	cnts = contours.sort_contours(questionCnts[i:i + 5])[0]
	bubbled = []
	for (j, c) in enumerate(cnts):
		x, y = thresh.shape[0], thresh.shape[1]
		mask = np.zeros(thresh.shape, dtype='uint8')
		cv2.drawContours(mask, [c], -1, 255, -1)
		mask = cv2.bitwise_and(thresh, thresh, mask=mask)
		total = cv2.countNonZero(mask)
	if total > x//20 * y//10:
		bubbled.append(j)
		cont += 1
	if cont == 1:
		res.append(bubbled[0])
	else:
		res.append(-1)
		color = (0, 0, 255)
		k = gb[q]
	if cont == 1:
		if k == bubbled[0]:
			color = (0, 255, 0)
			correct += 1
	for s in range (cont):
		cv2.drawContours(paper, [cnts[bubbled[s]]], -1, color, 3)

res2 = []
for i in range(len(res)):
	res2.append(res[len(res)-i-1])

print('Gabarito:', gb)
print('Respostas:', res2)
print('Nota:', float(correct))
cv2.imshow('Answer Sheet', paper)
cv2.waitKey(0)
cv2.imshow('real', image)
cv2.waitKey(0)
