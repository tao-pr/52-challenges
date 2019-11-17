module Fourier.FFT where

import Control.Parallel.Strategies
import Data.Complex(Complex,Complex((:+)),realPart,imagPart)
import Data.Matrix(matrix,fromList)

-- Cooley & Tukey Fast Fourier transformation of a sequence
fft :: [Double] -> [Complex Double]
fft fs = error "not implemented"

-- Typical Discrete Fourier transformation of a sequence
dft :: [Double] -> [Complex Double]
dft [] = []
dft fs = error "not implemented"

-- Compute DFT coefficient at index
dftAt :: Int -> [Double] -> [Complex Double]
dftAt _ [] = [0.0:+0.0]
dftAt i fs = if length fs <= i then [0.0:+0.0] else 
  [1.0:+0.0]


