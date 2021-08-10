# -*- coding: utf-8 -*-
'''
Spyder Editor

This is a temporary script file.
'''


import pandas as pd
import numpy as ny

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
   
# limits data we are looking at to only include current_drinkers and individuals with abuse, dependence or both in last 12, remove S2AQ8A 99=unknown
sub1=data [(data['CONSUMER']!=3) & (data['ALCABDEPP12DX']!=0) & (data['ALCABDEP12DX']!=0) & (data['S2AQ8A']!='99') & (data['S2AQ8B']!=99)] 

# makes copy of data set sub2 is what we use to reference now
sub2=sub1.copy() 

#convert to numeric after removing non-numeric response which was blank
sub2['S2AQ8A'] = pd.to_numeric(sub2['S2AQ8A'])
sub2['S2AQ8B'] = pd.to_numeric(sub2['S2AQ8B'])

# remove 99 S1Q1E
sub2['S1Q1E'] = sub2['S1Q1E'].replace(99, ny.nan)

# remove 99 S2AQ8B
sub2['S2AQ8B'] = sub2['S2AQ8B'].replace(99, ny.nan)

#change S2AQ8A to reflect drinks per year
recode1 = {1: 365, 2: 286, 3: 104, 4: 52, 5: 52, 6: 30, 7: 12, 8: 9, 9: 4.5, 10: 1.5,}
sub2['DRINKSPERYEAR']= sub2['S2AQ8A'].map(recode1)

print('counts for DRINKSPERYEAR')
c1 = sub2['DRINKSPERYEAR'].value_counts(sort=False)
print(c1)

print('percentages for DRINKSPERYEAR')
p1 = sub2['DRINKSPERYEAR'].value_counts(sort=False, normalize=True)
print(p1)

#estimating drinks per year by multiplying drinks per year * # drinks when consumed alcohol
sub2['NUMDRINKYEAR_EST'] = sub2['DRINKSPERYEAR'] * sub2['S2AQ8B']

print('counts for NUMDRINKYEAR_EST')
c2 = sub2['NUMDRINKYEAR_EST'].value_counts(sort=False)
print(c2)

print('percentages for NUMDRINKYEAR_EST')
p2 = sub2['NUMDRINKYEAR_EST'].value_counts(sort=False, normalize=True)
print(p2)

#changing schooling level to represent did not finish highschool, did not finish college, finished college, finished professional degree
sub2['SCHOOLING_LEVEL'] = pd.cut(sub2.S1Q6A, [0, 7, 10, 13, 14])
print (pd.crosstab(sub2['SCHOOLING_LEVEL'], sub2['S1Q6A']))

print('counts for SCHOOLING_LEVEL')
c3 = sub2['SCHOOLING_LEVEL'].value_counts(sort=False)
print(c3)

print('percentages for SCHOOLING_LEVEL')
p3 = sub2['SCHOOLING_LEVEL'].value_counts(sort=False, normalize=True)
print(p3)

sub2['SCHOOLING_LEVEL'] = pd.cut(sub2.S1Q6A, [0, 7, 10, 13, 14])
print (pd.crosstab(sub2['SCHOOLING_LEVEL'], sub2['S1Q6A']))

#new data subset to display only intended variables
sub3=sub2[['IDNUM','S1Q6A','SCHOOLING_LEVEL', 'S1Q1E', 'ALCABDEP12DX', 'ALCABDEPP12DX','DRINKSPERYEAR', 'S2AQ8B', 'NUMDRINKYEAR_EST']]
print(sub3.head(25))