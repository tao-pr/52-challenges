from collections import namedtuple
from functools import partial
from io import StringIO

import fitz
from lxml import etree

BLOCK_IMAGE = 1
BLOCK_TEXT = 0

Block = namedtuple("Block", ['tl','br','w','h','content', 'type'])

def read_pdf2(path: str):
  """
  Read PDF pages with PyPDF2 lib
  """
  import PyPDF2

  file = PyPDF2.PdfFileReader(open(path, 'rb'))
  num_pages = file.getNumPages()
  pages = [file.getPage(n) for n in range(num_pages)]
  return pages

def read_pdf(path: str):
  """
  Read PDF pages with PyMuPDF
  """
  pdf = fitz.open(path)
  num_pages = pdf.page_count
  metadata = pdf.metadata
  toc = pdf.get_toc()
  pages = [pdf.load_page(n) for n in range(num_pages)]
  
  # Read as textblocks
  ptextblocks = map(lambda x: \
    map(parse_text_block, x.get_text_blocks()), pages) # pages -> blocks

  # Read as HTML
  phtmls = map(lambda p: parse_html(p.get_textpage().extractHTML()), pages) # pages -> html


  """
  [...
    (28.346399307250977,
    72.4287109375,
    555.9425659179688,
    91.57421875,
    'Allgemeine Informationen zu Produktbezeichnungen gemäß § 15  Zahlungskontengesetz\nSoweit im Folgenden die Begrifflichkeiten „Commerzbank Girocard“, „Mastercard Debit“ oder „Virtual Debit Card“ genannt werden, entsprechen diese der standar disierten Zahlungskontenterminologie „Ausgabe einer Debitkarte“.\nSoweit im Folgenden die Begrifflichkeiten „PremiumKreditkarte“, „Young Visa Kreditkarte“, „ClassicKreditkarte“, „GoldKreditkarte“, „Prepaid Karte“ oder „Prepaid Karte Junior“ genannt werden, entsprechen diese der standardisierten Zahlungskontenterminologie „Ausgabe einer Kreditkarte“.\n',
    138,
    0)]
  """
  p = next(ptextblocks)

  import IPython
  IPython.embed()

def parse_text_block(bl):
  x0, y0, x1, y1, obj, bl_no, bl_type = bl
  w = x1-x0
  h = y1-y0
  # NOTE: dimension of textblock may not accurately infer how big or small
  # the whole text is. The whole block may be rotated and its bounding rect 
  # will get bigger than expected.
  b = Block(tl=(x0,y0), br=(x1,y1), w=w, h=h, content=obj, type=bl_type)
  return b

def parse_html(ht):
  tree = etree.parse(StringIO(ht))
  return tree
