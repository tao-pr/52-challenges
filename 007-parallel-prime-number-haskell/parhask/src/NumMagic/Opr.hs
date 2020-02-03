module NumMagic.Opr where

import Data.Set

-- Find all multiples of the specified integers
-- multiplesOf :: Int -> Int -> [Int] -> [Int]
-- multiplesOf n lim primes = uniq $ do 
--   m <- [n * p | p <- primes, n*p <= lim] -- first-degree expansion
--   q <- m:(multiplesOf m lim primes)    -- second-degree expansion
--   return q


multiplesOf :: Int -> Int -> [Int]
multiplesOf a lim = [a*i | i <- [2..], a*i <= lim]


-- Sort and uniqify the list of Integer
uniq :: [Int] -> [Int]
uniq ns = uniq' [] ns where
  uniq' qs [] = qs
  uniq' qs (m:ms) = uniq' (addOrder m qs) ms


-- Exclude all members from list [A] in [B]
exclude :: [Int] -> [Int] -> [Int]
exclude ns [] = ns
exclude (n:ns) ms = if n `elem` ms 
  then exclude ns ms
  else n:(exclude ns ms)


-- Add a number to an ordered list
addOrder :: Int -> [Int] -> [Int]
addOrder n [] = [n]
addOrder n (m:ms) =
  if n<m then n:m:ms
    else if n==m then m:ms
      else m:(addOrder n ms)
 

findPrimes :: Int -> [Int]
findPrimes 1 = []
findPrimes 2 = [2]
findPrimes n = 
  -- TAOTODO recursive call, see hints on the bottom of page
  withoutMultiplesOf (2) [2..n]


withoutMultiplesOf :: Int -> [Int] -> [Int]
withoutMultiplesOf _ [] = []
withoutMultiplesOf n ns = ns `exclude` (multiplesOf n (last ns))

[2,3,4,5,6,7]
 
 2 -> [4]      -> [2,3,_,5,6,7,9]
 3 -> [6,9]    -> [2,3,_,5,_,7,_]
 5 -> []       -> [2,3,_,5,_,7,_]
 ..



