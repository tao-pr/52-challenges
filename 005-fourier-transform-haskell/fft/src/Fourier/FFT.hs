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
  ; let re = xk k xs cos
  ; let im = -1 * (xk k xs sin)
  ; return (re :+ im)}

-- Calculate the sum of coefficience at [k]
-- Formula: xk = sum x[n] f(2pi * k * n/N)
xk :: Int -> [Double] -> (Double -> Double) -> Double
xk k xs f = let ys = do { (i,x) <- zip [0..] xs
  ; let n = fromIntegral $ length xs
  ; return (x * f( 2.0 * pi * (fromIntegral k) * (fromIntegral i) / n)) }
    in sum ys


