# Skewed Data Classification Problem

Build classification on Highly skewed training set. Trying multiple 
sampling techniques and evaluations.

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

## Licence

TBD
