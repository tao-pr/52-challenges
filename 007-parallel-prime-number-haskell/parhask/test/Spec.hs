{-# OPTIONS_GHC -F -pgmF hspec-discover #-}

module Lib.Spec (main,spec) where

import Test.Hspec
import Test.QuickCheck()
import Lib

main :: IO ()
main = hspec spec

spec :: Spec
spec = do

  describe "Fundamentals" $ do

    it "finds multiples of a number" $ do

      error "no implementation"