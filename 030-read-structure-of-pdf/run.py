import os
import IPython
import glob

from pdf.lib import read_pdf, save_to

if __name__=="__main__":
  # Read PDF and convert to tabular data
  output = 'data'
  ls = glob.glob(os.path.expanduser('~/data/sustain/') + r'*.pdf')
  for i,f in enumerate(ls):
    ctree = read_pdf(f)
    save_to(ctree, output + str(i) + '.csv')
    break