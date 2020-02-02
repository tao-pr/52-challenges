module NumMagic.OprSpec (main,spec) where

import Test.Hspec
import Test.QuickCheck()
import NumMagic.Opr

main :: IO ()
main = hspec spec

spec :: Spec
spec = do

  describe "Uniqify" $ do

    it "add a number to an ordered list" $ do
      addOrder 4 [1,2,3,5] `shouldBe` [1,2,3,4,5]

    it "add a number to an ordered list (duplicate)" $ do
      addOrder 4 [1,2,3,4,5] `shouldBe` [1,2,3,4,5]

    it "add a number to an empty list" $ do
      addOrder 4 [] `shouldBe` [4]

    it "uniqify and sort a list" $ do
      uniq [1,10,5,4] `shouldBe` [1,4,5,10]

  describe "Multiples" $ do

    it "finds multiples of a number" $ do
      (multiplesOf 7 35 [2,3,5]) `shouldBe` [14,21,28,35]

    it "finds multiples of a number (highly nested)" $ do 
      (multiplesOf 12 100 [2,3,5,7,11]) `shouldBe` [24,36,48,60,72,84,96]