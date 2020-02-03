module NumMagic.Opr where

import Data.Set


multiplesOf :: Int -> Int -> [Int]
multiplesOf a lim = [a*i | i <- [2..], a*i <= lim]


-- Sort and uniqify the list of Integer
uniq :: [Int] -> [Int]
uniq ns = uniq' [] ns where
  uniq' qs [] = qs
  uniq' qs (m:ms) = uniq' (addOrder m qs) ms


-- Exclude all members from list [A] in [B]
exclude :: [Int] -> [Int] -> [Int]
exclude [] _ = []
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
 

-- Find all prime numbers up to the specified number
findPrimes :: Int -> [Int]
findPrimes lim = filteroutMultiples 2 [2..lim]


filteroutMultiples :: Int -> [Int] -> [Int]
filteroutMultiples _ [] = []
filteroutMultiples _ [1] = []
filteroutMultiples _ [1,2] = [2]
filteroutMultiples a (n:ns) = 
  if n<=1 then filteroutMultiples a ns
    else if a>=last(n:ns) then n:ns -- it's over, no more elements to filter
      else if a>=n then a:(filteroutMultiples (a+1) ns) -- TAOTODO instead of monotonically increasing, we can walk up the list of primes
        else withoutMultiplesOf a (n:ns)

-- Filter the list without multiples of the specified number
withoutMultiplesOf :: Int -> [Int] -> [Int]
withoutMultiplesOf _ [] = []
withoutMultiplesOf a ns = [n | n <- ns, n `mod` a > 0] --ns `exclude` (multiplesOf n (last ns))



-- [2,3,4,5,6,7]
 
--  2 -> [4]      -> [2,3,_,5,6,7,9]
--  3 -> [6,9]    -> [2,3,_,5,_,7,_]
--  5 -> []       -> [2,3,_,5,_,7,_]
--  ..



