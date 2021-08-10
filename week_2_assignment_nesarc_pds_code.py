# -*- coding: utf-8 -*-
'''
Spyder Editor

This is a temporary script file.
'''


import pandas as pd
import numpy

data = pd.read_csv('nesarc_pds.csv', low_memory=(False))
#data = import data set, improve program efficiency

#uper-case all DataFrame column names
data.columns = map(str.upper, data.columns)

#bug fix for display formats to avoid run time errors
pd.set_option('display.float_format', lambda x:'%f'%x)

#ensure each of these columns are numeric
data['CONSUMER'] = pd.to_numeric(data['CONSUMER'])
data['ALCABDEP12DX'] = pd.to_numeric(data['ALCABDEP12DX'])
data['ALCABDEPP12DX'] = pd.to_numeric(data['ALCABDEPP12DX'])
data['S1Q6A'] = pd.to_numeric(data['S1Q6A'])
data['AGE'] = pd.to_numeric(data['AGE'])
data['S1Q1E'] = pd.to_numeric(data['S1Q1E'])

#data refers to data frame indicated in line 12 of intial read in
print(len(data)) #number of observations (rows)
print(len(data.columns)) #number of variables (columns)

# Another option for displaying Observations or rows in a DataFrame is
print(len(data.index))

# to check format of your variables you use the below string
# data['VARIABLE_NAME'].dtype - output is recorded in console int64 is numeric

# to change variable 
# data['VARIABLE_NAME'] = pandas.to.numeric(data['VARIABLE_NAME'])

ct1 = data.groupby('ALCABDEP12DX').size() # group by ALCABDEP12DX count
print(ct1)

pt1 = data.groupby('ALCABDEP12DX').size() * 100 / len(data) # group by ALCABDEP12DX percentage
print(pt1)    

sub1=data [(data['CONSUMER']!=3) & (data['ALCABDEPP12DX']!=0) & (data['ALCABDEP12DX']!=0)] # limits data we are looking at to only include current_drinkers and individuals with abuse, dependence or both in last 12 

sub2=sub1.copy() # makes copy of data set sub2 is what we use to reference now

print('counts for ALCABDEP12DX')
c1 = sub2['ALCABDEP12DX'].value_counts(sort=False)
print(c1)

print('percentages for ALCABDEP12DX')
p1 = sub2['ALCABDEP12DX'].value_counts(sort=False, normalize=True)
print(p1)
 
print('counts for ALCABDEPP12DX')
c2 = sub2['ALCABDEPP12DX'].value_counts(sort=False)
print(c2)

print('percentages for ALCABDEPP12DX')
p2 = sub2['ALCABDEPP12DX'].value_counts(sort=False, normalize=True)
print(p2)  

print('counts for S1Q6A')
c3 = sub2['S1Q6A'].value_counts(sort=False)
print(c3)

print('percentages for S1Q6A')
p3= sub2['S1Q6A'].value_counts(sort=False, normalize=True)
print(p3)

print('counts for AGE')
c9 = sub2['AGE'].value_counts(sort=False)
print(c9)

print('percentages for AGE')
p9 = sub2['AGE'].value_counts(sort=False, normalize=True)
print(p9)

print('counts for S1Q1E')
c10 = sub2['S1Q1E'].value_counts(sort=False)
print(c10)

print('percentages for S1Q1E')
p10 = sub2['S1Q1E'].value_counts(sort=False, normalize=True)
print(p10)