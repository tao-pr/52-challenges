module Main (main) where

import qualified MC

main :: IO ()
main = do
  putStrLn "Enter number of rounds: "
  n <- getLine
  let n' = read n :: Int
  print $ "Generating simulation of " ++ n ++ " rounds"


