from datetime import date
from jinja2 import Environment, PackageLoader
import qrcode
from qrcode import QRCode
from qrcode.constants import ERROR_CORRECT_L
from io import BytesIO
from base64 import b64encode, b64decode

# QR size: (4*5+17+2*2)*4
qr = QRCode(version=1, error_correction=ERROR_CORRECT_L, box_size=4, border=2)
qr.add_data('SAMPLE')
qr.make()
img = qr.make_image(fill_color='black', back_color='white')
qr.clear()
output = BytesIO()
img.save(output, format='PNG')
output.seek(0)

env = Environment(
	loader=PackageLoader('render'), trim_blocks=True, lstrip_blocks=True)

with open('./out/out.html', 'w', encoding='utf-8') as f:
	f.write(
		env.get_template('answer_sheet.html').render(
			name='John Doe', n_choices=5, n_questions=257, enrollment=789456, 
			date=date.today().strftime('%A, %d/%m/%Y'), 
			qr=b64encode(output.read()).decode()
		)
	)
