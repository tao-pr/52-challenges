# 005 : Fast Fourier Transformation with Haskell

Fast Fourier transformation implementation with purely-functional flavour. I opted for [Cooley & Tukey algorithm](https://en.wikipedia.org/wiki/Cooley%E2%80%93Tukey_FFT_algorithm) for an implementation of FFT, which is also a very common approach for the task.

## Additional Resources

For a quick definition of Fast Fourier Transformation and its relation with Discrete Fourier Transformation, see [TU-Chemnitz lecture](https://www.tu-chemnitz.de/informatik/ThIS/downloads/courses/ws02/datkom/Fouriertransformation.pdf)

## Prerequisites

- Haskell Stack build tool (https://docs.haskellstack.org/en/stable/README/)

## Install dependencies, build and run test

```
$ stack install
$ stack build
$ stack test
```


## Licence

BSD