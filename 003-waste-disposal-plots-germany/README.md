# Plots of Waste Disposal Density in Schleswig-Holstein over Time

TBA

## Dataset

This project uses the opendata of 2015-2017 waste disposal in Schleswig-Holstein, in the north of Germany from following sources

- 2017 : https://www.govdata.de/web/guest/suchen/-/details/abfallentsorgung-in-schleswig-holstein-2017-anlagen-der-abfallentsorgung
- 2016 : https://www.govdata.de/web/guest/suchen/-/details/abfallentsorgung-in-schleswig-holstein-2016-anlagen-der-abfallentsorgung-korrektur
- 2015 : https://www.govdata.de/web/guest/suchen/-/details/abfallentsorgung-in-schleswig-holstein-2015-anlagen-der-abfallentsorgung-korrektur


# Initial preparation

Create and start a virtual environment as follows.

```
$ virtualenv 003
$ source 003/bin/activate
```

Install all required packages with jupyter notebook kernel as follows

```
$ pip3 install -r requirements.txt
$ ipython kernel install --user --name=003
```

Then the notebook can be executed with the kernel named `003`.

NOTE: You can deactivate the session later with

```
$ deacticate
```

### Setup Google API key

Given you have a system variable `GOOGLE_API_KEY` containing your active 
Google API Key, then export it to the local file as follows

```
$ echo $GOOGLE_API_KEY > google_api_key
```

## Licence

MIT