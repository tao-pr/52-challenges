import os
import IPython
from pdf.lib import read_pdf

if __name__=="__main__":
  pages = read_pdf(os.path.expanduser('~/Downloads/preisaushang.pdf'))
  IPython.embed()