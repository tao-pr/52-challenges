module SemiGr.SemiGrSpec (main,spec) where

import Test.Hspec
import Test.QuickCheck()
import Data.Complex(Complex((:+)))
import SemiGr.Semi(fromList, toList, LinkedList(..))

main :: IO ()
main = hspec spec

spec :: Spec
spec = do

  describe "Basic" $ do

    it "create linked list from list" $ do
      let a = [1, 2, 3, 4] 
        in (fromList a) `shouldBe` LinkedList 1 (LinkedList 2 (LinkedList 3 (LinkedList 4 Empt)))

    it "join two linked list with semigroup opr" $ do
      let { a = fromList [1,2,3]
          ; b = fromList [4,5,6]}
          in (toList $ a <> b) `shouldBe` [1,4,2,5,3,6]