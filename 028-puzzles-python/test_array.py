# Array puzzles

def test_remove_duplicates_sorted():
  ns = [1,2,2,3,1,1,2,3,4,1,2,4,5]

  def remove_dup(vs):
    out = []
    def add_to(v, ws):
      if len(ws)==0:
        return [v]
      elif v<ws[0]:
        return [v]+ws
      elif v>ws[0]:
        return [ws[0]] + add_to(v,ws[1:])
      else:
        return ws

    for v in vs:
      out = add_to(v,out)
    return out

  assert remove_dup(ns) == [1,2,3,4,5]



def test_median_one_pass():
  ns = [4,3,1,5,3,1,2,5,3,1,5]

  def median(vs):
    def add_sorted(v, ws):
      if len(ws)==0:
        return [v]
      elif v<=ws[0]:
        return [v]+ws
      else:
        return [ws[0]]+add_sorted(v,ws[1:])

    sorted_vs = []
    i = 0
    m = 0
    for v in vs:
      sorted_vs = add_sorted(v, sorted_vs)
      # median index steps next every even index
      if i>0 and i%2==0:
        m += 1
      i += 1
    return sorted_vs[m]

  assert median(ns) == 3


def test_trap_rain_water():
  # REF: https://leetcode.com/problems/trapping-rain-water/
    
  def eval(blocks):
    sum_vol = 0
    h = 0
    i = 0
    for b in blocks:
      if b>h:
        # Perhaps begin of left bound
        h = b
      elif b<h:
        # Concave!
        vol, next_blocks = project_to_right(h, blocks[i:])
        if vol>0:
          # concave has right boundary
          # Break and start a new scan from next right bound
          sum_vol += vol
          sum_vol += eval(next_blocks)
          return sum_vol
        else:
          # concave has no right boundary, startover
          h = b
      i += 1
    return sum_vol

  def project_to_right(h, blocks):
    vol = 0
    has_end = False
    i = 0
    next_blocks = blocks[:]
    for b in blocks:
      if b>=h:
        # Find right boundary
        return vol, next_blocks
      else:
        vol += h-b
      next_blocks = next_blocks[1:]
    return 0, [] # No right boundary


  assert eval([0,1,0,2,1,0,1,3,2,1,2,1]) == 6
  assert eval([4,2,0,3,2,5]) == 9