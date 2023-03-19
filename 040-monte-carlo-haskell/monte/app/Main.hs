module Main (main) where

import qualified MC
import Text.Printf

main :: IO ()
main = do
  putStrLn "Enter number of rounds: "
  n <- getLine
  let n' = read n :: Int
  print $ "Generating simulation of " ++ n ++ " rounds"
  pi <- MC.simulatePi n'
  printf "Estimated value of Pi = %f\n" pi


