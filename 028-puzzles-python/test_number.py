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