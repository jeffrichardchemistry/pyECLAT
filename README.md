[![DOI](https://zenodo.org/badge/268823869.svg)](https://zenodo.org/badge/latestdoi/268823869) [![PyPI version](https://img.shields.io/pypi/v/pyeclat)](https://pypi.python.org/pypi/pyeclat) [![PyPI Downloads](https://pepy.tech/badge/pyeclat)](https://pepy.tech/project/pyeclat)

# pyECLAT
Unlike the a priori method, the ECLAT method is not based on the calculation of confidence and lift, therefore the ECLAT method is based on the calculation of the support conjunctions of the variables.

pyECLAT is a simple package for associating variables based on the support of the different items of a dataframe.This method returns two dictionaries, one with the frequency of occurrence of the items conjunctions and the other with the support of the items conjunctions.

## Install
<b>Via pip</b>
```
pip3 install pyECLAT
```
<b>Via github</b>
```
git clone https://github.com/jeffrichardchemistry/pyECLAT
cd pyECLAT
python3 setup.py install
```
#### Dependencies
> numpy>=1.17.4, pandas>=0.25.3, tqdm>=4.41.1

## How to use
This package has two dataframes as example, its possible to use:
```
from pyECLAT import Example1, Example2
ex1 = Example1().get()
ex2 = Example2().get()
```
The working dataframe should look like the one below. In this case, each line represents a customer's purchase at a supermarket.

|   | 0      | 1     | 2      | 3      |
|---|--------|-------|--------|--------|
| 0 | milk   | beer  | bread  | butter |
| 1 | coffe  | bread | butter | NaN    |
| 2 | coffe  | bread | butter | NaN    |
| 3 | milk   | coffe | bread  | butter |
| 4 | beer   | NaN   | NaN    | NaN    |
| 5 | butter | NaN   | NaN    | NaN    |
| 6 | bread  | NaN   | NaN    | NaN    |
| 7 | bean   | NaN   | NaN    | NaN    |
| 8 | rice   | bean  | NaN    | NaN    |
| 9 | rice   | NaN   | NaN    | NaN    |

This package works directly with a pandas dataframe without column's name.
<b>Example: Making your dataframe </b>
```
import pandas as pd
dataframe = pd.read_csv('dir/of/file.csv', header=None)  
```
<b>Run ECLAT method:</b>
```
from pyECLAT import ECLAT
eclat_instance = ECLAT(data=dataframe, verbose=True) #verbose=True to see the loading bar
```
After getting <i>eclat_instance</i>, a binary dataframe is automatically generated, among other resources that can be accessed:
```
eclat_instance.df_bin   #generate a binary dataframe, that can be used for other analyzes.
eclat_instance.uniq_    #a list with all the names of the different items

```
eclat_instance.<b>support</b>, eclat_instance.<b>fit</b> and eclat_instance.<b>fit_all</b> are the functions to perform the calculations. Example:
```
get_ECLAT_indexes, get_ECLAT_supports = eclat_instance.fit(min_support=0.08,
                                                           min_combination=1,
                                                           max_combination=3,
                                                           separator=' & ',
                                                           verbose=True)

```
It is possible to access the documentation, as well as the description, of each method using:
```
help(eclat_instance.fit)
help(eclat_instance.fit_all)
help(eclat_instance.support)

```


