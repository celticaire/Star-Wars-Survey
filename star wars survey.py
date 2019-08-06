#!/usr/bin/env python
# coding: utf-8

# # Read data into a pandas dataframe

# In[1]:


import numpy as np
import pandas as pd
star_wars = pd.read_csv("star_wars.csv", encoding="ISO-8859-1")


# # Explore data

# In[2]:


star_wars.head(10)


# In examining the data for strange values, we can see that row 0 is actually a second header row containing the choices for three different multiple choice questions, each of which may or may not contains an answer in each row. Row 2 is missing answers to many of the questions, with NaN in many columns. Household income sometimes has a NaN value. The question asking if the respondent is a Star Wars fan also has a lot of NaN values. 

# In[3]:


star_wars.columns


# # Remove rows where RespondentID is NaN

# In[4]:


star_wars['RespondentID'] = star_wars[pd.notna(star_wars['RespondentID']) == True]


# # Examine columns 1 and 2

# In[5]:


star_wars['Have you seen any of the 6 films in the Star Wars franchise?'].value_counts(dropna=False)


# In[6]:


star_wars['Do you consider yourself to be a fan of the Star Wars film franchise?'].value_counts(dropna=False)


# There are lots of NaN values in the 'Do you consider yourself to be a fan of the Star Wars film franchise?' column.

# # Convert both columns to Booleans to make them easier to work with

# In[7]:


# mapping dictionary
yes_no = {
    "Yes": True,
    "No": False
}

#convert both columns by applying dictionary
star_wars['Have you seen any of the 6 films in the Star Wars franchise?'] = star_wars['Have you seen any of the 6 films in the Star Wars franchise?'].map(yes_no)
star_wars['Do you consider yourself to be a fan of the Star Wars film franchise?'] = star_wars['Do you consider yourself to be a fan of the Star Wars film franchise?'].map(yes_no)


# In[8]:


star_wars['Have you seen any of the 6 films in the Star Wars franchise?'].value_counts(dropna=False)


# In[9]:


star_wars['Do you consider yourself to be a fan of the Star Wars film franchise?'].value_counts(dropna=False)


# # Re-name the next 6 columns for easier analysis

# In[10]:


# These columns are star_wars.columns[3:9]
# Convert values to Booleans

dict = {'Star Wars: Episode I  The Phantom Menace': True, 
        'Star Wars: Episode II  Attack of the Clones': True, 
        'Star Wars: Episode III  Revenge of the Sith': True, 
        'Star Wars: Episode IV  A New Hope': True, 
        'Star Wars: Episode V The Empire Strikes Back': True, 
        'Star Wars: Episode VI Return of the Jedi': True, 
        np.NaN: False}
star_wars['Which of the following Star Wars films have you seen? Please select all that apply.'] = star_wars['Which of the following Star Wars films have you seen? Please select all that apply.'].map(dict)
star_wars['Unnamed: 4'] = star_wars['Unnamed: 4'].map(dict)
star_wars['Unnamed: 5'] = star_wars['Unnamed: 5'].map(dict)
star_wars['Unnamed: 6'] = star_wars['Unnamed: 6'].map(dict)
star_wars['Unnamed: 7'] = star_wars['Unnamed: 7'].map(dict)
star_wars['Unnamed: 8'] = star_wars['Unnamed: 8'].map(dict)


# In[11]:


# check the columns to make sure the conversion worked
star_wars['Which of the following Star Wars films have you seen? Please select all that apply.'].value_counts(dropna=False)


# In[12]:


# Rename the columns to something more user-friendly

star_wars = star_wars.rename(columns={'Which of the following Star Wars films have you seen? Please select all that apply.': 'seen_1',
                                     'Unnamed: 4': 'seen_2',
                                     'Unnamed: 5': 'seen_3',
                                     'Unnamed: 6': 'seen_4',
                                     'Unnamed: 7': 'seen_5',
                                     'Unnamed: 8': 'seen_6'})


# In[13]:


# double-check column names

print(star_wars.columns)


# # Clean up Star Wars Movie Ranking Columns

# In[14]:


# Re-name ranking columns

star_wars = star_wars.rename(columns={'Please rank the Star Wars films in order of preference with 1 being your favorite film in the franchise and 6 being your least favorite film.': 'ranking_1',
                                     'Unnamed: 10': 'ranking_2',
                                     'Unnamed: 11': 'ranking_3',
                                     'Unnamed: 12': 'ranking_4',
                                     'Unnamed: 13': 'ranking_5',
                                     'Unnamed: 14': 'ranking_6'})


# In[15]:


# Double check renamed columns

print(star_wars.columns[9:15])


# In[16]:


# Convert columns to floats so they can be manipulated later

star_wars.iloc[1:, 9:15] = star_wars.iloc[1:, 9:15].astype('float')
star_wars.iloc[1:, 9:15]


# # Find highest ranked movie by taking mean of each column

# In[17]:


ranking_mean = star_wars.iloc[1:, 9:15].mean()
ranking_mean.head


# In[18]:


get_ipython().magic('matplotlib inline')
import matplotlib.pyplot as plt


# In[19]:


plt.bar(height=ranking_mean, left=range(6), y=0, align='center')
plt.show


# In examining the mean score for each of the 6 Star Wars movies, where 1 is the best score and 5 the worst, it becomes apparent that Movie 5, The Empire Strikes Back, is the overall favorite of the survey respondents.

# # Find out how many people have seen each movie by taking the sum of each 'seen' column

# In[20]:


def sum_seen(col):
    sum = col.sum()
    return sum
seen_sums = star_wars.iloc[1:, 3:9].apply(sum_seen)


# In[21]:


seen_sums


# In[22]:


plt.bar(height=seen_sums, left=range(6), y=0, align='center')
plt.show                         


# Analysis of the number of respondents that had seen each movie shows that The Emperor Strikes Back and Return of the Jedi were the top two movies seen, with The Phantom Menace coming in at third place.

# ## Examine how men responded vs. women

# In[23]:


# Split data into two groups, male and female

males = star_wars[star_wars["Gender"] == "Male"]
females = star_wars[star_wars["Gender"] == "Female"]


# In[28]:


# Analyze mean score and total movies watched for males

male_rankings = males.iloc[1:, 9:15].mean()
male_sums = males.iloc[1:, 3:9].apply(sum_seen)

# visualize male average rank
plt.bar(height=male_rankings, left=range(6), y=0, align='center')
plt.show 


# In[29]:


# visualize male total seen per movie
plt.bar(height=male_sums, left=range(6), y=0, align='center')
plt.show 


# Men rated The Phantom Menace, Attack of the Clones, and Revenge of the Sith the highest. However, when looking at the totals who had seen each movie, the movies that were viewed the most were The Empire Strikes Back, Return of the Jedi, and The Phantom Menace. So more men viewed the classic movies, but they did not rate them as well as the newer trilogy.

# In[30]:


# Analyze mean score and total movies watched for females

female_rankings = females.iloc[1:, 9:15].mean()
female_sums = females.iloc[1:, 3:9].apply(sum_seen)

#visualize female rankings
plt.bar(height=female_rankings, left=range(6), y=0, align='center')
plt.show 


# In[31]:


# visualize female total seen per movie
plt.bar(height=female_sums, left=range(6), y=0, align='center')
plt.show 


# Examination of female rankings and sum total seen per movie, the same trend emerges. Females ranked The Phantom Menace, Attack of the Clones, and Revenge of the Sith the highest, taking the first three places in the rankings. However, they also had seen the same three movies the most: The Phantom Menace, The Empire Strikes Back, and Return of the Jedi.

# In[ ]:




