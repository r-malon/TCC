#!/usr/bin/env python3

from datetime import date
from jinja2 import Environment, PackageLoader
import qrcode
from qrcode import QRCode
from qrcode.constants import ERROR_CORRECT_L
from io import BytesIO
from base64 import b64encode, b64decode
import csv


def getQR(data):
	qr.add_data(data)
	qr.make()
	img = qr.make_image(fill_color='black', back_color='white')
	qr.clear()
	output = BytesIO()
	img.save(output, format='PNG')
	output.seek(0)
	return b64encode(output.read()).decode()

# size = (4*version + 17 + 2*border) * box_size
# id_list = ','.join([str(randint(0, 999999)).zfill(6) for _ in range(20)])
DOMAIN = 'my-domain-789123654.herokuapp.com'
N_CHOICES = 5
N_QUESTIONS = 259
qr = QRCode(version=4, error_correction=ERROR_CORRECT_L, box_size=4, border=2)

env = Environment(
	loader=PackageLoader('render'), trim_blocks=True, lstrip_blocks=True)

'''
# (n_questions - 21*3) // 24 + 3 + 1
with open('./static/n_columns.css', 'w', encoding='utf-8') as f:
	f.write(
		f':root {{ --n_columns: {1 if N <= 21 else 2 if N <= 42 else 3}; }}')
'''
with open('./static/students.csv', newline='') as f:
	reader = csv.DictReader(f)
	for row in reader:
		name = row['name']
		enrollment = row['enrollment']
		with open(f'./sheets/{enrollment}.html', 'w', encoding='utf-8') as g:
			g.write(
				env.get_template('answer_sheet.html').render(
					name=name, enrollment=enrollment, 
					n_choices=N_CHOICES, n_questions=N_QUESTIONS, 
					date=date.today().strftime('%A, %d/%m/%Y'), 
					qr=getQR(f'https://{DOMAIN}/user/{enrollment}/#{name};{enrollment}')
				)
			)
