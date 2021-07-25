import PyPDF2

def read_pdf(path: str):
  file = PyPDF2.PdfFileReader(open(path, 'rb'))
  num_pages = file.getNumPages()
  pages = [file.getPage(n) for n in range(num_pages)]
  return pages