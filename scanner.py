#!/usr/bin/env python3

import cv2
import numpy
import imutils
from imutils.perspective import four_point_transform

def find_circles(img):
	return cv2.HoughCircles(img, 
		cv2.HOUGH_GRADIENT, 1, 20, param1=50, 
		param2=30, minRadius=1, maxRadius=22)

def find_contours(img):
	contours, hierarchy = cv2.findContours(img, 
		cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	if contours:
		return sorted(contours, key=cv2.contourArea, reverse=True)
	return None

if __name__ == '__main__':
	img = cv2.imread('out/out.png')
	result = img.copy()
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	blurred = cv2.GaussianBlur(gray, (3, 3), 0)
	edged = cv2.Canny(blurred, 20, 150)
	print(find_contours(blurred))
	blurred = cv2.drawContours(blurred, find_contours(blurred), -1, (0, 255, 0))

	for c in find_contours(blurred):
		peri = 0.02 * cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, peri, True)
		if len(approx) == 4:
			docCnt = approx

	thresh = cv2.inRange(img, (0, 0, 0), (255, 255, 255))
	kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (22, 22))
	morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
	morph = cv2.morphologyEx(morph, cv2.MORPH_OPEN, kernel)
	paper = four_point_transform(img, docCnt.reshape(4, 2))
	warped = four_point_transform(gray, docCnt.reshape(4, 2))
	width, height = int(paper.shape[0] // 2.95), int(paper.shape[0] // 11)
	paper = paper[height:paper.shape[0], width:paper.shape[1]]
	'''
	circles = numpy.uint16(numpy.around(find_circles(blurred)))
	for i in circles[0, :]:
		cv2.circle(blurred, (i[0], i[1]), i[2], (0, 255, 0), 2)
	'''
	cv2.imwrite('out/test.png', morph)
