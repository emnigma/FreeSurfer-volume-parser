# import pdfkit
# pdfkit.from_url('http://localhost:1234/', 'out.pdf')


from pyhtml2pdf import converter

converter.convert("http://localhost:1234/", "out.pdf")
