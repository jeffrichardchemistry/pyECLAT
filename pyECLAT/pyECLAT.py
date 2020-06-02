# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from tqdm import tqdm
import itertools

class Example1:        
    def get(self):
	    df = pd.read_csv('https://raw.githubusercontent.com/jeffrichardchemistry/pyECLAT/master/data/base1.csv', header=None)
	    return df			

class Example2:
    def get(self):
        df = pd.read_csv('https://raw.githubusercontent.com/jeffrichardchemistry/pyECLAT/master/data/base2.csv', header=None)
        return df
        

class ECLAT():
    """
    
    Arguments
    ---------------------
    data
        The `data` is a pandas dataframe format. The data should look like the example below.
        In this case, each line represents the purchase of one person.
            >>> Example of data format
            	0	1	2	3
            0	milk	beer	bread	butter
            1	coffe	bread	butter	NaN
            2	coffe	bread	butter	NaN
            3	milk	coffe	bread	butter
            4	beer	NaN	NaN	NaN
            5	butter	NaN	NaN	NaN
            6	bread	NaN	NaN	NaN
            7	bean	NaN	NaN	NaN
            8	rice	bean	NaN	NaN
            9	rice	NaN	NaN	NaN
        
        After get a ECLAT class instance, a binary dataframe is created,
        in which the column names are the product names. 0 = 'No' 1 = 'Yes' for a transaction that occurred.
            >>> eclat_instance = ECLAT(df=data)
                eclat_instance.df_bin
            	bean	beer	bread	butter	milk	rice	coffe
            0	0	1	1	1	1	0	0
            1	0	0	1	1	0	0	1
            2	0	0	1	1	0	0	1
            3	0	0	1	1	1	0	1
            4	0	1	0	0	0	0	0
            5	0	0	0	1	0	0	0
            6	0	0	1	0	0	0	0
            7	1	0	0	0	0	0	0
            8	1	0	0	0	0	1	0
            9	0	0	0	0	0	1	0
    verbose
        Show a progress bar in three steps.
    """
    
    def __init__(self, data, verbose=False):
        self.data = data
        self.uniq_ = []
        ECLAT._getUnique(self)
        if verbose:
            self.df_bin = ECLAT._makeTable(self, verbose=True)
        else:
            self.df_bin = ECLAT._makeTable(self, verbose=False)            
    
            
    def _getUnique(self):
        # Return a list with unique names of features
        dif_atrib = []
        n_columns = len(self.data.columns)
        for column in range(n_columns):
            dif_atrib.extend(list(self.data.iloc[:, column].unique()))
        
        self.uniq_ = list(set(dif_atrib))
    
    def _makeTable(self, verbose=False):
        """
        Remove nan and return a binary table with name of products how column names. 0 = 'No' 1 = 'Yes'
        
        """
        
        columns_table = self.uniq_ 
        if np.nan in columns_table:
            columns_table.remove(np.nan)
        elif 'nan' in columns_table:
            columns_table.remove('nan')
        elif 'NaN' in columns_table:
            columns_table.remove('NaN')
        ECLAT._getUnique(self) #don't modify uniq_
        
        dict_index = {}
        lst_index = []
        if verbose:
            for column in tqdm(columns_table):
                for i in range(len(self.data.columns)):
                    lst_index.extend(list(self.data.loc[self.data[i] == column].index.values))
                    if i == len(self.data.columns) - 1 :
                        dict_index[column] = list(set(lst_index))
                        lst_index = []
        else:
            for column in columns_table:
                for i in range(len(self.data.columns)):
                    lst_index.extend(list(self.data.loc[self.data[i] == column].index.values))
                    if i == len(self.data.columns) - 1 :
                        dict_index[column] = list(set(lst_index))
                        lst_index = []
        
        data_init = {}
        
        if verbose:
            for i in tqdm(columns_table):
                data_init[i] = [0 for i in range(len(self.data))]
        else:
            for i in columns_table:
                data_init[i] = [0 for i in range(len(self.data))]
            
        df_table = pd.DataFrame(data_init)
        
        if verbose:
            for name_column in tqdm(columns_table):
                df_table.loc[dict_index[name_column], name_column] = 1
        else:
            for name_column in columns_table:
                df_table.loc[dict_index[name_column], name_column] = 1
        
        return df_table
        
    def support(self, min_support=None):
        """
        Return a dictionary. The key is the feature and value is support
        
        Arguments
        ---------------------
        min_support
            Must be 'None' to return all features and supports or 'Float' to filter features by support
        """
        column_names = self.df_bin.columns.values
        support = {}
        support_min = {}
        total = len(self.df_bin)
        if min_support == None:
            for column in column_names:
                numerator = self.df_bin.loc[self.df_bin[column] != 0, column].sum()
                support[column] = numerator / total
            return support
        
        else:
            min_support = float(min_support)
            
            for column in column_names:
                numerator = self.df_bin.loc[self.df_bin[column] != 0, column].sum()
                support[column] = numerator / total
            
            for key, value in support.items():
                if value >= min_support:
                    support_min[key] = value
                    
            return support_min                    
    
    def _makeQuery(self, lst=[]):
        str_query = ''
        for item in lst:
            if item == lst[-1]:
                str_query = ''.join(str_query+'`{}` == 1'.format(item))
                break
            str_query = ''.join(str_query+'`{}` == 1 and '.format(item))
        return (str_query)
                        
    def fit_all(self, min_support=0.08, separator=' & ', verbose=False, min_combination=1):
        """
        Return a dictionary. The key is the feature and value is support.
        This algorithm works with all possible permutations (without repetitions)
        until the all supports = 0.
        
        Arguments
        ---------------------
        min_support
            Must be 'None' to return all features and supports or 'Float' to filter features by support
        separator
            Separator for the output dictionary key. Just to organize. default = ' & '
        verbose
            `True` to enables the loading bar.
        """
        if min_support == None:
            min_support = 0
            
        support_dict = ECLAT.support(self, min_support=min_support)
        
        total = len(self.data)
        dict_finally_support = {}
        dict_finally_index = {}
        test_support = []
        if verbose:
            #permute the features by number of total features
            for j in range(min_combination, len(self.df_bin.columns) + 1):
                print('Combination {} by {}'.format(j, j))
                          
                for i in tqdm(itertools.combinations(support_dict.keys(), r=j)): #permutation
                    get_query = ECLAT._makeQuery(self, list(i)) #get string with conditional for query pandas
                    
                    try:
                        numerator = len(self.df_bin.query('{}'.format(get_query)).loc[:, list(i)])
                    except:
                        continue
                    #calc support
                    support = numerator / total
                    test_support.append(support)
                    
                    #Filter features < min_support
                    if support < min_support:
                        continue
                    
                    #create dictionary with answers
                    dict_finally_support[separator.join(list(i))] = support
                    dict_finally_index[separator.join(list(i))] = list(self.df_bin.query('{}'.format(get_query)).loc[:, list(i)].index)
                
                #Stop when all supports = 0
                if test_support.count(0) == len(test_support):
                    print('Stopping in combination {} by {}. All supports = 0.'.format(j, j))
                    break
                test_support = []
            return dict_finally_index, dict_finally_support
        
        else:
            for j in range(2, len(self.df_bin.columns) + 1):
                for i in itertools.combinations(support_dict.keys(), r=j):
                    get_query = ECLAT._makeQuery(self, list(i))
                    try:
                        numerator = len(self.df_bin.query('{}'.format(get_query)).loc[:, list(i)])
                    except:
                        continue
                    support = numerator / total
                    
                    if support < min_support:
                        continue
                    
                    dict_finally_support[separator.join(list(i))] = support
                    dict_finally_index[separator.join(list(i))] = list(self.df_bin.query('{}'.format(get_query)).loc[:, list(i)].index)
                
                if test_support.count(0) == len(test_support):
                    break
                test_support = []
            return dict_finally_index, dict_finally_support
        
    def fit(self, min_support=0.08, min_combination = 1, max_combination = 3,separator=' & ', verbose=True):
        """
        Return a dictionary. The key is the feature and value is support. A high number of 
        combinations (greater than three) can take a long time to finish. 
        
        
        Arguments
        ---------------------
        min_support
            Must be 'None' to return all features and supports or 'Float' to filter features by support
        min_combination
            Minimal combination of attributes
        max_combination
            Maximum combination of attributes
        separator
            Separator for the output dictionary key. Just to organize. default = ' & '
        verbose
            `True` to enable the loading bar.
        """
        
        if min_support == None:
            min_support = 0
            
        support_dict = ECLAT.support(self, min_support=min_support)
        
        total = len(self.data)
        dict_finally_support = {}
        dict_finally_index = {}
        if verbose:
            for j in range(min_combination, max_combination + 1): #min_combination until max combination
                print('Combination {} by {}'.format(j, j))
                for i in tqdm(itertools.combinations(support_dict.keys(), r=j)):                    
                    get_query = ECLAT._makeQuery(self, list(i))
                    
                    try:
                        numerator = len(self.df_bin.query('{}'.format(get_query)).loc[:, list(i)])
                    except:
                        continue
                    support = numerator / total
                    
                    if support < min_support:
                        continue
                    
                    dict_finally_support[separator.join(list(i))] = support
                    dict_finally_index[separator.join(list(i))] = list(self.df_bin.query('{}'.format(get_query)).loc[:, list(i)].index)
            
            
            return dict_finally_index,dict_finally_support
        
        else:
            for j in range(min_combination, max_combination + 1):
                for i in itertools.combinations(support_dict.keys(), r=j):
                    get_query = ECLAT._makeQuery(self, list(i))
                    
                    try:
                        numerator = len(self.df_bin.query('{}'.format(get_query)).loc[:, list(i)])
                    except:
                        continue
                    support = numerator / total
                    
                    if support < min_support:
                        continue
                    
                    dict_finally_support[separator.join(list(i))] = support
                    dict_finally_index[separator.join(list(i))] = list(self.df_bin.query('{}'.format(get_query)).loc[:, list(i)].index)
                               
                
            return dict_finally_index, dict_finally_support
