class Node:
  def __init__(self, x):
    self.data = x
    self.next = None

  def print(self):
    nextprint = "" if self.next is None else ":" + self.next.print()
    return str(self.data) + nextprint

  def pop_last(self):
    prev = None
    last = self
    while last.next is not None:
      prev = last
      last = last.next
    if prev is not None:
      prev.next = None
    return last

  def join(self, next):
    if self.next is None:
      self.next = next 
    else:
      self.next.join(next)

def create(ls):
  root = Node(ls[0])
  cur = root
  for a in ls[1:]:
    cur.next = Node(a)
    cur = cur.next
  return root


def test_reorder_alternate():
  # REF: https://leetcode.com/problems/reorder-list/

  # Given list: a0:a1:a2:...:aN-1
  # Reoder to : a0:aN-1:a1:aN-2..

  def reorder(ls):
    cursor = ls
    swap_from_last(cursor)
    return ls

  def swap_from_last(cursor):
    nextelem = cursor.next
    if nextelem is None:
      return
    if nextelem.next is None:
      return

    last = cursor.pop_last()
    cursor.next = last
    last.next = nextelem

    swap_from_last(nextelem)


  # Test1
  list1 = Node(1)
  list1.next = Node(2)
  list1.next.next = Node(3)
  list1.next.next.next = Node(4)
  assert list1.print() =="1:2:3:4"
  assert reorder(list1).print() == "1:4:2:3"

  list1 = Node(1)
  list1.next = Node(2)
  list1.next.next = Node(3)
  list1.next.next.next = Node(4)
  list1.next.next.next.next = Node(5)
  assert list1.print() =="1:2:3:4:5"
  assert reorder(list1).print() == "1:5:2:4:3"


def test_reverse_and_filter():
  # Reverse a list and drop anything greater than cutoff
  def rev_filter(ls, cutoff):
    # prev -> [a] -> next
    prev = None
    a = ls
    while a is not None:
      next = a.next
      # drop [a] if greater than cutoff
      if a.data <= cutoff:
        a.next = prev
        prev = a
        a = next
      else:
        a = next
    return prev

  # Test1
  list1 = Node(1)
  list1.next = Node(5)
  list1.next.next = Node(3)
  list1.next.next.next = Node(4)
  assert list1.print() =="1:5:3:4"
  assert rev_filter(list1, 4).print() == "4:3:1"
  assert rev_filter(list1, 2).print() == "1"


def test_rotate_list():
  # REF: https://leetcode.com/problems/rotate-list/

  def rotate(ls, k):
    n = 1
    # make list cyclic
    last = ls
    while last.next is not None:
      last = last.next
      n += 1
    last.next = ls

    # rotate head position
    k = k % n
    head = ls
    while k>0:
      head = head.next
      last = last.next
      k -= 1
    # cut head & last off so it's linear once again
    last.next = None
    return head

  # Test1
  list1 = create([1,2,3,4,5])
  assert list1.print() == "1:2:3:4:5"
  assert rotate(list1, 3).print() == "4:5:1:2:3"
  
  list2 = create([1,2,3,4,5,6,7])
  assert list2.print() == "1:2:3:4:5:6:7"
  assert rotate(list2, 9).print() == "3:4:5:6:7:1:2"


def test_odd_even_list():

  def add(ls, n):
    if ls is None:
      return n
    elif ls.next is None:
      ls.next = n
      return ls
    else:
      ls.next = add(ls.next, n)
      return ls

  def oddeven(ls):
    odd = None
    even = None
    cur = ls
    while cur is not None:
      next = cur.next
      if cur.data % 2 == 0:
        # even
        cur.next = None
        even = add(even, cur)
      else:
        # odd
        cur.next = None
        odd = add(odd, cur)
      cur = next
    odd.join(even)
    return odd

  # Test1
  list1 = create([1,2,3,4,5])
  assert list1.print() == "1:2:3:4:5"
  assert oddeven(list1).print() == "1:3:5:2:4"
  
  list2 = create([1,2,3,4,5,6,7])
  assert list2.print() == "1:2:3:4:5:6:7"
  assert oddeven(list2).print() == "1:3:5:7:2:4:6"


def test_reverse_sub_linked_list_to_make_sorted():
  def reverse_sort(ls):
    # locate the first element to start a reverse
    prevOfPrev = None
    prev = None
    n = ls
    while n is not None:
      if prev is not None:
        # Only check if n is not the first
        if n.data < prev.data:
          # So first element to swap is [prev]
          ls = swapsub(ls, prev, prevOfPrev)
      prevOfPrev = prev
      prev = n
      n = n.next 
    return ls

  def swapsub(ls, cur, head):
    # Swap from cur --> until the end, and reconnect to head
    # head :: cur :: cur+1 :: ... :: last :: None
    # -> becomes
    # head :: last :: .. :: cur+1 :: cur :: None
    prev = None
    while cur is not None:
      curnext = cur.next
      # swap links
      cur.next = prev

      # iterate next
      prev = cur
      cur = curnext

    if head is not None:
      head.next = prev
      return ls # no change to the head of list
    else:
      # Reversing the whole list, the new head will take place
      return prev

  assert reverse_sort(create([1,2,3,4])).print() == "1:2:3:4"
  assert reverse_sort(create([1,4,3,2])).print() == "1:2:3:4"
  assert reverse_sort(create([1,2,4,3])).print() == "1:2:3:4"
  assert reverse_sort(create([4,3,2,1])).print() == "1:2:3:4"


def test_sublist_reverse():
  """
  Given a linked list L, find beginning and ending position 
  to reverse the sub list which makes whole list sorted
  """
  def subreverse(ls):
    # inspect the first element to start swapping
    i, j = None, None
    n = 0
    ps = ls
    prev = None
    firstswap = None
    while ps is not None:
      # [1, a, ..... b, 7, 8] => [1, b, ..... a, 7, 8]

      # identify beginning of swap
      if prev is not None:
        if i is None and ps.data < prev:
          i = n-1
          firstswap = ps.data
          j = i-1
        # stop as soon as we find the end
        if j is not None and prev < ps.data:
          j += 1
          return (i, j)
      n += 1
      j = j+1 if j is not None else None
      prev = ps.data
      ps = ps.next
    j += 1
    return (i,j)

  assert subreverse(create([1,4,3,2,5])) == (1,3)
  assert subreverse(create([2,4,5,7,6])) == (3,4)
  assert subreverse(create([3,2,1])) == (0,2)