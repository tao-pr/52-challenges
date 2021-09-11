from collections import namedtuple
from functools import partial
from io import StringIO

import fitz
from lxml import etree

BLOCK_IMAGE = 1
BLOCK_TEXT = 0

Block = namedtuple("Block", ['tl','br','w','h','content', 'type', 'density'])
SBlock = namedtuple("SBlock", ['page','content','priority'])

def read_pdf2(path: str):
  """
  Read PDF pages with PyPDF2 lib
  """
  import PyPDF2

  file = PyPDF2.PdfFileReader(open(path, 'rb'))
  num_pages = file.getNumPages()
  pages = [file.getPage(n) for n in range(num_pages)]
  return pages

def read_pdf(path: str, verbose: bool=False):
  """
  Read PDF pages with PyMuPDF
  """
  if verbose:
    print(f'Reading : {path}')
  pdf = fitz.open(path)
  num_pages = pdf.page_count
  metadata = pdf.metadata
  pages = [pdf.load_page(n) for n in range(num_pages)]
  
  # Read as textblocks
  only_text = lambda b: b.type == BLOCK_TEXT
  ptextblocks = map(lambda x: \
    filter(only_text, map(parse_text_block, x.get_text_blocks())), 
    pages) # pages -> blocks

  # Create content tree
  ctree = gen_content_tree(ptextblocks)

  return ctree

def parse_text_block(bl):
  x0, y0, x1, y1, obj, bl_no, bl_type = bl
  w = x1-x0
  h = y1-y0
  # NOTE: dimension of textblock may not accurately infer how big or small
  # the whole text is. The whole block may be rotated and its bounding rect 
  # will get bigger than expected.

  if bl_type == BLOCK_TEXT:
    density = (w*h) / len(obj)
  else:
    density = None

  b = Block(tl=(x0,y0), br=(x1,y1), w=w, h=h, content=obj, type=bl_type, density=density)
  return b

def parse_html(ht):
  tree = etree.parse(StringIO(ht))
  return tree

def gen_content_tree(blocks):
  # Build chain of titles-paragraphs
  chain = []
  for p, page in enumerate(blocks):
    for block in page:
      is_title = False
      chain.push(SBlock(page=p, content=block.content, priority=is_title))
  return chain
