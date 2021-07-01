import pdfkit

config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
pdfkit.from_url('https://getbootstrap.com/docs/4.5/layout/overview/', 'output.pdf', configuration=config)