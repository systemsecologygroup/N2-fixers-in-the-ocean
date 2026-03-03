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

The final data column names are also named the same way for the same type of bateria. 

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

### $O^2$,$T$, $P$, $N$

Firstly netCDF files are opened and visualized. Then the same files are reopened for processing and sliced based on *desired_depth*. Columns are renamed, when the xarray is converted to a pandas dataframe. The coordinates are rounded for better join. 

Finally, the 4 environmental variables are joined together and empty rows are dropped before saving to csv.

### Solar radiation

[ERA5 monthly averaged data on single levels from 1940 to present](https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels-monthly-means?tab=overview) is the source for this data, in terms of exact features chosen in the request for the data the following were selected:
- **Product type:** 
Monthly averaged reanalysis
- **Mean rates:** Mean surface downward long-wave radiation flux
- **Months:** all months
- **Year**: 2024
- **Time** 00:00 - the only available option

The data file is openedd and the specific solar feature contained there is averaged over time and plotted. Then the file is converted to a pandas dataframe. 

Coordinates are rounded. Next data is grouped by geographic locations and averaged to remove duplicate points. Columns are renamed to fit the common standard and for better readability. Also, no step for dropping empty rows is  needed as there are no null values. Coordinates are then rounded. 

However, we notice that the longitude is out of range. So it is converted to -180<->180 range form 0<->360. As not all sunlight is usable by bacteria the final values are mutliplied by $0.45$ to match that. 

One final note here is presence of points in the continents, which means that when this data is joined with the rest an inner join should be used.

### $Fe$ data

The data was provided to me in form of 12 NetCDF files each for a single month containing points for different depths.

Firstly, as usual all 12 files are opened and stored in an array. Then the data is visualized across all 12 months. Also, the depth is sliced up to desired depth. 

All 12 months are joined together based on MONTH dimension. Then all points are grouped by the 3 coordinates like above and averaged so as to avoid duplicated. 

Then redundant columns are removed and remaining ones are renamed to fit in. Coordinate range is fixed to to -180 to 180 range like before for the same reason. 

Lastly, NaN values in empty rows are removed, which prevents empty points in the middle of the continent from appearing and then being extrapolated to. In addition, again duplicate points are removed by averaging the grouped by points based on 3 coordinates. 

### Joining them together

The final step is joining 3 csv files together. Firstly, OTPN and Fe data is joined based on settign 3 indicies. Then the joined data is visualized in histograms.

The last step is opening preprocessed solar data and joining via inner joined based on latitude and longitude alone, as those are the only 2 coordinates available for it. The join is inner in order to leave only ocean data.

The final dataset is saved as *env_data.csv* to the features folder. 

Also the final data is also plotted. It contains a few missing points that need to be extrapolated to. 

# FILL ENV

The goal of this file is to extrapolate on the remaining missing points and the points where bacterial data is present. The last part is crucial for getting more training data. 

Firstly the dataset is opened and key variables like expected columns name lists are defined. Then, bacterial data is also opened and a comparison join is performed. Rows present only in bacterial data are selected and added to the initial dataframe. Averages for the environmental variables at points where both environment and baterial data is present are computed and saved for later use. 

## Simple approach

The averages computed before can be simply used to fill in missing values in corresponding columns. This is the least accurate, but the fastest to execute approach. 

## Complex fill

In this approach for each column latitude based average is computed and used for imputation. This makes it more accurate than the previous attempt, while remaining relatively quick. The idea here is that latitude is a key factor in how the data is distributed. 

Sadly, this doesn't comer all points leaving out a decent amount. 

### Strategy 1: Go back to simple fill

First strategy is to copy the data so as to keep the original and just use the means we computed for the entire globe from before. Essentially performing a simple fill on remaining points. This is fast, but not so accurate approach. 

### Strategy 2: averages of neighbourhoods

The second strategy is to instead compute average of a given neighborhood and use it to impute a missing value. This takes way longer to execute but is way higher quality. So, this is the final data that is used for training.

Algorithm:

For each data column:

    1. select all rows where there are nulls left for a given column
    2. For each row repeat the next steps
    3. retrieve coordinates of a given point
    4. Filter for rows in the neighbourhood and average retrieved data
    5. If no data is found, expand the search radius by 100%. If data is find exit loop and impute the data. 

## KNN

This approach was also initially considered. Using KNN imputer can be useful, but it was decided against it as it takes way too much time.

## Feature engineering

On a selected dataset as the final one new features are added. In out case the complex fill with neighbourhood based imputer is used. 

This is meant to replicate the approach the Tang et all paper used and adds C1,C2,C3 as new geographic features and also N:P ratio. 

Final results are saved for the next step. 

These are the formulas:
$
C1= sin(latitude \cdot \frac{\pi}{180})\\
C2= sin(longitude \cdot \frac{\pi}{180}) \cdot cos(latitude \cdot \frac{\pi}{180})\\
C3= -cos(longitude \cdot \frac{\pi}{180}) \cdot cos(latitude \cdot \frac{\pi}{180})
$

And for N:P ratio this is simple division.

# JOIN_CSV

# MODELS

# PREDICT

# SUMMARY