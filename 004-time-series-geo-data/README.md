# Time-Series Geographical Data Regression Problem

Build a simple regression model on time-series geographical data.

## Requirements

Download weather dataset from [https://www.kaggle.com/berkeleyearth/climate-change-earth-surface-temperature-data/download](Berkeley earth climate dataset on Kaggle), extract the zip and put all csv files 
into: `$HOME/data/global-temperature/`

Install the internal package before running the Jupyter notebooks 

```
$ pip install -e libdata
```

Then you can start the jupyter notebook as usual.

## Executing the package

Try running the package as follows

```
$ python3 -m libdata
```

For the first time, the package will pick up the csv dataset 
and run a model training. The process produces two output files:

- features_train.csv
- model.pkl

Running the package once again will pick up the model and do a classification.

## Results

The model is built on 10,746 samples and tested on 1,897 samples.
The prediction of temperature changes performs as follows.

mean square error : 0.06516339518348233
.... Error < 1 celcius : 23.563521349499208%
.... Error < 3 celcius : 47.02161307327359%
.... Error < 5 celcius : 22.72008434370058%
.... Error < 10 celcius : 6.378492356352135%
.... Error < inf celcius : 0.316288877174486%

## Licence

TBD
