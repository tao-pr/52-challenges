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

    print(P) # TAODEBUG
    return P

  assert cpermu('aaa') == 1
  assert cpermu('aba') == 3 # aba, aab,baa
  assert cpermu('aaaa') == 1
  assert cpermu('abca') == 12
  assert cpermu('kkka') == 4