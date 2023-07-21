#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 


# In[4]:


data=pd.read_csv("housing_1.csv")


# In[5]:


data


# In[6]:


data.info()


# In[7]:


data.dropna(inplace=True)


# In[8]:


data.info()


# In[9]:


from sklearn.model_selection import train_test_split
x=data.drop(['median_house_value'],axis=1)
y=data['median_house_value']


# In[10]:


x


# In[11]:


y


# In[13]:


x_train, x_test, y_train, y_test= train_test_split(x,y,test_size=0.3)


# In[15]:


train_data=x_train.join(y_train)


# In[16]:


train_data


# In[17]:


train_data.hist()


# In[21]:


sns.heatmap(train_data.corr(),annot=True,cmap='YlGnBu')


# In[23]:


train_data['total_rooms']=np.log(train_data['total_rooms']+1)
train_data['total_bedrooms']=np.log(train_data['total_bedrooms']+1)
train_data['population']=np.log(train_data['population']+1)
train_data['households']=np.log(train_data['households']+1)


# In[24]:


train_data.hist()


# In[26]:


train_data=train_data.join(pd.get_dummies(train_data.ocean_proximity)).drop(['ocean_proximity'],axis=1)


# In[27]:


train_data


# In[28]:


sns.heatmap(train_data.corr(),annot=True,cmap='YlGnBu')


# In[30]:


sns.scatterplot(x='latitude',y='longitude',data=train_data,hue="median_house_value",palette="coolwarm")


# In[31]:


train_data['bedroom_ratio']=train_data['total_bedrooms']/train_data['total_rooms']
train_data['household_rooms']=train_data['total_rooms']/train_data['households']


# In[35]:


sns.heatmap(train_data.corr(),annot=True,cmap='YlGnBu')


# In[43]:


from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
scaler=StandardScaler()
x_train,y_train=train_data.drop(['median_house_value'],axis=1),train_data['median_house_value']
x_train_s=scaler.fit_transform(x_train)
reg=LinearRegression()
reg.fit(x_train_s,y_train)


# In[37]:


test_data=x_test.join(y_test)

test_data['total_rooms']=np.log(test_data['total_rooms']+1)
test_data['total_bedrooms']=np.log(test_data['total_bedrooms']+1)
test_data['population']=np.log(test_data['population']+1)
test_data['households']=np.log(test_data['households']+1)

test_data=test_data.join(pd.get_dummies(test_data.ocean_proximity)).drop(['ocean_proximity'],axis=1)

test_data['bedroom_ratio']=test_data['total_bedrooms']/test_data['total_rooms']
test_data['household_rooms']=test_data['total_rooms']/test_data['households']


# In[41]:


x_test,y_test=test_data.drop(['median_house_value'],axis=1),test_data['median_house_value']


# In[44]:


x_test_s=scaler.transform(x_test)


# In[45]:


reg.score(x_test_s, y_test)


# In[48]:


from sklearn.ensemble import RandomForestRegressor
forest= RandomForestRegressor()
forest.fit(x_train_s,y_train)


# In[49]:


forest.score(x_test_s,y_test)


# In[56]:


from sklearn.model_selection import GridSearchCV
forest=RandomForestRegressor()
param_grid={
    "n_estimators":[100,200,300],
    "min_samples_split":[2,4],
    "max_depth":[None,4,8]
}
grid_search=GridSearchCV(forest,param_grid,cv=5,
                        scoring="neg_mean_squared_error",
                        return_train_score=True)
grid_search.fit(x_train_s,y_train)


# In[57]:


grid_search.best_estimator_


# In[58]:


grid_search.best_estimator_.score(x_test_s,y_test)


# In[ ]:




