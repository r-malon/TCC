from datetime import date
from jinja2 import Environment, PackageLoader
import pdfkit
import qrcode
from qrcode import QRCode
from qrcode.constants import ERROR_CORRECT_L
from io import BytesIO
from base64 import b64encode, b64decode

CHOICES = ['Ⓐ', 'Ⓑ', 'Ⓒ', 'Ⓓ', 'Ⓔ', 'Ⓕ', 'Ⓖ', 'Ⓗ', 'Ⓘ', 'Ⓙ', 'Ⓚ', 'Ⓛ', 'Ⓜ', 
	'Ⓝ', 'Ⓞ', 'Ⓟ', 'Ⓠ', 'Ⓡ', 'Ⓢ', 'Ⓣ', 'Ⓤ', 'Ⓥ', 'Ⓦ', 'Ⓧ', 'Ⓨ', 'Ⓩ']
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
		env.get_template('sheet.html').render(
			name='John Doe', n_choices=5, n_questions=30, enrollment=789456, 
			date=date.today().strftime('%A, %d/%m/%Y'), 
			qr=b64encode(output.read()).decode(), 
			choices=CHOICES
		)
	)

pdfkit.from_file('./out/out.html', './out/out.pdf', 
	verbose=True, options={
		'no-outline': None, 
		'encoding': 'UTF-8', 
		'enable-local-file-access': None
	}
)
