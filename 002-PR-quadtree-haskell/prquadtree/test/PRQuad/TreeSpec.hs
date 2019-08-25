module PRQuad.TreeSpec (main,spec) where

import Test.Hspec
import Test.QuickCheck()
import PRQuad.Tree as T
import Prelude hiding (min, max)
import Data.Maybe(fromJust)

main :: IO ()
main = hspec spec

_b_ ::Bound 
_b_ = (-5,-5,5,5)

spec :: Spec
spec = do
  describe "Basic creation and insertion" $ do

    it "creates sole tree" $ do
      let n = count $ Sole _b_ (2,4)
        in n `shouldBe` 1
