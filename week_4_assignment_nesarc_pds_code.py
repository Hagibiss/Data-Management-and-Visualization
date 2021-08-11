# -*- coding: utf-8 -*-
'''
Spyder Editor

This is a temporary script file.
'''


import pandas as pd
import numpy as ny
import seaborn as sb
import matplotlib.pyplot as plt

data = pd.read_csv('nesarc_pds.csv', low_memory=(False))
#data = import data set, improve program efficiency

#uper-case all DataFrame column names
data.columns = map(str.upper, data.columns)

#set PANDAS to show all columns in DataFrame
pd.set_option('display.max_columns', None)

#set PANDAS to show all rows in DataFrame
pd.set_option('display.max_rows', None)

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

#estimating drinks per year by multiplying drinks per year * # drinks when consumed alcohol
sub2['NUMDRINKYEAR_EST'] = sub2['DRINKSPERYEAR'] * sub2['S2AQ8B']

#changing schooling level to represent did not finish highschool, did not finish college, finished college, finished professional degree
sub2['SCHOOLING_LEVEL'] = pd.cut(sub2.S1Q6A, [0, 7, 10, 13, 14])
print (pd.crosstab(sub2['SCHOOLING_LEVEL'], sub2['S1Q6A']))

sub2['SCHOOLING_LEVEL']=sub2['SCHOOLING_LEVEL'].cat.rename_categories(['DNC Highschool', 'DNC College', 'CMPLT College', 'CMPLT Professional Degree'])

sub2['ETHRACE2A']=sub2['ETHRACE2A'].astype('category')

sub2['ETHRACE2A']=sub2['ETHRACE2A'].cat.rename_categories(['White', 'Black', 'NatAm', 'Asian', 'Latino'])

print('counts for ETHRACE2A')
c1 = sub2['ETHRACE2A'].value_counts(sort=False)
print(c1)

print('percentages for ETHRACE2A')
p1 = sub2['ETHRACE2A'].value_counts(sort=False, normalize=True)
print(p1)

#new data subset to display only intended variables
sub3=sub2[['IDNUM','S1Q6A','SCHOOLING_LEVEL', 'ETHRACE2A', 'DRINKSPERYEAR', 'S2AQ8B', 'NUMDRINKYEAR_EST', 'LIQRECF']]

#Bar chart for highest grade or year of school completed
sb.countplot(x='S1Q6A', data=sub3)
plt.xlabel('Highest Grade or Year of School Completed')
plt.title('An Analysis of the Influence of Education Level on Alcohol Abuse or Dependence and the Impact of Education Level')

#Univariate histogram for quantitative variable
sb.displot(sub3['NUMDRINKYEAR_EST'].dropna(), kde=False)
plt.xlabel('Number of Drinks Per Year')
plt.title('An Analysis of the Influence of Education Level on Alcohol Abuse or Dependence - Estimated Number of Drinks Per Year')

#standard deviation and other descriptive statistics for quantitative variables
print('describe number of drinks per year')
desc1 = sub3 ['NUMDRINKYEAR_EST'].describe()
print(desc1)

c2 = sub3.groupby('SCHOOLING_LEVEL').size()
print(c2)

sb.catplot(x='SCHOOLING_LEVEL', y='NUMDRINKYEAR_EST', data=sub3, kind='bar', ci=None)
plt.xlabel('Highest Level of School')
plt.ylabel('Proportion of Drinks Per Year')
plt.title('An Analysis of the Influence of Education Level on Alcohol Abuse or Dependence')

sb.catplot(x='SCHOOLING_LEVEL', y='NUMDRINKYEAR_EST', hue='ETHRACE2A', data=sub3, kind='bar', ci=None)
plt.xlabel('Highest Level of School')
plt.ylabel('Proportion of Drinks Per Year')
plt.title('An Analysis of the Influence of Education Level on Alcohol Abuse or Dependence - A Comparison by Ethnicity')


