#!/usr/bin/env python3

import cv2
import numpy as np
import string

def crop(img, margin_x, margin_y):
	return img[margin_y:-margin_y, margin_x:-margin_x]

def crop_black(img):
	y_nonzero, x_nonzero = np.nonzero(img)
	return img[
		np.min(y_nonzero):np.max(y_nonzero+1), 
		np.min(x_nonzero):np.max(x_nonzero+1)]

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

def deduplicate(array):
	uniques = []
	for arr in array:
		if not any(np.array_equal(arr, unique_arr) for unique_arr in uniques):
			uniques.append(arr)
	return uniques

if __name__ == '__main__':
	img = cv2.imread('out/out.png')
	result = img.copy()
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	blurred = cv2.GaussianBlur(gray, (7, 7), 0)
	thresh = cv2.adaptiveThreshold(blurred, 255, 
		cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 23, 2)
	_, thresh_nogrid = cv2.threshold(blurred, 0, 255, 
		cv2.THRESH_BINARY_INV|cv2.THRESH_OTSU)
	edged = cv2.Canny(thresh, 20, 3*20)
	outers = get_rects(edged, slice(0, 3))
#	mask = np.zeros(gray.shape, np.uint8)
#	result = cv2.bitwise_and(gray, mask)
#	cv2.drawContours(result, outers[:6], -1, (0, 255, 0))
	answers = []
	roi_n = 0
	curr_question = 1
	for c in deduplicate(outers):
		(x, y, w, h) = cv2.boundingRect(c)
		# extent = float(cv2.contourArea(c)) / (w*h)
		box = edged[y:y+h, x:x+w]
		inners = get_rects(box, method=cv2.RETR_TREE)
		for v in deduplicate(inners):
			(a, b, i, j) = cv2.boundingRect(v)
			aspect_ratio = float(i)/j # w/h
			if aspect_ratio != 1.0 and aspect_ratio > 3:
				inner_box = crop_black(
					crop(thresh_nogrid[y:y+h, x:x+w][b:b+j, a:a+i], 4, 4))
				opt_box = cut(inner_box, 5)
				marked = 0
				answer = -1
				for i in range(5):
					if marked > 1:
						answer = -1
						break
					cropped_opt = crop_black(opt_box[i])
					white = cv2.countNonZero(cropped_opt)
					black = cv2.countNonZero(cv2.bitwise_not(cropped_opt))
					if white/(white+black) > 0.7:
						answer = i
						marked += 1
						cv2.imwrite(f'out/test_{roi_n}_{i}.png', cropped_opt)
				answers.insert(curr_question, answer)
				roi_n += 1
				curr_question += 1
		# _, thresh = cv2.threshold(box, 0, 255, cv2.THRESH_BINARY|cv2.THRESH_OTSU)
		# mask = cv2.bitwise_not(thresh)
		# cv2.drawContours(result[y:y+h, x:x+w], inners, -1, (0, 255, 0))
	cv2.imwrite('out/test.png', edged)
	correct_answers = [0,1,2,3,4,4,3,2,1,0]
	print('Gabarito')
	print('\t'.join(
		f'{i}.{string.ascii_uppercase[a]}' for i, a in enumerate(correct_answers)))
	print('Suas respostas')
	print('\t'.join(
		'-' if a < 0 else string.ascii_uppercase[a] for a in answers))
	n_correct = sum(1 for a, b in zip(answers, correct_answers) if a == b)
	n_incorrect = len(correct_answers) - n_correct
	print(f'Acertos|Erros: {n_correct}|{n_incorrect}')
	print(f'Nota: {(n_correct/len(correct_answers)):.0%}')
	# count, correct = map(sum, zip(*((a > 3, a > 5) for a in answers)))
