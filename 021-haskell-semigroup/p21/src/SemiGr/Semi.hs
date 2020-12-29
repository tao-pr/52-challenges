module SemiGr.Semi where

data LinkedList a = Empt | LinkedList a (LinkedList a)

instance (Show a) => Show (LinkedList a) where
  show (Empt) = ""
  show (LinkedList k Empt) = (show k)
  show (LinkedList k next) = (show k) <> " -> " <> (show next)

-- instance Semigroup (LinkedList a) where
--   <> = 