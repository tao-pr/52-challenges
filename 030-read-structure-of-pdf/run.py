import os
import IPython
import glob

from pdf.lib import read_pdf, save_to

if __name__=="__main__":
  # Read PDF and convert to tabular data
  output = 'out'
  ls = glob.glob(os.path.expanduser('~/data/sustain/') + r'*.pdf')
  for i,f in enumerate(ls):
    print(f'({i}) processing : {f}')
    ctree = read_pdf(f)
    if ctree is not None and len(ctree)>0:
      save_to(ctree, output + '/' + ctree[0].filename.split('.')[0] + '.csv')
    #break