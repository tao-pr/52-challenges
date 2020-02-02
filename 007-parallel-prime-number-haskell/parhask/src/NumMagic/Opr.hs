module NumMagic.Opr where

import Data.Set

-- Find all multiples of the specified integers
multiplesOf :: Int -> Int -> [Int] -> [Int]
multiplesOf n lim primes = uniq $ do 
  m <- [n * p | p <- primes, n*p <= lim] -- first-degree expansion
  q <- m:(multiplesOf m lim primes)    -- second-degree expansion
  return q


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


-- Find all prime number up until the specified bound
findPrimes :: Int -> [Int]
findPrimes 0 = primes
findPrimes 1 = primes
findPrimes lim = do
  n <- [2..lim]
  m <- multiplesOf n lim primes -- TAOTODO find primes for this input first

