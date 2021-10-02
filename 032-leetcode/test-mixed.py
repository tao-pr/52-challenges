def test_group_division():
  """
  Find out if we can divide a group into bipartite?
  """
  def bipart(G):
    # create adjacency list
    M = {}
    for a,b in G:
      if a not in M:
        M[a] = [b]
      else:
        M[a].append(b)

      if b not in M:
        M[b] = [a]
      else:
        M[b].append(a)

    visited = set()
    colourset = [set(), set()]

    # assign first node as red (group 0)
    n = G[0][0]
    colourset[0].add(n)
    return colour(M, visited, colourset, n, 1)

  def colour(M, visited, colourset, n, nextcolour):
    # DFS
    visited.add(n)
    for m in M[n]:
      if m in visited:
        # colour of m shouldn't conflict
        if m not in colourset[nextcolour]:
          return False
      else:
        colourset[nextcolour].add(m)
        # DFS
        if not colour(M, visited, colourset, m, abs(1-nextcolour)):
          return False
    return True

  G = [
    (1,2),
    (2,3),
    (1,3)
  ]
  assert bipart(G) == False

  G = [
    (1,3),
    (2,3),
    (2,4),
  ]
  assert bipart(G) == True


def test_count_unique_permutation():
  """
  Given a string of length at least 3,
  find the number of possible permutations where each is unique
  """
  def cpermu(w):
    P = set()
    return len(permu(P, '', w))

  def permu(P, pre, w):
    for i in range(len(w)):
      a = w[i]
      bb = w[:i] + w[i+1:]
      if len(bb)==0:
        P.add(pre + a)
      else:
        permu(P, pre+a, bb)

    return P

  assert cpermu('aaa') == 1
  assert cpermu('aba') == 3 # aba, aab,baa
  assert cpermu('aaaa') == 1
  assert cpermu('abca') == 12
  assert cpermu('kkka') == 4


def test_count_number_of_missings():
  """
  Given an array of positive integers,
  Figure out how many integers are missing if it is supposed 
  to begin with 1
  """
  def count_miss(M):
    prev = 0
    c = 0
    for m in M:
      if m > prev + 1:
        c += m - prev - 1
      prev = m
    return c

  assert count_miss([2,3,4]) == 1
  assert count_miss([1,2]) == 0
  assert count_miss([1,15,17]) == 14
  assert count_miss([7,8,10,12,15,16]) == 10


def test_roll_array_as_matrix():
  """
  Given an array of N elements,
  roll it CCW so it becomes a square matrix
  (go up first)
  """
  def roll(N):
    from math import sqrt
    w = int(sqrt(len(N)))
    M = [[None for _ in range(w)] for _ in range(w)]

    k = w if w%2==0 else w-1
    r,c = int(k/2), int(k/2)
    D = [(-1,0),(0,-1),(1,0),(0,1)] # go up first, followed by left, ..
    M[r][c] = N[0]
    N = N[1:]

    # Walk patterns:
    # U - L - D - D - R - R - U - U - U - L - L - L - D - D - D - D
    # meaning every time we go "D", we repeat 1 more
    max_momentum = 1
    momentum = 0

    while len(N)>0:
      # step next
      if momentum >= max_momentum:
        momentum = 0
        D = D[1:] + [D[0]]
        if D[0] == (1,0):
          max_momentum += 1 # longer momentum everytime we go down
      dr, dc = D[0]
      r, c = r+dr, c+dc
      M[r][c] = N[0]
      N = N[1:]
      momentum += 1
    
    return M


  assert roll([1,2,3,4]) == [
    [3,2],
    [4,1]
  ]
  assert roll([1]) == [[1]]
  assert roll([5,4,1,2,0,1,3,1,3]) == [
    [1,4,3],
    [2,5,1],
    [0,1,3]
  ]


def test_
