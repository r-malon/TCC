#!/usr/bin/env python3

import cv2
import numpy
'''
def find_circles(img):
	return cv2.HoughCircles(img, 
		cv2.HOUGH_GRADIENT, 1, 20, param1=50, 
		param2=30, minRadius=1, maxRadius=22)
'''
def crop(img, margin_x, margin_y):
	return img[margin_y:-margin_y, margin_x:-margin_x]

def cut(img, n_pieces, horizontal=False):
	h, w = img.shape[:2]
	size = h//n_pieces if horizontal else w//n_pieces
	return [img[i*size:(i+1)*size, :] if horizontal 
		else img[:, i*size:(i+1)*size] for i in range(n_pieces)]

def get_rects(img, slicer=slice(0, None), method=cv2.RETR_EXTERNAL):
	contours, hierarchy = cv2.findContours(img, 
		method, cv2.CHAIN_APPROX_SIMPLE)
	if contours:
		rects = []
		contours = sorted(contours, key=cv2.contourArea, reverse=True)
		for c in contours[slicer]:
			peri = 0.01 * cv2.arcLength(c, True)
			approx = cv2.approxPolyDP(c, peri, True)
			if len(approx) == 4:
				rects.append(approx)
		return rects
	return None


if __name__ == '__main__':
	img = cv2.imread('out/out.png')
	result = img.copy()
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	blurred = cv2.GaussianBlur(gray, (7, 7), 0)
	thresh = cv2.adaptiveThreshold(blurred, 255, 
		cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
	edged = cv2.Canny(thresh, 20, 3*20)
	outers = get_rects(edged, slice(0, 3))
#	mask = numpy.zeros(gray.shape, numpy.uint8)
#	result = cv2.bitwise_and(gray, mask)
#	cv2.drawContours(result, outers[:6], -1, (0, 255, 0))
	cv2.drawContours(result, outers, -1, (255, 0, 0))
	roi_n = 0
	for c in outers:
		(x, y, w, h) = cv2.boundingRect(c)
		# extent = float(cv2.contourArea(c)) / (w*h)
		box = edged[y:y+h, x:x+w]
		inners = get_rects(box, method=cv2.RETR_TREE)
		for v in inners:
			(x, y, w, h) = cv2.boundingRect(v)
			aspect_ratio = float(w)/h
			if aspect_ratio != 1.0 and aspect_ratio > 3:
				cv2.rectangle(result, (x, y), (x+w, y+h), (0, 255, 0), 1)
				inner_box = crop(box[y:y+h, x:x+w], 5, 5)
				opt_box = cut(inner_box, 5)
				for i in range(5):
					cv2.imwrite(f'out/test_{roi_n}_{i}.png', opt_box[i])
				roi_n += 1
		# _, thresh = cv2.threshold(box, 0, 255, cv2.THRESH_BINARY|cv2.THRESH_OTSU)
		# mask = cv2.bitwise_not(thresh)
		# cv2.drawContours(result[y:y+h, x:x+w], inners, -1, (0, 255, 0))
	cv2.imwrite('out/test.png', result)

'''
circles = numpy.uint16(numpy.around(find_circles(edged)))
for i in circles[0, :]:
	cv2.circle(result, (i[0], i[1]), i[2], (0, 255, 0), 2)
'''
