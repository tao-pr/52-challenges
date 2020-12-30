module SemiGr.Semi (
  LinkedList(..), fromList, toList) 
where

data LinkedList a = Empt | LinkedList a (LinkedList a)

instance (Show a) => Show (LinkedList a) where
  show (Empt) = ""
  show (LinkedList k Empt) = (show k)
  show (LinkedList k next) = (show k) <> " -> " <> (show next)

instance (Eq a) => Eq (LinkedList a) where
  (==) Empt Empt = True
  (==) Empt _ = False
  (==) _ Empt = False
  (==) (LinkedList a as) (LinkedList b bs) = (a==b) && (as == bs)

-- Create a LinkedList from list
fromList :: [a] -> LinkedList a
fromList [] = Empt
fromList (n:ns) = LinkedList n (fromList ns)

-- Create a list from LinkedList
toList :: LinkedList a -> [a]
toList Empt = []
toList (LinkedList a as) = a : toList as

instance Semigroup (LinkedList a) where
  (<>) Empt Empt = Empt
  (<>) t Empt = t
  (<>) Empt t = t
  (<>) (LinkedList a as) (LinkedList b bs) = 
    LinkedList a (LinkedList b (as <> bs))