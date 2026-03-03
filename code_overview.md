# CODE OVERVIEW AND DESCRIPTIONS

This file gived a detailed overview of how this project works and what parts is it made of. Each sections corresponds to 
a notebook of the same name. Order mostly matched the order of recommended execution.

This file does not describe exact order of execution and details about each function as those can be found respectively in 
the README file and the .py files where the functions are declared. 

It gives high level logic description not absolute technical details as those can be found by just reading the code and comments.

The text is partially based on the internship_report.pdf file as a lot of things remain relevant.

# OBS_NIFH

## Introduction

Firstly, the data is spread over several datasets with different formatting and
scales. So, the first step is to keep only the data we need and format it in
the same way.

Secondly, it is of high importance to make a join between the datasets
possible. This means that we shouldn’t have duplicate coordinates and float-
ing point numbers for latitude and longitude. Otherwise, there is a high
chance of most rows containing either environmental or bacterial data, but
not both and an inner join returning an empty set

Data For NiFH genes datasets is preprocess mostly the same way as the column names and scales are more or less
consistent across different datasets.

## Datasets

There are 4 datasets that are provided. 3 of them contain Trichodesmium, UCYN-A,B and 1 only UCYN-A. The 
final table contains 3 spatial coordinates: **Longitude, Latitude and Depth (m)**. Coordinates are integers
, while data is floating point.

## Steps of the pipeline

GENERAL STEPS:

1. Open the dataset, with NaN values being only "" empty string, keep defualt NaN is disabled
2. If needed columns are renamed to match the common list
3. prePrNifh function is called, that contains most of the preprocessing:
    1. dataset is copied not to change the original
    2. ND values are set either to close to 0 or -1000 if random is False
    3. Redundant columns are removed
    4. Remaining columns are converted from object to a numerical value
    5. Empty data rows are removed, where no data besides coordinates is present
    6. Coordinates are rounded to int and result returned
4. Datasets are joined into a single one
5. Duplicate rows are removed
6. If random was set to False -1000 is set to a random value close to 0

This is mostly the end of actual changes to the data. 


7. Remaining cell just plot the data and save it to a csv file in features folder

# OBS_ENV

## Intoduction

Similarly, to the previous section the goal is to have 3 spatial coordinates and each input feature to be contained
in a single corresponding column.

# FILL ENV

# MODELS

# PREDICT

# SUMMARY