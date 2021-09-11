import os
import IPython
import glob

from pdf.lib import read_pdf

if __name__=="__main__":
  ls = glob.glob(os.path.expanduser('~/data/sustain/') + r'*.pdf')
  for f in ls:
    ctree = read_pdf(f)
    IPython.embed()
    break