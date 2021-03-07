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


def test_sum_combination():
  # Find subarrays which sum up to make a number 
  # less than or equal the threshold
  def find_comb(arr, k):
    combs = expand_comb(arr, k)
    return combs

  def expand_comb(arr, k):
    comb = []
    for i, a in enumerate(arr):
      if a==k:
        # Found the last element of the combination
        comb.append([a])
        continue
      tail = arr[i+1:]
      # take one element from tail
      for j,b in enumerate(tail):
        if a+b <= k:
          cand = [a,b]
          comb.append([a,b])
          # recursion
          for c in find_comb(tail[j+1:], k-a-b):
            comb.append([a,b] + c)
    return comb

  assert find_comb([1,2,3,4], 5) == [[1,2],[1,3],[1,4],[2,3]]
  assert find_comb([1,2,3,1], 4) == [[1,2],[1,2,1],[1,3],[1,1],[2,1],[3,1]]


def test_lego_blocks():
  # Given a list of 3x3 lego blocks, find matches (may need to rotate)
  def find_matches(blocks):
    matches = []
    for i,b in enumerate(blocks):
      rotatedB = gen_rotates(b)
      assert(len(rotatedB)==4)
      for j, c in enumerate(blocks[i+1:]):
        rotatedC = gen_rotates(c)
        assert(len(rotatedC)==4)
        found_match = False
        for rb in rotatedB:
          for rc in rotatedC:
            if fit(rb, rc):
              matches.append([i, i+j+1])
              found_match = True
              break
          if found_match:
            break
    return matches

  def fit(a,b):
    for i in range(len(a)):
      for j in range(len(a)):
        if a[i][j] + b[i][j] != 1:
          return False
    return True

  def gen_rotates(b):
    # Rotate clockwise by 90*
    # (0,0) ---> (N,0) (1,0) (0,0)
    # (1,0)
    # (N,0)
    rot = [b]
    w = b[:]
    N = len(b)
    for n in range(3):
      ww = []
      for i in range(N):
        row = [w[N-1-j][i] for j in range(N)]
        ww.append(row)
      rot.append(ww)
      w = ww[:]
    return rot

  blocks1 = [
    [[1,1,0],[1,1,0],[1,1,0]],
    [[0,1,0],[0,1,0],[0,1,0]],
    [[1,1,1],[0,0,0],[1,1,1]],
    [[0,0,0],[0,1,0],[0,0,0]]
  ]
  assert find_matches(blocks1) == [[1,2]]

  blocks2 = [
    [[1,1,0],[1,1,0],[1,1,0]],
    [[0,1,0],[0,1,0],[0,1,0]],
    [[1,1,1],[0,0,0],[1,1,1]],
    [[0,0,0],[0,1,0],[0,0,0]],
    [[1,1,1],[0,0,0],[0,0,0]]
  ]
  assert find_matches(blocks2) == [[0,4],[1,2]]


def test_rotate_submatrix():
  # Given big matrix A: NxN
  # how many submatrices we can rotate to make them 
  # identical to the goal matrix?

  def count_rotate_submat(M, G):
    matsize = len(M)
    gsize = len(G)
    # Assume both square
    n = 0
    # gen rotates of G
    Grotates = gen_rotates(G)
    assert(len(Grotates)==4)
    # sliding window
    for i in range(matsize-gsize+1):
      for j in range(matsize-gsize+1):
        sub = [[M[i+b][j+a] for a in range(gsize)] for b in range(gsize)]
        # check equality
        for R in Grotates:
          if eq(sub, R):
            n += 1
            break
    return n

  def eq(A,B):
    for i in range(len(A)):
      for j in range(len(A)):
        if A[i][j] != B[i][j]:
          return False
    return True

  def gen_rotates(M):
    rot = [M]
    W = M[:]
    for i in range(0, 3):
      # Rotate W by 90* clockwise
      # 10  => 30 20 10
      # 20
      # 30 
      R = []
      for i in range(len(M)):
        row = [W[len(M)-1-j][i] for j in range(len(M))]
        R.append(row)
      rot.append(R)
      W = R[:]
    return rot

  # Test1
  A1 = [
    [1,1,1,1,1],
    [1,1,2,1,1],
    [1,1,1,1,1],
    [1,1,1,1,1],
    [1,1,1,1,1]
  ]
  G1 = [
    [0, 0],
    [0, 1]
  ]
  #assert(count_rotate_submat(A1, G1)) == 0

  # Test2
  A2 = [
    [1,1,0,1,1],
    [0,1,2,1,0],
    [0,0,0,0,0],
    [0,1,1,0,1],
    [1,1,1,1,1]
  ]
  G2 = [
    [0, 0],
    [0, 1]
  ]
  assert(count_rotate_submat(A2, G2)) == 5


def test_seating_arrangement():
  # REF: https://www.facebookrecruiting.com/portal/coding_practice_question/?problem_id=2444722699191194

  def minOverallAwkwardness(arr):
    # sorted: 1 2 3 4
    # take every other element 1 3
    # append with reverse of the remaining 1 3 + 4 2
    sarr = sorted(arr)
    minarr = []
    remain = []
    for i, a in enumerate(sarr):
      if i%2 == 0:
        minarr.append(a)
      else:
        remain = [a] + remain
    marr = minarr + remain + [minarr[0]]
    print(marr)
    awk = 0
    for a,b in zip(marr, marr[1:]):
      awk = max(awk, abs(a-b))
    return awk

  arr_1 = [5, 10, 6, 8]
  expected_1 = 4
  output_1 = minOverallAwkwardness(arr_1)
  assert expected_1 == output_1

  arr_2 = [1, 2, 5, 3, 7]
  expected_2 = 4
  output_2 = minOverallAwkwardness(arr_2)
  assert expected_2 == output_2


def test_quick_sort():
  def qsort(arr):
    return qsort_(arr, low=0, high=len(arr)-1)
  def qsort_(arr, low, high):
    if low < high:
      pindex = partition(arr, low, high)
      qsort_(arr, low, pindex-1) # left partition of pivot
      qsort_(arr, pindex+1, high) # right partition of pivot
    return arr

  def partition(arr, low, high):
    i = low-1
    pivot = arr[high]
    for n in range(low, high):
      if arr[n] <= pivot:
        i += 1
        arr[n], arr[i] = arr[i], arr[n] # swap element smaller than pivot

    arr[i+1], arr[high] = arr[high], arr[i+1]
    return i+1

  assert qsort([1,2,3]) == [1,2,3]
  assert qsort([4,3,1,5]) == [1,3,4,5]
  assert qsort([1,1,5,3]) == [1,1,3,5]