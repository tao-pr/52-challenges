# Let TensorFlow estimate the crosshair coordinates in images

TBD

## Prerequisites

Prepare environment with `virtualenv`.

```bash
$ virtualenv env
$ source env/bin/activate
$ pip install -r requirements.txt
```

## Run

There are a few options you can run the tensor as follows.

### 0. Generate the training data

The repository has a script to generate the image data for you. 
You can either quickly run the following.

```bash
$ ./GEN_DATA
```

or generate data with your own desired parameters

```bash
$ python3 -m tensor.data --saveto {PATH} --size {NUM_FILES} --dim {IMAGE_WIDTH}
```

### 1. Train the model

Running the following script to train the model

```bash
$ ./TRAIN
```

or train with your own desired parameters

```bash
$ python3 -m tensor.run --datapath {PATH} --ratio {TRAIN_RATIO} \
                        --batch {BATCHSIZE} --epoch {NUM_EPOCHS}
```

### 2. Generate dataset for testing

TBD

### 3. Test

TBD

## Licence

MIT