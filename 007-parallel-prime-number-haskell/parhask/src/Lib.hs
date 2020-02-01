module Lib
    ( multiplesOf,
      findPrimes
    ) where

import Control.Parallel.Strategies

-- Find all multiples of the specified integer
multiplesOf :: Int -> Int -> [Int] -> [Int]
multiplesOf n lim primes = [n*p | p <- primes, n*p <= lim]

-- Find all prime number up until the specified bound
findPrimes :: Int -> [Int]
findPrimes lim = error "not implemented"