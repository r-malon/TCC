from datetime import date
from jinja2 import Environment, PackageLoader
import qrcode
from qrcode import QRCode
from qrcode.constants import ERROR_CORRECT_L
from io import BytesIO
from base64 import b64encode, b64decode

# size = (4*version + 17 + 2*border) * box_size
qr = QRCode(version=4, error_correction=ERROR_CORRECT_L, box_size=4, border=2)
DOMAIN = 'my-domain-789123654.herokuapp.com'
qr.add_data(f'http://{DOMAIN}/user/123456/#JohnDoe;123456')
qr.make()
img = qr.make_image(fill_color='black', back_color='white')
qr.clear()
output = BytesIO()
img.save(output, format='PNG')
output.seek(0)

env = Environment(
	loader=PackageLoader('render'), trim_blocks=True, lstrip_blocks=True)

N=46
'''
# (n_questions - 21*3) // 24 + 3 + 1
with open('./static/n_columns.css', 'w', encoding='utf-8') as f:
	f.write(
		f':root {{ --n_columns: {1 if N <= 21 else 2 if N <= 42 else 3}; }}')
'''
with open('./out/out.html', 'w', encoding='utf-8') as f:
	f.write(
		env.get_template('answer_sheet.html').render(
			name='John Doe', n_choices=5, n_questions=N, enrollment=789456, 
			date=date.today().strftime('%A, %d/%m/%Y'), 
			qr=b64encode(output.read()).decode()
		)
	)
