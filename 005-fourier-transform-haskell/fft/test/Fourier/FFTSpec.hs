module Fourier.FFTSpec (main,spec) where

import Test.Hspec
import Test.QuickCheck()
import Fourier.FFT

main :: IO ()
main = hspec spec

spec :: Spec
spec = do

  describe "FFT" $ do

    it "transform steady function" $ do
      [1,2,3] `shouldBe` ([])