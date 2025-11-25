'''
TRAINING.PY

This file stores the scalers, transformers used for training the models and functions assoicated with them
'''

import pandas as pd
import numpy as np


"""
===================================================================================================
Mathematical transformer classes used in both join_csv.ipynb and models.ipynb

Here I applied different transformations for each column, this allows for maximum 
customization and tuning and also to easily revert back the changes afterwards.
===================================================================================================
"""
class SimpleTransformer():
    '''
    Simple transformer class used for training the model. Applies mathematical functions to transform the dataset.

    Attributes:
        transforms: dictionary of transform functions for each column
        inverse_transforms: dictionary of inverse transform functions

    Methods: 
        transform: transform the data and return the resulting df
        inverse transform: reverse the transformation

    '''

    transforms = {
        "O2":(lambda x: np.log(x*(10**6)+10)),
        "T":(lambda x: np.log((x+10)*(10**6))),
        "N":(lambda x: np.log(x*(10**3)+10)),
        "P":(lambda x: np.log(x*(10**3)+10)),
        "Fe":(lambda x: np.log(x*1000+10)),
        "solar":(lambda x:x),
        "N:P":(lambda x: x),
        'Trichodesmium nifH Gene (x106 copies m-3)':(lambda x: np.log(x*(10**6)+10)),
        'UCYN-A nifH Gene (x106 copies m-3)':(lambda x: np.log(x*(10**6)+10)),
        'UCYN-B nifH Gene (x106 copies m-3)':(lambda x: np.log(x*(10**10)+10))
    }

    inverse_transforms = {
        "O2":(lambda x: (np.exp(x)-10)/(10**6)),
        "T":(lambda x: (np.exp(x))/(10**6)-10),
        "N":(lambda x: (np.exp(x)-10)/(10**3)),
        "P":(lambda x: (np.exp(x)-10)/(10**3)),
        "Fe":(lambda x: (np.exp(x)-10)/(10**3)),
        "solar":(lambda x:x),
        "N:P":(lambda x: x),
        'Trichodesmium nifH Gene (x106 copies m-3)':(lambda x: (np.exp(x)-10)/(10**6)),
        'UCYN-A nifH Gene (x106 copies m-3)':(lambda x: (np.exp(x)-10)/(10**6)),
        'UCYN-B nifH Gene (x106 copies m-3)':(lambda x: (np.exp(x)-10)/(10**10))
    }

    def __init__(self):
        print("Simple transformer initiated")

    ''' 
    apply transformations to a set of columns based on a dictionary of the format:
    col_name --> lambda function on a numpy array
    '''
    def __applyTransormations(self, dct,df):
        new_df = pd.DataFrame()
        for key in dct.keys():
            if key in df.columns:
                new_df[key] = dct[key](df[key])
        return new_df
    
    ''' 
    forward transofrm before training
    '''
    def transform(self,df):
        return self.__applyTransormations(self.transforms, df)

    ''' 
    backward transform for the model results
    '''
    def inverse_transform(self,df):
        return self.__applyTransormations(self.inverse_transforms, df)
    
class SecondTransformer():
    '''
    Second transformer calls

     Attributes:
        transforms: dictionary of transform functions for each column
        inverse_transforms: dictionary of inverse transform functions
    '''
    transforms = {
        "O2":(lambda x: np.log(x*(10**6)+10)),
        "T":(lambda x: np.log10(x+10)),
        "N":(lambda x: np.log(x*(10**3)+10)),
        "P":(lambda x: np.log(x*(10**6)+10)),
        "Fe":(lambda x: np.log(x*(10**6)+10)),
        "solar":(lambda x:x),
        "N:P":(lambda x: x),
        'Trichodesmium nifH Gene (x106 copies m-3)':(lambda x: np.log10(x*(10**8)+10)),
        'UCYN-A nifH Gene (x106 copies m-3)':(lambda x: np.log10(x*100+5)),
        'UCYN-B nifH Gene (x106 copies m-3)':(lambda x: np.log(x*(10**10)+10))
    }

    inverse_transforms = {
        "O2":(lambda x: (np.power(10,x)-10)),
        "T":(lambda x: (np.exp(x))/(10**6)-10),
        "N":(lambda x: (np.exp(x)-10)/(10**3)),
        "P":(lambda x: (np.exp(x)-10)/(10**6)),
        "Fe":(lambda x: (np.exp(x)-10)/(10**6)),
        "solar":(lambda x:x),
        "N:P":(lambda x: x),
        'Trichodesmium nifH Gene (x106 copies m-3)':(lambda x: (np.power(10,x)-10)/(10**8)),
        'UCYN-A nifH Gene (x106 copies m-3)':(lambda x: (np.power(10,x)-5)/100),
        'UCYN-B nifH Gene (x106 copies m-3)':(lambda x: (np.exp(x)-10)/(10**10))
    }

    def __init__(self):
        print("Second transformer initiated")

    ''' 
    apply transformations to a set of columns based on a dictionary of the format:
    col_name --> lambda function on a numpy array
    '''
    def __applyTransormations(self, dct,df):
        new_df = pd.DataFrame()
        for key in dct.keys():
            if key in df.columns:
                new_df[key] = dct[key](df[key])
        return new_df
    
    ''' 
    forward transofrm before training
    '''
    def transform(self,df):
        return self.__applyTransormations(self.transforms, df)

    ''' 
    backward transform for the model results
    '''
    def inverse_transform(self,df):
        return self.__applyTransormations(self.inverse_transforms, df)
    
"""
===================================================================================================
Outlier removal functions used in join_csv.ipynb
===================================================================================================
"""
#these 2 values are needed to find outliers within a given column
def getIQR(col, df):
    '''
    Get upper lower and IQR values  to find outliers within a given colum

    Args: 
        col: string for column name
        df: dataframe

    Returns:
        upper: upper limit
        lower: lower limit
        IQR: IQR
    '''
    Q1 = np.percentile(df[col].dropna(), 25, method="midpoint")
    Q3 = np.percentile(df[col].dropna(), 75, method="midpoint")
    IQR = Q3 - Q1
    return {"upper":Q3+1.5*IQR, "lower":Q1- 1.5*IQR, "IQR": IQR}

#this sets all outliers as Nan in a given single column
def setOutliersAsNaN(col, df):
    '''
    Sets all outliers as Nan in a given single column
    
    :param col: column name where to set outliers as NaN
    :param df: Dataframe
    '''
    df[col] = pd.to_numeric(df[col], errors='coerce')
    dct = getIQR(col,df)
    upper = dct["upper"]
    lower = dct["lower"]

    if (np.isnan(upper)) or (np.isnan(lower)):
        raise ValueError("Got nan value instead of boundary")

    indicies = np.where((df[col]>upper) | (df[col]<lower))[0]

    print("{0}: Lower bound: {1}; Upper Bound{2}; Outlier count: {3}".format(col, lower, upper, len(indicies)))

    df.loc[indicies, col] = np.nan    

#this sets outliers as nan in several columns
def setOutliersAsNaNinCols(cols, df):
    '''
    Sets outliers as nan in several columns
    
    :param cols: Columns to set outliers as NaN at
    :param df: Dataframe
    '''
    for col in cols:
        setOutliersAsNaN(col,df)

"""
===================================================================================================
Correlation scoring for linear correlation matricies
===================================================================================================
"""
def corScore(x,y,mtrx):
    '''
    Score the matrix by avergaing the squares of values
    
    :param x: rows of the matrix to track
    :param y: columns of the matrix to track
    :param mtrx: correlation matrix to score

    Returns:
        correlation score
    '''
    subset = mtrx.loc[x,y]
    sq_avg = (subset**2).values.sum() / subset.size
    print("{0}: correlation mean square average = {1}".format(y, sq_avg))
    return sq_avg

"""
===================================================================================================
Getting the data from the datasets and formatting it
===================================================================================================
"""
def getData(
        feature, 
        dataset, 
        x_columns=['O2', 'T', 'N', 'P', 'Fe', 'solar','N:P'], 
        y_columns=['Trichodesmium nifH Gene (x106 copies m-3)','UCYN-A nifH Gene (x106 copies m-3)','UCYN-B nifH Gene (x106 copies m-3)']
    ):
    '''
    Get subset of dataset where feature is not null
    '''
    # We need to make sure that all values left are not null. So we take a subset of values where feature is not NaN
    cleared = dataset.dropna(subset=(feature+x_columns))[x_columns+y_columns]
    # To check reuslts I print the NaN count
    imp_cols = feature+x_columns
    print("after getting data NaN count is: {0}".format(cleared[imp_cols].isnull().sum().sum()))
    return cleared

from sklearn.metrics import root_mean_squared_error

def train_model(model, X_train, y_train, model_name="-"):
    #we train the model
    model.fit(X_train, y_train)

    #get the preictions
    predictions = model.predict(X_train)

    error_rate = root_mean_squared_error(y_train, predictions)
    print("Model {0} achieved RMSE score of {1} on train dataset".format(model_name, error_rate))

    return error_rate

"""
===================================================================================================
Our own model that is stupid on purpose to use as a benchmark
===================================================================================================
"""
class DummyModel():
    '''
    This is a "Dummy model" desiged to perform as bad as possible by discarding all inputs and 
    just reproducing the average of the training data.
    '''
    value=None

    def __init__(self):
        self.value=None

    def fit(self, X_train, y_train):
        self.value = np.mean(y_train)

    def predict(self, X_train):
        return np.full(len(X_train), self.value)