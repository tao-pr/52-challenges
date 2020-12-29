module SemiGr.Semi where

data LinkedList a = Empt | LinkedList a (LinkedList a)

instance (Show a) => Show (LinkedList a) where
  show (Empt) = ""
  show (LinkedList k Empt) = (show k)
  show (LinkedList k next) = (show k) <> " -> " <> (show next)

-- Create a LinkedList from list
fromList :: [a] -> LinkedList a
fromList [] = Empt
fromList (n:ns) = LinkedList n (fromList ns)

-- instance Semigroup (LinkedList a) where
--   <> = 