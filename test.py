from weasyprint import HTML
HTML(string='<h1>Test PDF</h1>').write_pdf('test.pdf')
