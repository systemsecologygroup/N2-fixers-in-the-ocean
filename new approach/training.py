'''
TRAINING.PY

This file stores the scalers, transformers used for training the models and functions assoicated with them
'''

class SimpleTransformer():
    '''
    Simple transformer class used for training the model. Applies mathematical functions to transform the dataset.

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
        print("")

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
        print("")

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