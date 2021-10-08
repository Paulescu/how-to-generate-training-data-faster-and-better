# How to generate training data for your ML models, faster and better.

## What is this repo about?

Pattern to generate tabular training data from an SQL-type DB. Faster and better
than what you are doing at the moment.

Go check my [blog post](http://datamachines.xyz/2021/10/08/how-to-generate-training-data-faster-and-better/) to know more.

## Quick setup

You need Python >= 3.7 and a tool to install the exact packages you need for this
code to run as expected.

Instructions for virtualenv:
```
...cd into the root directory...
$ pip install virtualenv
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

## Example usages

```
python src/data.py --from 2021-07-12 --to 2021-10-08
```

```
python src/data_faster.py --from 2021-07-12 --to 2021-10-08 --overwrite
```

```
python src/data_faster_and_better.py --from 2021-07-12 --to 2021-10-08 --overwrite
```



