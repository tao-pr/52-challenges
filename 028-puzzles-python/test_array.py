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
        i += 1 # step element for swapping 
        arr[n], arr[i] = arr[i], arr[n] # swap element smaller than pivot

    # dont forget to swap the last with pivot itself
    arr[i+1], arr[high] = arr[high], arr[i+1]
    return i+1

  assert qsort([1,2,3]) == [1,2,3]
  assert qsort([4,3,1,5]) == [1,3,4,5]
  assert qsort([1,1,5,3]) == [1,1,3,5]


def test_minimum_bound_rect():
  """
  Find area of minimum rectable covering all "1" in the matrix
  """

  """
  0 0 0 0
  0 1 0 0 
  0 0 1 0
  0 1 1 1
  """
  def min_rect(mat):
    W, H = len(mat[0]), len(mat)

    minx, maxx = W-1, W-1
    miny, maxy = H-1, H-1

    # identify top-left
    for x in range(W):
      for y in range(miny+1):
        if mat[y][x]==1:
          miny = y if y<miny else miny
          minx = x if x<minx else minx
          if x==y==0:
            break

    # identify bottom-right
    for x in range(W-1, minx-1, -1):
      for y in range(H-1, miny-1, -1):
        if mat[y][x]==1:
          maxy = y if y>maxy else maxy
          maxx = x if x>maxx else maxx
          if x==W-1 and y==H-1:
            break
    
    print(f'TL = {minx}, {miny}')
    print(f'BR = {maxx}, {maxy}')

    area = (maxy-miny+1) * (maxx-minx+1)
    return area

  R1 = [[1,0],[0,1]]
  assert(min_rect(R1)) == 4
  R2 = [[0,0,0,0],[0,1,0,1],[0,0,1,0],[0,1,1,0]]
  assert(min_rect(R2)) == 9
  R3 = [[0,0,0,0],[0,0,1,0],[0,0,1,0],[0,1,0,1],[0,0,0,1]]
  assert(min_rect(R3)) == 12


def test_steepest():
  """
  Find the maximum steep of the terrain.
  Considering 8 directions around cell
  """
  def maxsteep(mat):
    from heapq import heappush, heappop

    # calculate cell gradient of the whole mat
    H, W = len(mat), len(mat[0])
    G = []
    for y in range(len(mat)):
      for x in range(len(mat[0])):
        # only calculate "*" neighbours, as x were already visited
        # x x *
        # x   *
        # * * *
        dd = [[-1,1],[0,1],[1,1],[1,0],[1,-1]] # y,x
        for dy,dx in dd:
          if 0<=x+dx<W and 0<=y+dy<H:
            diff = abs(mat[y][x] - mat[y+dy][x+dx])
            heappush(G, -diff)

    return -heappop(G)

  R1 = [[0,0,0],
        [0,1,0],
        [0,1,0]]
  assert maxsteep(R1) == 1

  R2 = [[0,0,0,0],
        [0,1,2,0],
        [0,1,1,0],
        [0,1,0,0]]
  assert maxsteep(R2) == 2

  R3 = [[0,1,1,1,0],
        [0,1,2,1,1],
        [0,1,3,2,1],
        [0,1,1,1,0]]
  assert maxsteep(R2) == 2


def test_find_min_rotate_sorted_array():
  # REF: https://leetcode.com/problems/find-minimum-in-rotated-sorted-array-ii/

  def min_rotate(arr):
    # find first element such that arr[n] > arr[n+1]
    arr.append(arr[0])
    for i in range(len(arr)-1):
      if arr[i]>arr[i+1]:
        return arr[i+1]

  assert min_rotate([1,3,5]) == 1
  assert min_rotate([2,2,2,0,1]) == 0
  assert min_rotate([1,3,3,4,5,6,0]) == 0
  assert min_rotate([1,3,3,4,5,6]) == 1


def test_mini_subarray_sum():
  # REF: https://leetcode.com/problems/minimum-size-subarray-sum/

  # Find the `minimum` length of subarray
  # of which sum is equal or greater than target

  # O(n log n) is preferred

  def subarray_sum(arr, target):
    N = len(arr)
    from heapq import heappush, heappop
    H = []
    # 0 1 2 3 
    for i in range(N):
      s = arr[i]
      if s>=target:
        return 1
      for n in range(1,N-i):
        s += arr[i+n]
        if s>=target:
          heappush(H, n+1)
          break
    return heappop(H) if len(H)>0 else 0

  assert subarray_sum([2,3,1,2,4,3], 7) == 2
  assert subarray_sum([1,4,4], 4) == 1
  assert subarray_sum([1,1,1,1,1,1,1,1], 11) == 0

def test_fold_spiral():
  """
  Given a 1-d array, fold it clockwise to make a 2d matrix
  """
  def fold(arr):
    import numpy as np
    W = np.sqrt(len(arr))
    if W!=np.round(W):
      return [] # invalid array size, can't fold CW
    W = int(W)
    M = [[None for _ in range(W)] for _ in range(W)]

    row,col = 0, 0
    for a in arr:
      M[row][col] = a
      # next cell
      # try R
      if col<W-1 and M[row][col+1] is None:
        col +=1
      # try D
      elif row<W-1 and M[row+1][col] is None:
        row +=1
      # try left
      elif col>0 and M[row][col-1] is None:
        col -= 1
      # try up
      elif row>0 and M[row-1][col] is None:
        row -= 1
      # nowhere to go
      else:
        return M
    return M

  assert fold([1,2,3,4]) == [[1,2],[4,3]]
  assert fold([]) == []
  assert fold([1]) == [[1]]
  assert fold([1,2,3,4,5,6,7,8,9]) == [[1,2,3],[8,9,4],[7,6,5]]


def test_count_swap():
  """
  Given two arrays, find minimum number of element swap to make them identical
  """
  def cswap(arr1, arr2):
    if len(arr1)==len(arr2)==0:
      return 0
    if eq(arr1, arr2):
      return 0
    M = []
    nswap = 0
    for i in range(len(arr1)):
      if arr1[i]==arr2[i]:
        continue
      # find an element to swap with
      for j in range(i+1, len(arr1)):
        if arr1[i]==arr2[j]:
          nswap += 1
          arr2[j] = arr2[i]
          break
    return nswap

  def eq(arr1, arr2):
    return all([a==b for a,b in zip(arr1,arr2)])

  assert cswap([],[]) == 0
  assert cswap([1],[1]) == 0
  assert cswap([1,2,3],[1,3,2]) == 1
  assert cswap([1,1,5,3],[1,5,3,1]) == 2
  assert cswap([1,6,7,3],[3,6,7,1]) == 1


def test_search_word():
  def search(M,w):
    V = set()
    # locate all the origins
    cands = []
    for i in range(len(M)):
      for j in range(len(M[0])):
        if M[i][j] == w[0]:
          if walk((i,j), M, V, w[1:]):
            return True
    return False

  def walk(pos, M, V, w):
    if len(w)==0:
      return True
    i, j = pos

    valid = lambda a,b: a>=0 and b>=0 and a<len(M) and b<len(M[0])
    # expand neighbours, DFS
    for di in [-1,0,1]:
      for dj in [-1,0,1]:
        if abs(di)!=abs(dj) and (i+di, j+dj) not in V and valid(i+di, j+dj):
          if M[i+di][j+dj] == w[0]:
            V_ = V.copy()
            V_.add((i+di, j+dj)) # prevent from repeating the cells
            if walk((i+di, j+dj), M, V_, w[1:]):
              return True
    return False

  M1 = [['A','A','C','A'],
        ['A','C','C','D'],
        ['D','A','B','C']]
  assert search(M1, 'CAAD') == False
  assert search(M1, 'BCDA') == True
  assert search(M1, 'BFBA') == False
  assert search(M1, 'ACCB') == True
  assert search(M1, 'ADDC') == False
  assert search(M1, 'AADABC') == True


def test_largest_rect_histogram():
  # REF: https://leetcode.com/problems/largest-rectangle-in-histogram/
  def lg(H):
    # complexity : O(N^2)
    largest = 0
    for i in range(len(H)):
      area = expand(H,i)
      largest = max(largest, area)
    return largest

  def expand(H,i):
    w = 1
    # expand to left
    j = i-1
    while j>=0 and H[j]>=H[i]:
      j-=1
      w += 1
    # expand to right
    j = i+1
    while j<len(H) and H[j]>=H[i]:
      j+=1
      w += 1
    return w*H[i]

  assert lg([2,1,5,6,2,3]) == 10
  assert lg([2,4]) == 4


def test_interval_arrays():
  """
  Given a list of intervals, find total amount of overlapping time.
  Union all overlapping
  """
  def overlap(intervals):
    uni = []
    # O(N^2)
    for i,t1 in enumerate(intervals):
      for t2 in intervals[i+1:]:
        sec = intersect(t1,t2)
        if len(sec)>0:
          uni = union(uni, sec)
    if len(uni)==0:
      return 0
    a,b = uni
    return b-a

  def intersect(t1,t2):
    a1,b1 = t1
    a2,b2 = t2
    l = max(a1,a2)
    u = min(b1,b2)
    if l>=u: # no intersection
      return []
    else:
      return [l,u]

  def union(t1,t2):
    if len(t1)==0:
      return t2
    a1,b1 = t1
    a2,b2 = t2
    return [min(a1,b1), max(b1,b2)]

  assert intersect([0,10],[10,15]) == []
  assert intersect([0,10],[5,10]) == [5,10]
  assert intersect([0,10],[5,7]) == [5,7]
  assert intersect([5,10],[7,15]) == [7,10]
  assert intersect([5,10],[1,2]) == []
  assert intersect([5,10],[1,6]) == [5,6]

  assert overlap([[1,15],[15,60],[25,60],[45,75]]) == 35
  assert overlap([[0,30],[45,50],[35,40]]) == 0
  assert overlap([[30,100],[10,20],[20,40],[10,50]]) == 20


def test_search_2dmat():
  # REF: https://leetcode.com/problems/search-a-2d-matrix/
  # Each row is sorted from left -> right
  # Each col is sorted from top -> bottom

  def search(M, v):
    from functools import reduce
    # start from mid point
    y = (len(M)-1)//2
    x = (len(M[0])-1)//2

    if v < M[0][0] or v > M[len(M)-1][len(M[0])-1]:
      return False # OOB

    # Flatten the matrix into 1-d list (Binary tree)
    B = list(reduce(lambda x,y: x+y, M))

    # 0 1 [2] 3 4
    return bsearch(B, v)

  def bsearch(B, v):
    if len(B)==0:
      return False
    i = len(B)//2
    if B[i]==v:
      return True
    if B[i]<v:
      return bsearch(B[i+1:], v)
    else:
      return bsearch(B[:i], v)

  M1 = [
    [1,5],
    [6,9]
  ]
  assert search(M1, 4) == False
  M2 = [
    [1,1,4,5],
    [6,8,9,10],
    [12,17,30,35],
    [36,40,41,50]
  ]
  assert search(M2, 8) == True
  assert search(M2, 50) == True
  assert search(M2, 18) == False
  assert search(M2, 21) == False
