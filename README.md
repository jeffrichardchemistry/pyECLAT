# pyECLAT
Unlike the a priori method, the ECLAT method is not based on the calculation of confidence and lift, therefore the ECLAT method is based on the calculation of the support together of the variables.

pyECLAT is a simple package for associating variables based on the support of the different items, together, of a dataframe.

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
This package has two dataframes as an example
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

