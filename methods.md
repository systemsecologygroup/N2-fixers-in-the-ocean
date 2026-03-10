# Methods

This file describes the overall methods used in this project in order to achieve the results we did. It can
be thought of as a summary of [code_overview](./code_overview.md) file with regard to specifics of data processing. 
So, if more details are needed please take a look there or at the source files.

## Pre processing

Missing values encoded as empty strings were preserved during import to distinguish between structural missing data and numerical no data
values where actual recordings were present.

Firstly, all unnecessary columsn were removed and remaining are converted to numerical values. The coordinates
were converted to integer values, which includes latitude, longitude and depth. Then empty rows were removed 
and ND values replaced with a constant of -1000 in order to later remove duplicates at the end.

In order to maintain a consistent range of coordintes it was decided to keep longitude between -180 and 180. If
for a given source this was not the case, the column range was converted. 

Columns were renamed to a common standard in order to join them together. For bacterial one can select to use a 
subset of data instead of all datasets. The recommended subset is Tang and Shio. After such choice is made
the bacterial data is joined. More or less the same pipline was applied to environmental data as well.

After removing duplicates the resulting dataframe was modifies to remove -1000 constants, that signified ND cells
in the original dataframe and a small random number was placed instead. This is done to prevent the model learning
to just predict 0 and make the patterns more fussy and unclear.

The flow of data from sources to final file can be seen below.

Bacterial data supplied is in $10^{6} per \;m^{-3}$, which means that when plotting data should be mutliplied by $10^6$ in
order to match the paper, where it was sourced from.

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
In order to extrapolate onto points where bacterial data is present we compared bacterial and environmental data and picked points,
where only bacterial data is present. For such points extrapolation was performed. This was done to have the most training data
out of available datasets. 

In order to extrapolate to points with no data latitude based averages were used. For points where the methods yields no data
a neighbourhood is averaged instead to get an approximation of the expected value. This gives more or less accurate result for missing
points, which allows to increase the potential training set.

Other methods to fill NaNs were also explored but the one described above was chosen as the best balance between accuracy
and execution time.

On a chosen dataset new features were engineered. C1,C2,C3 are based on latitude and longitude and encode geographic data as
well as serve as proxy for other environmental variables that are not included in inputs, but might affect the NiFH gene concenttration. 
N:P ratio is also computed and added as a column. This is based on Tang et all paper, as the authors there performed the same feature
engineering step.

$
C1= sin(latitude \cdot \frac{\pi}{180})\\
C2= sin(longitude \cdot \frac{\pi}{180}) \cdot cos(latitude \cdot \frac{\pi}{180})\\
C3= -cos(longitude \cdot \frac{\pi}{180}) \cdot cos(latitude \cdot \frac{\pi}{180})
$

## Joining

After extrapolating environmental data to necessary points we joined with bacterial data using a left join in order to keep
only rows, where bacterial data is present. Also, duplicate points in space in environmental data were removed. This was done using 
group by and average before the joining with bacterial data. This prevents duplication of bacterial data after the join operation and
keeps the count of rows available for training consisten with the numbers shown below.

- Trichodesmium nifH Gene (x106 copies m-3)  1519
- UCYN-A nifH Gene (x106 copies m-3)         1716
- UCYN-B nifH Gene (x106 copies m-3)         1542

It was also decied to focus on the region of the ocean closer to the surface. So, points deeper than 50m were removed. In order to keep
the relation betweeb geographic coordinates and final predictions more fussy and less clear during training a small error is added
in form of a random variable. This prevents the model from focusing too much on C1,C2,C3.

On combined dataset different analysis and transformations were performed in hoped of making it easier to train on and 
make better predictions. The best transformation was using log and adding a constant to the bacterial data. Exact formulas can be
found in the source code and below:

```
"O2":(lambda x: np.log(x*(10**6)+10)),
"T":(lambda x: np.log((x+10)*(10**6))),
"N":(lambda x: np.log(x*(10**3)+10)),
"P":(lambda x: np.log(x*(10**3)+10)),
"Fe":(lambda x: np.log(x*1000+10)),
"solar":(lambda x:x),
"N:P":(lambda x: x),
"C1": (lambda x: x),
"C2": (lambda x: x),
"C3": (lambda x: x),
'Trichodesmium nifH Gene (x106 copies m-3)':(lambda x: np.log(x*(10**6)+10)),
'UCYN-A nifH Gene (x106 copies m-3)':(lambda x: np.log(x*(10**6)+10)),
'UCYN-B nifH Gene (x106 copies m-3)':(lambda x: np.log(x*(10**10)+10))
```


## Finding the best model

In order to find the best model different models were trained on all available datasets and evaluated based on RMSLE in 
order to pick the best pair (model, dataset). RMSLE is used due to large range of values in the data. It captures error
the best on such long ranges and its values mostly match quality of predicitons. 

In comparison, RMSE doesn't show much difference between pairs, where one is significantly better, than the other.

The conclusion achieved was using simple transformer and Random forest regression. In addition, we tried finding
the best hyperparameters for the model, but they seem to show little effect on overall accuracy of the results.

## Predictions

For each feature a model was selected as well as a dataset and then train test split on the datasets was performed. After training all
environmental data was fetched and transformed to a selected scale, model was used for predictions on all of it. Afterwards, a transformation
to the initial scale was performed. Results are plotted.

The final dataset was the one mentioned above: simple transformer and a random forest regression model for training and predictions for all
features. 

For plottign different configurations were used to get a better look at the data from different angles and understand it better.