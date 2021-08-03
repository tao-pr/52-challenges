def test_find_longest_sequence():
  """
  Given an array L,
  find the position p and length k which 
    - all elements to the left of p from p-k position are in ascending order
    - all elements to the right of p until p+k position are in descending order
    - and L[p] is the biggest among that sequence 
  """
  def find(L):
    ans = (0,0)
    for i,p in enumerate(L):
      ansp = expand(L, p, p, i, 1)
      # update answer if a longer sequence is found
      if ansp[1] > ans[1]: 
        ans = ansp
    return ans

  def expand(L, pleft, pright, i, k):
    if i-k>=0 and i+k<len(L) and L[i-k] < pleft and L[i+k] < pright:
      return expand(L, L[i-k], L[i+k], i, k+1)
    else:
      return (i,k-1) # Recede

  assert find([0,1,0]) == (1,1)
  assert find([4,3,2,5,6,3,2,1]) == (4,2)
  assert find([2,4,3,2,1,2,3,4,5]) == (1,1)