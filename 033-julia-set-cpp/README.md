# Julia set with OpenCV

Visualise Julia set with OpenCV

### Prerequisites

C++17 compatible compiler (gcc preferred)

### Compile & Run

```
./make.sh
```

And run with

```
build/julia
```

### Sample sets

All following are rendered with `z_re` between [-1.5,+1.5] and `z_im` between [-1.5,+1.5], 
resolution of 0.001 and 50 iterations

```
c = -1
```

![IMG](media/c-1.png)


```
c = 0
```

![IMG](media/c-2.png)


```
c = -i
```

![IMG](media/c-3.png)


```
c = -0.123 + 0.745i
```

![IMG](media/c-4.png)


```
c = -0.75i
```

![IMG](media/c-5.png)


```
c = 0.285 + 0.01i
```

![IMG](media/c-6.png)


```
c = -0.4 + 0.6i
```

![IMG](media/c-7.png)


```
c = 0.285
```

![IMG](media/c-8.png)


```
c = -0.70176 + -0.3842i
```

![IMG](media/c-9.png)


```
c = −0.835 − 0.2321i
```

![IMG](media/c-10.png)

```
c = −0.7269 + 0.1889i

This one is rendered with iteration = 250
```

![IMG](media/c-11.png)

