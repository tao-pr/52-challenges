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

