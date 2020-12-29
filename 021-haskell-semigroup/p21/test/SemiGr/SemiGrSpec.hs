module SemiGr.SemiGrSpec (main,spec) where

import Test.Hspec
import Test.QuickCheck()
import Data.Complex(Complex((:+)))
import SemiGr.Semi(fromList)

main :: IO ()
main = hspec spec

spec :: Spec
spec = do

  describe "Basic" $ do

    it "create linked list from list" $ do
      error "TAOTODO"