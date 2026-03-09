import pandas as pd
import numpy as np

from var import cordinates_cols, y_columns

"""
===================================================================================================
PRE PROCESSING BASIC FUNCTIONS

These functions are used to format the dataset to a common form and exclude unnecessary data.
===================================================================================================
"""
def removeEmptyRows(cols, df):
    """

    Remove empty rows in dataframe where all specified columns are empty.

    This is essentially my wrapper on dropna function as it was frequently used.

    Args:
        cols: list of column names
        df: pandas dataframe
    
    Returns:
        modified dataframe
    """
    return df.dropna(subset=cols, how='all')


def removeRed(keepers, df):
    """
    This function removes all not specified columns from the dataframe

    Args:
        keepers: list of column names tp keep
        df: pandas dataframe
    
    Returns:
        nothing

    """
    cols = set(df.columns) - set(keepers)
    df.drop(columns=list(cols), inplace=True)

def objToNum(df):
    """
    Convert all object type columns to numeric

    Args:
        df: pandas dataframe
    
    Returns:
        nothing
    """
    object_columns = df.select_dtypes(include='object').columns.tolist()
    for col in object_columns:
        df[col]=pd.to_numeric(df[col], errors="coerce")

def filterDepth(df, depth = 50, depth_col = "DEPTH (m)"):
    """
    Filter the column encodign depth in meters so that only values under a certain constant are kept.

    Args:
        df: pandas dataframe
        depth: max depth value to be kept(default 50)
        depth_col: column to be filtered(defualt 'DEPTH(M)')
    
    Returns:
        modified dataframe
    """
    df_mask = (df[depth_col] <=depth)
    df_depth = df[df_mask]
    return df_depth

def setND(dataframe, columns, random=True):
    """
    This function modifies columns specidies where it finds ND values to be either close to 0
    with some noise or -1000 so they can be further modified and compared.

    Args:
        dataframe: dataframe to modify
        columns: columns to check for ND values and modify  
        random: set value as random close to 0 or -1000
    Returns:
        nothing
    """
    #range for the random function
    high = 10.0**(-2)
    low = 10.0**(-6)

    #if it is not a random value we need to indicate that this is ND. So value out of likely range is choden
    new_nd = -1000.0

    if (random):
        print("Imputing ND values with uniform random distribution between {0} and {1}".format(low, high))
    else: 
        print("Imputing ND values with a constant {0}".format(new_nd))

    for col in columns:
        col_str = dataframe[col].astype(str).str.strip()

        mask = (col_str=="n.d.") | (col_str=="ND") |  (col_str=="nan") | (col_str=="dnq")  | (col_str=="bd") | (dataframe[col]==new_nd)
        dataframe[col] = pd.to_numeric(dataframe[col], errors="coerce")

        if (random):
            dataframe.loc[mask, col]=np.random.uniform(low, high, size=mask.sum())#used to be just 0
        else:
            dataframe.loc[mask, col]=new_nd
      
def roundCoord(cols, df, coord_cols=["LATITUDE","LONGITUDE"]):
    """
    Round the coordinate columns and returns the resulting dataframe with coordinate and specified columns kept.

    Args:
        cols: list of column names to keep that are not coordinates
        df: pandas dataframe
        coord_cols: columns to round in the process (default = ["LATITUDE","LONGITUDE"])
    Returns:
        modified dataframe
    """
    if df is None:
        raise ValueError("Dataframe passed is None")
    for col in cols+coord_cols:
        if col not in df:
            raise KeyError("column {0} is not found in dataframe".format(col))
        
    # we separate the data and coordinates in order to round the coordinate grid
    coordinates = []
    for col in coord_cols:
        coordinates.append(np.round(df[col]).astype(int))

    coord_data = pd.concat(coordinates, axis=1)
    data = df[cols]

    # we join the data back together
    df_rnd = pd.concat([coord_data, data], axis=1)
    return df_rnd

"""
===================================================================================================
NIFH DATA PREPROCESSING PIPELINE

This function combines the functions above for a single consistent way to transform the dataset
into a new format.
===================================================================================================
"""

def prePrNifh(df, y_col, cord=cordinates_cols, random=True):
    """
    Preprocess a given nifh dataset so it matches the format expected. 

    Args:
        df: dataframe with the data
        cord: coordinate columns that will be rounded
        y_col: data columns not to round
        random: should the ND points be set as a random value or not
    Returns:
        a processed dataframe with numercial columns and rounded coordinates
    """

    new_df = df.copy()#data is copied to avoid overwriting the og
    setND(new_df, y_col, random=random)#replace ND with a special value or random

    #I removed all redundant columns and made everything into a number
    removeRed(y_col+cord, new_df)
    objToNum(new_df)

    #if empty rows are created they should be removed
    new_df = removeEmptyRows(y_col,new_df)

    #coordinates are rounded
    return roundCoord(cols=y_col, df=new_df, coord_cols=cord)

"""
===================================================================================================
FEATURE ENGINEERING C1,C2,C3
===================================================================================================
"""
def constructFeatures(dataframe):
    """
    The dataframe is modified to include N:P ratio and modified coordinates as inputs to the model.

    The coordinates transformation is based on the formula provided in Tang et all.
    
    :param dataframe: a pandas dataframe with lat, long and depth columns as well as N,P 
    """
    #columns presence is checked to avoid key errors

    # firstly N:P ratio is added
    if "N" in dataframe.columns and "P" in dataframe.columns:
        dataframe["N:P"]=dataframe["N"]/dataframe["P"]
    else:
        print("ERROR:3 one of the columns: N,P is not found")

    # then a coordinate transform is performed
    if "LATITUDE" in dataframe.columns and "LONGITUDE" in dataframe.columns:
        # this calculation is present in all steps. So, I made it a variable
        latp = dataframe["LATITUDE"]*(np.pi/180.0)
        longp = dataframe["LONGITUDE"]*(np.pi/180.0)

        # final column computations
        C1 = np.sin(latp)
        C2 = np.sin(longp)*np.cos(latp)
        C3 = -np.cos(longp)*np.cos(latp)

        # assigning values
        dataframe["C1"]=C1
        dataframe["C2"]=C2
        dataframe["C3"]=C3
    else:
        print("ERROR:3 one of the columns: LATITUDE,LONGITUDE is not found")

    