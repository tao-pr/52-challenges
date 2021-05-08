def test_gcd():
  """
  Given a list of numbers,
  find GCD
  """
  def gcd(ns):
    if len(ns)==2:
      return gcd2(ns[0], ns[1])
    else:
      a,b = ns[:2]
      return gcd([gcd2(a,b)] + ns[2:])

  def gcd2(a,b):
    # Euclidean algorithm
    if a==b:
      return a
    elif a<b:
      a,b = b,a

    while b != 0:
      a,b = b,a % b

    return a

  assert gcd([1,3]) == 1
  assert gcd([3,9]) == 3
  assert gcd([3,4,7]) == 1
  assert gcd([7,21,14]) == 7
  assert gcd([6,18,42]) == 6


def test_factorise():
  """
  Factorise a number
  """
  from functools import lru_cache # assume python 3.7 or older

  @lru_cache
  def fact(n):
    F = set()
    if n<=3:
      return [n]

    k = n
    while len(F)==0: # Runtime : O(N!)
      k -= 1
      if k==1:
        return [n] # n is a prime
      if n%k==0: # n = m*k
        m = n//k
        # Remove any elements from F which m or k can divide
        fm = set(fact(m))
        fk = set(fact(k))
        F = F.union(fm)
        F = F.union(fk)
        return sorted(list(F))

    return [n]

  assert fact(2) == [2]
  assert fact(7) == [7]
  assert fact(18) == [2,3]
  assert fact(175) == [5,7]
