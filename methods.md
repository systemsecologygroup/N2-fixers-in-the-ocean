# Methods

This file describes the overall methods used in this project in order to achieve the results we did. It can
be thought of as a summary of [code_overview](./code_overview.md) file with regard to specifics of data processing. 
So, if more details are needed please take a look there or at the source files.

## Pre processing

When opening the files the default nan is switched to "" empty string in order to distringuish no data and not a number
cells in the table.

Firstly, all unnecessary columsn are removed and remaining are converted to numerical values. The coordinates
are converted to integer values for better joining. Then empty rows are removed and ND values replaced with a constant
in order to later remove duplicates at the end.

If longitude is  in a different range like 0 to 360 it is itransformed. 

Columns are renames to a common standard in order to join them together and then all data is concatenated together. 
For bacterial one can select to use a subset of data instead of all datasets. The recommended subset is Tang and Shio.

Aftre removing duplicates the resulting dataframe is passed through setND again to set the constant that replaces ND
with a random very small value close to 0.

**Bacterial data preprocessing:**
```               
              ┌───────┐                 
dataset 1─────│select │                 
              │what   │                 
dataset 2─────│to keep│                 
              │       │────bact_data.csv
dataset 3─────│       │                 
              │       │                 
dataset 4─────│       │                 
              └───────┘                 
                                        
```

**Environmental data preprocessing**
```
O────┐                                            
T────│                                            
P────│                                            
N────└─OTPN.csv──┐                                
                 │                                
Fe 12──Fe.csv───merge─────┐                       
files                     │                       
                     inner join───env_data.csv    
solar─────────────────────┘                       
                                                  
```

## Filling in missing values
In order to extrapolate onto points where bacterial data is present we compare bacterial and environmental data and pick points,
where only bacterial data is present. Then for they are added as rows with no data to environmental data dataframe. 

In order to extrapolate to points with no data latitude based averages are used. For points where the methods yields no data
a neighbourhood is averaged instead to get an approximation of the expected value. 

Other methods to fill NaNs are also explored but the one described above was chosen as the best balance between accuracy
and execution time.

On a chosen dataset new features are engineered. C1,C2,C3 are based on latitude and longitude and encode geographic data as
well as serve as proxy for other environmental variables that are not included in inputs, but might affect the NiFH gene concenttration. 
N:P ratio is also computed and added as a column.

## Joining

After eliminating NaN values in environmental data we can join with bacterial data using a left join in order to keep
only bacterial data rows. Also, duplicate points in space in environmental data are removed using group by and average before the join.
This prevents duplication of bacterial data after the join operation.

On combined dataset different analysis and transformations are performed in hoped of making it easier to train on and 
make better predictions. The best transformation was using log10 and adding a constant to the bacterial data. Exact formulas can be
found in the source code.

## Finding the best model

In order to find the best model different models are trained on all available datasets and evaluated based on RMSLE in 
order to pick the best pair (model, dataset). RMSLE is used due to large range of values in the data. It captures error
the best on such long ranges and its values mostly match quality of predicitons. 

In comparison, RMSE doesn't show much difference between pairs, where one is significantly better, than the other.

## Predictions

For each feature a model is selected as well as a dataset and then train test split on the datasets is performed. After training all
environmental data is fetched and transformed to a selected scale, model is used for predictions. Afterwards, a transformation
to the initial scale is performed. Results are plotted.

For plottign different configurations are used to get a better look at the data from different angles and understand it better.