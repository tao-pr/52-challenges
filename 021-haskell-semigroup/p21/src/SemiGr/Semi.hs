module SemiGr.Semi (LinkedList(..), fromList) where

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

-- instance Semigroup (LinkedList a) where
--   <> = 