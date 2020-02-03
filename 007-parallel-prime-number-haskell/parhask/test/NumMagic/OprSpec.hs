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

    it "exclude elements from the list" $ do
      exclude [1..10] [1,5,7,8,10] `shouldBe` [2,3,4,6,9]

  describe "Multiples" $ do

    it "filter list without multiples of something" $ do
      withoutMultiplesOf 3 [1..28] `shouldBe` [1,2,4,5,7,8,10,11,13,14,16,17,19,20,22,23,25,26,28]