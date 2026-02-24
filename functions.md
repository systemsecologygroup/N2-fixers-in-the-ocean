# Functions and classes used in this project

This file explains the exact functions, their funtionalities in an overview manner. For more
details go to corresponding file and read the comments there. 

## format.py

This file contains functions used in the preprocessing step of the project.
Where data is formatted and joined together. File with the source can be found
at [format.py](./new_approach/format.py)

| Function           | Use cases                                              |
|--------------------|--------------------------------------------------------|
|removeEmptyRows     | drop rows with no values in them at all                |
|removeRed           | remove NOT specified columns from the dataframe        |
|objToNum            | convert all object columns to a numeric value          |
|filterDepth         | filter out all the rows that are too deep              |
|setND               | set no data values in the dataframe to a random value close to 0 |
|roundCoord          | round a list of coordinate columns to integer values   |
|constructFeatures   | create C1,C2,C3 features based on lat and long cols    |

## training.py

[training.py](./new_approach/training.py) here you can find the source of the functions.

This file contains both functions and classes used during training. Most of them 
apply different transformations in order to achieve better results during training.


| Function           | Use cases                                              |
|--------------------|--------------------------------------------------------|
|getIQR              | get IQR values for removing outliers                   |
|setOutliersAsNaN    | set outliers as np.NaN values                          |
|setOutliersAsNaNinCols| set outliers as NaN in several columns(No longer used)|
|||
|getData             | get only rows where data is present                    |
|train_model         | train a given model and print the score                |
|||
|transofrm_back      | transform the data to original scale                   |
|transofrm_forward   | transform data to a specific scale, normalize          |

These are my classes for using math functions specified manually in order to transform
data in a more custom manner.

| Class              | Use cases                                              |
|--------------------|--------------------------------------------------------|
|MathTransformer     | Use mathematical functions for transform, not instances|
|SimpleTransformer   | Child of MathTransformer uses log10 for most transforms|
|SecondTransformer   | Child of MathTransformer variation on the SimpleTr-r   |

This class is used for comparison with real models. The idea is to see if the model
actually performs better than just predicting the average. 

| Class              | Use cases                                              |
|--------------------|--------------------------------------------------------|
|DummyMode           | Learn the average of train and always predict it, discard inputs|

## visualize.ppy

[visualize.py](./new_approach/visualize.py/) source file.

Since most plots repeat and are similar common functions to create them are grouped into this file. 

| Function           | Use cases                                              |
|--------------------|--------------------------------------------------------|
|plotColsOnMap       | plot geo data on a map, quite flexible and adjustable function|
|histCols            | plot histograms of specified columns                   |
|plotCorMatr         | plot the correlation matrix                            |
|errorScorePlot      | plot the error scores of different models together     |