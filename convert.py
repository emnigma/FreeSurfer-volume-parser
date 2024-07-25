import sys

from pyhtml2pdf import converter

converter.convert("http://localhost:1234/", f"{sys.argv[1]}")
