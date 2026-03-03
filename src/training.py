'''
TRAINING.PY

This file stores the scalers, transformers used for training the models and functions assoicated with them
'''

import pandas as pd
import numpy as np
import joblib as joblib

from var import x_canon, y_canon

"""
===================================================================================================
Mathematical transformer classes used in both join_csv.ipynb and models.ipynb

Here I applied different transformations for each column, this allows for maximum 
customization and tuning and also to easily revert back the changes afterwards.
===================================================================================================
"""
class MathTransformer():
    '''
    Math transformer class used for training the model. Applies mathematical functions to transform the dataset. This
    class is meant to be inherited from and with attributes override. By default no transform is applied.

    Attributes:
        transforms: dictionary of transform functions for each column
        inverse_transforms: dictionary of inverse transform functions

    Methods: 
        transform: transform the data and return the resulting df
        inverse_transform: reverse the transformation

    '''

    transforms = {
        "O2":(lambda x: x),
        "T":(lambda x: x),
        "N":(lambda x: x),
        "P":(lambda x: x),
        "Fe":(lambda x: x),
        "solar":(lambda x:x),
        "N:P":(lambda x: x),
        "C1": (lambda x: x),
        "C2": (lambda x: x),
        "C3": (lambda x: x),
        'Trichodesmium nifH Gene (x106 copies m-3)':(lambda x: x),
        'UCYN-A nifH Gene (x106 copies m-3)':(lambda x: x),
        'UCYN-B nifH Gene (x106 copies m-3)':(lambda x: x)
    }

    inverse_transforms = {
        "O2":(lambda x: x),
        "T":(lambda x: x),
        "N":(lambda x: x),
        "P":(lambda x: x),
        "Fe":(lambda x: x),
        "solar":(lambda x:x),
        "N:P":(lambda x: x),
        "C1": (lambda x: x),
        "C2": (lambda x: x),
        "C3": (lambda x: x),
        'Trichodesmium nifH Gene (x106 copies m-3)':(lambda x: x),
        'UCYN-A nifH Gene (x106 copies m-3)':(lambda x: x),
        'UCYN-B nifH Gene (x106 copies m-3)':(lambda x: x)
    }
    def __init__(self):
        '''
        Constructor method
        '''
        print("Simple transformer initiated")

    
    def __applyTransormations(self, dct,df):
        ''' 
        apply transformations to a set of columns based on a dictionary of the format:
        col_name --> lambda function on a numpy array
        '''
        new_df = pd.DataFrame()
        for key in dct.keys():
            if key in df.columns:
                new_df[key] = dct[key](df[key])
        return new_df
    
    def transform(self,df):
        ''' 
        forward transofrm before training
        '''
        return self.__applyTransormations(self.transforms, df)

    def inverse_transform(self,df):
        ''' 
        backward transform for the model results
        '''
        return self.__applyTransormations(self.inverse_transforms, df)
    


class SimpleTransformer(MathTransformer):
    '''
    Simple transformer class used for training the model. Applies mathematical functions to transform the dataset. 
    Mainly log10 is applied with constant added to make sure values are non negative. 

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
        "C1": (lambda x: x),
        "C2": (lambda x: x),
        "C3": (lambda x: x),
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
        "C1": (lambda x: x),
        "C2": (lambda x: x),
        "C3": (lambda x: x),
        'Trichodesmium nifH Gene (x106 copies m-3)':(lambda x: (np.exp(x)-10)/(10**6)),
        'UCYN-A nifH Gene (x106 copies m-3)':(lambda x: (np.exp(x)-10)/(10**6)),
        'UCYN-B nifH Gene (x106 copies m-3)':(lambda x: (np.exp(x)-10)/(10**10))
    }
    
class SecondTransformer(MathTransformer):
    '''
    Second transformer calls with adjusted functions.

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
        "C1": (lambda x: x),
        "C2": (lambda x: x),
        "C3": (lambda x: x),
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
        "C1": (lambda x: x),
        "C2": (lambda x: x),
        "C3": (lambda x: x),
        'Trichodesmium nifH Gene (x106 copies m-3)':(lambda x: (np.power(10,x)-10)/(10**8)),
        'UCYN-A nifH Gene (x106 copies m-3)':(lambda x: (np.power(10,x)-5)/100),
        'UCYN-B nifH Gene (x106 copies m-3)':(lambda x: (np.exp(x)-10)/(10**10))
    }
    
"""
===================================================================================================
Outlier removal functions used in join_csv.ipynb NO LONGER USED
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
        x_columns=None, 
        y_columns=['Trichodesmium nifH Gene (x106 copies m-3)','UCYN-A nifH Gene (x106 copies m-3)','UCYN-B nifH Gene (x106 copies m-3)']
    ):
    '''
    Get subset of dataset where feature is not null
    '''
    if x_columns == None:
        x_columns = list(set(dataset.columns)-set(y_columns))
    # We need to make sure that all values left are not null. So we take a subset of values where feature is not NaN
    cleared = dataset.dropna(subset=(feature+x_columns))[x_columns+y_columns]
    # To check reuslts I print the NaN count
    imp_cols = feature+x_columns
    print("after getting data NaN count is: {0} for feature: {1}".format(cleared[imp_cols].isnull().sum().sum(), feature))
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
    
"""
===================================================================================================
TRANSFORMERS for multiple datasets
===================================================================================================
"""
transformers = joblib.load("../model/transformers")#transformers as stored in a file

def transofrm_back(name,df):
    ''' 
    transform the dataset back to original scale

    Args:
        name: name of the dataset type used
        df: dataframe

    Returns:
        a modified dataset with the same number and names of columns but in og scale
    '''
    #saved for laters
    actual_cols = df.columns
    #in case the columns that are used do not consitute the full available set
    cols_canon = set(x_canon+y_canon)

    #the diffrerence is the missing columsn that we need to add to make it work
    #this is due to the transformers from scikit learn requiring the same set of columns regardless of 
    #what is happening
    cols_dif = cols_canon - set(actual_cols)
    N = df.shape[0]

    #columns are added
    for col in cols_dif:
        df[col]=np.ones(N)

    #both naming and order are important so the order is maintained here
    df = df[x_canon+y_canon]

    #now we actually transform the data
    if "simple" in name:
        #print("using a simple tr")
        return SimpleTransformer().inverse_transform(df)[actual_cols]
    elif "second" in name:
        if "scaled" in name:
            df = pd.DataFrame(transformers["second_transform_scaler"].inverse_transform(df), columns=df.columns)
        return SecondTransformer().inverse_transform(df)[actual_cols]
    elif "power" in name:
        #print("power branch is called")
        transfored_arr = transformers["power_transf"].inverse_transform(df)
    elif "quantile" in name:
        #print("quantile branch is called")
        transfored_arr = transformers["quantile_transf"].inverse_transform(df)
    else:
        #print("raw branch")
        return df[actual_cols]
    
    return pd.DataFrame(transfored_arr, columns=df.columns)[actual_cols]


def transofrm_forward(name,df):
    ''' 
    transform the dataset to a specific scale
    Args:
        name: name of the dataset type used
        df: dataframe

    Returns:
        a modified dataset with the same number and names of columns but in og scale
    '''
    #saved for laters
    actual_cols = df.columns
    #in case the columns that are used do not consitute the full available set
    cols_canon = set(x_canon+y_canon)

    #the diffrerence is the missing columsn that we need to add to make it work
    #this is due to the transformers from scikit learn requiring the same set of columns regardless of 
    #what is happening
    cols_dif = cols_canon - set(actual_cols)
    N = df.shape[0]

    #columns are added
    for col in cols_dif:
        df[col]=np.ones(N)

    #both naming and order are important so the order is maintained here
    df = df[x_canon+y_canon]

    #now we actually transform the data
    if "simple" in name:
        return SimpleTransformer().transform(df)[actual_cols]
    elif "second" in name:
        second = SecondTransformer().transform(df)
        if "scaled" in name:
            df = pd.DataFrame(transformers["second_transform_scaler"].transform(second), columns=df.columns)
            return df[actual_cols]
        else:
            return second[actual_cols]
    elif "power" in name:
        transfored_arr = transformers["power_transf"].transform(df)
    elif "quantile" in name:
        transfored_arr = transformers["quantile_transf"].transform(df)
    else:
        return df[actual_cols]
    
    return pd.DataFrame(transfored_arr, columns=df.columns)[actual_cols]
