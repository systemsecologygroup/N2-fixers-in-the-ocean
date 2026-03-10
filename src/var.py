'''
ABOUT:

This file contains key variables used for training and creating the models. 
That is so as to avoid redundancy in the existing files and make the project
easier to adjust and change in the future.
'''


'''
TRAINING:

In order to apply changes to the set of features used for trainign the list can be edited to be the subset of the full set.

This might be useful to see the effects of different variables on the overall output and predictions made.

- geo_range: range of latitudes from where the data for training is used
- x_columns: range of columns to be trained on
- y_columns: predicted values for the model
- coordinate_cols: coordinates column names

- x_canon: DO NOT CHANGE, maximum allowed set of inputs
'''
geo_range=90#tweak this
x_columns = ['O2', 'T', 'N', 'P', 'Fe', 'solar','N:P',"C1","C2","C3"]#tweak this
y_columns = ['Trichodesmium nifH Gene (x106 copies m-3)','UCYN-A nifH Gene (x106 copies m-3)','UCYN-B nifH Gene (x106 copies m-3)']
cordinates_cols = ["LONGITUDE", "LATITUDE","DEPTH (m)"]

x_canon = ['O2', 'T', 'N', 'P', 'Fe', 'solar','N:P',"C1","C2","C3"]#DO NOT CHANGE
y_canon = ['Trichodesmium nifH Gene (x106 copies m-3)','UCYN-A nifH Gene (x106 copies m-3)','UCYN-B nifH Gene (x106 copies m-3)']