# Challenge 024 - Table reconstruction from image

Extend challenge 006 so it extracts and reconstructs information 
from table image.

## Constraints

- Use C++17 style
- Get shape information of the table, rows, cols

## Prerequisites

C++17 compatible gcc compiler with OpenCV3 library.

## Build and run

```
$ ./make.sh
```

Then

```
$ bin/extract
```

## Outputs

Extracted line components from image 

![1](data/lines.jpg)

Clean lines

![2](data/lines-filtered.jpg)

Extended lines 

![3](data/lines-extended.jpg)

Reconstructed tables

![4](data/tables.jpg)


## Run notebooks

Create and start a virtual environment as follows.

```
$ virtualenv env
$ source env/bin/activate
```

Install all required packages with jupyter notebook kernel as follows

```
$ pip3 install -r requirements.txt
$ ipython kernel install --user --name=env
```

Then the notebook can be executed with the kernel named `env`.
