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


def test_first_missing_positives():
  # REF: https://leetcode.com/problems/first-missing-positive/

  def add_sorted(v, ws):
    if len(ws)==0:
      return [v]
    elif v<=ws[0]:
      return [v]+ws
    else:
      return [ws[0]]+add_sorted(v,ws[1:])

  def find_it(ns):
    sorted_ns = []
    for n in ns:
      if n>0:
        sorted_ns = add_sorted(n, sorted_ns)

    expect = 1
    for n in sorted_ns:
      if n!=expect:
        return expect
      else:
        expect += 1
    return n+1
  
  assert find_it([1,2,0]) == 3
  assert find_it([3,4,-1,1]) == 2
  assert find_it([7,8,9,11,12]) == 1


def test_nested_flatten():

  def flatten(vs):
    ws = []
    for v in vs:
      if type(v) is list:
        ws = ws + flatten(v)
      else:
        ws.append(v)
    return ws

  assert flatten([1,2,3]) == [1,2,3]
  assert flatten([[1,2,[3]],[4]]) == [1,2,3,4]
  assert flatten([[],[1,[2,3,[4]]],5]) == [1,2,3,4,5]


def test_spiral_matrix():
  # REF: https://leetcode.com/problems/spiral-matrix/

  def spiral_walk(mat):
    # Create walk steps
    steps = create_walk_steps(len(mat), len(mat[0]))
    return [mat[row][col] for (row,col) in steps]

  def create_walk_steps(rows, cols):
    steps = []
    row = 0
    col = -1
    row0, col0 = 0, 0
    rowM, colM = rows-1, cols-1
    dd = [[0,1],[1,0],[0,-1],[-1,0]] # row, col
    while len(steps)<rows*cols:
      d = dd[0]

      row_ = row + d[0]
      col_ = col + d[1]

      # walk until hit boundary
      while row_ >= row0 and row_ <= rowM and col_ >= col0 and col_ <= colM:
        steps.append((row_, col_))
        row = row_
        col = col_
        row_ = row + d[0]
        col_ = col + d[1]

      # change direction
      dd = dd[1:] + dd[:1]

      # truncate boundary
      if d==[0,1]:
        row0 += 1
      if d==[1,0]:
        colM -= 1
      if d==[0,-1]:
        rowM -= 1
      if d==[-1,0]:
        col0 += 1
    return steps


  assert spiral_walk([[1,2,3,4],[5,6,7,8],[9,10,11,12]]) == [1,2,3,4,8,12,11,10,9,5,6,7]
  assert spiral_walk( [[1,2,3],[4,5,6],[7,8,9]]) == [1,2,3,6,9,8,7,4,5]


def test_reverse_make_equal():
  # REF: https://www.facebookrecruiting.com/portal/coding_practice_question/?problem_id=2869293499822992
  def are_they_equal(array_a, array_b):
    # Find the first & last position that they're not equal
    min_index = -1
    max_index = -1
    first_missing = None
    for a,b,i in zip(array_a, array_b, range(len(array_a))):
      if a != b:
        if min_index < 0:
          min_index = i
          first_missing = a

      if min_index>0 and b == first_missing:
        max_index = i
        break
    
    if max_index < 0:
      max_index = len(array_a)

    if min_index > 0:
      # try swapping subarray 
      array_b[min_index:max_index+1] = array_b[min_index:max_index+1][::-1]
      if array_a == array_b:
        return True
    return False

  assert are_they_equal([1, 2, 3, 4], [1, 4, 3, 2]) == True


def test_minimum_path_sum_triangle_array():
  # REF: https://leetcode.com/problems/triangle/

  # Input: triangle = [[2],[3,4],[6,5,7],[4,1,8,3]]
  #    2
  #   3 4
  #  6 5 7
  # 4 1 8 3
  # The minimum path sum from top to bottom is 2 + 3 + 5 + 1 = 11 


  def min_path_sum(tri):
    path_sum = 0
    for line in tri:
      path_sum += min(line)
    return path_sum

  assert min_path_sum([[2],[3,4],[6,5,7],[4,1,8,3]]) == 11
  assert min_path_sum([[-10]]) == -10


def test_num_pair_sum():
  # REF: https://www.facebookrecruiting.com/portal/coding_practice_question/?problem_id=840934449713537

  def numberOfWays(arr, k):
    # Write your code here
    return len(pair(arr, k))
  
  def pair(arr, k):
    pp = []
    for i,a in enumerate(arr):
      tail = arr[i+1:]
      for j, b in enumerate(tail):
        if a+b==k:
          pp.append([a,b])
    return pp

  assert pair([1,2,3,4], 5) == [[1,4],[2,3]]
  assert numberOfWays([1,2,3,4], 5) == 2


def test_combination():

  def gen_comb(arr, k):
    # Generate combination of [k] length
    return comb(arr, k, [])

  def comb(arr, k, prefix):
    if len(prefix)==k:
      return [prefix]

    out = []
    for i,a in enumerate(arr):
      cand = prefix + [a]
      tail = arr[i+1:]
      for c in comb(tail, k, cand):
        out.append(c)
    return out


  assert gen_comb([1,2,3], 2) == [[1,2],[1,3],[2,3]]
  assert gen_comb([1,2,3,4], 3) == [[1,2,3],[1,2,4],[1,3,4],[2,3,4]]