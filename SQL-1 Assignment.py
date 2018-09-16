
# coding: utf-8

# In[1]:


# read the following data set
#https://archive.ics.uci.edu/ml/machine-learning-databases/adult/
# rename the columns as per the description from this file
#https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.names


# In[2]:


import numpy as np
import pandas as pd
from pandas import DataFrame, Series
import sqlite3 as db


# In[5]:


url = "https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data"
col_list = ['age','workclass','fnlwgt','education','education-num','marital-status','occupation',
           'relationship','race','sex','capital-gain','capital-loss','hours-per-week','native-country','Label']
adult = pd.read_csv(url,sep=",",delimiter=",",names=col_list,skipinitialspace=True)
sqladb = adult.copy()


# In[6]:


print(sqladb.columns)

import re
sqladb.columns = [re.sub("[-]", "_", col) for col in adult.columns]

print(sqladb.columns)


# In[7]:


print(sqladb.education.unique())
print(sqladb.workclass.unique())
print(sqladb.relationship.unique())
print(sqladb.sex.unique())
print(sqladb.marital_status.unique())
print(sqladb.race.unique())


# In[8]:


sqladb.head()


# In[9]:


sqladb.shape


# In[10]:


sqladb.describe()


# In[11]:


from pandasql import sqldf
pysqldf = lambda q: sqldf(q, globals())


# In[12]:


#  Select 10 records from the adult sqladb

pysqldf("SELECT * FROM sqladb LIMIT 10;")


# In[14]:


# Show me the average hours per week of all men who are working in private sector

q = """ select sex,workclass,avg(hours_per_week) from sqladb where sex ='Male' and workclass ='Private' group by sex ; """

pysqldf(q)


# In[15]:


# Show me the frequency table for education, occupation and relationship, separately

q = """ select education,count(education) as frequency from sqladb group by education ; """

pysqldf(q)


# In[16]:


q = """ select occupation,count(occupation) as Frequency from sqladb group by occupation ; """

pysqldf(q)


# In[17]:


q = """ select relationship,count(relationship) as Frequency from sqladb group by relationship ; """

pysqldf(q)


# In[20]:


# Are there any people who are married, working in private sector and having a masters degree

q = """ 
 select count(*) as count_of_people from sqladb WHERE marital_status != 'Never-married' and education = 'Masters' and workclass = 'Private';
"""
pysqldf(q)


# In[21]:


# What is the average, minimum and maximum age group for people working in different sectors

q = """
    select avg(age),max(age),min(age),workclass from sqladb group by workclass ;
"""

pysqldf(q)


# In[22]:


# Calculate age distribution by country

q = """
    select native_country, max(age),min(age),avg(age) from sqladb group by native_country ;
"""  

pysqldf(q)


# In[23]:


# Compute a new column as 'Net-Capital-Gain' from the two columns 'capital-gain' and 'capital-loss'

q = """
    select (capital_gain - capital_loss) as Net_Capital_Gain from sqladb;
"""
pysqldf(q)

