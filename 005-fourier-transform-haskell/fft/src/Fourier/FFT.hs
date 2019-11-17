module Fourier.FFT where

import Control.Parallel.Strategies
import Data.Complex(Complex,Complex((:+)),realPart,imagPart)
import Data.Matrix(matrix,fromList)

-- Cooley & Tukey Fast Fourier transformation of a sequence
fft :: [Double] -> [Complex Double]
fft xs = dft xs

-- Typical Discrete Fourier transformation of a sequence
dft :: [Double] -> [Complex Double]
dft [] = []
dft xs = do { k <- [0..length xs - 1]
  ; let re = sumCoef k xs cos
  ; let im = sumCoef k xs sin
  ; return (re :+ im)}

-- Calculate the sum of coefficience at [k]
sumCoef :: Int -> [Double] -> (Double -> Double) -> Double
sumCoef _ _ _ = error "not implemented"


