#!/usr/bin/env python
# coding: utf-8

# # Data analysis of  "Events with two electrons from 2010" dataset from CERN Open Data
# 
# This data set has data associated with events with two electrons from particle physics experiment at CERN in 2010. Read more at: https://opendata.cern.ch/record/304
# 
# I will analyze this dataset.

# ## Data Preparation and Cleaning
# 
# Let's inspect data a little bit by .info() and .describe()
# 

# In[4]:


import pandas as pd


# In[5]:


electron_df = pd.read_csv('dielectron.csv')


# In[6]:


electron_df


# In[7]:


electron_df.info()


# In[8]:


electron_df.describe()


# In[9]:


electron_df.sort_values(by='M')[99900:99920]


# As you can see there are 85 values that are NaN for the M column, which is the invariant mass for two electrons. Let's delete those rows to have a absolutely complete dataset.

# In[10]:


electron_df[electron_df.M.notnull()]


# In[11]:


electron_df = electron_df[electron_df.M.notnull()]


# In[12]:


electron_df.info()


# We get the new data frame without any NaN index. 

# ## Exploratory Analysis and Visualization
# 
# Let's try to plot some graphs and see how to interpret them. 
# 

# Let's begin by importing`matplotlib.pyplot`, `seaborn` and `numpy`. And store electron_df in a variable called data.

# In[98]:


import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
get_ipython().run_line_magic('matplotlib', 'inline')

sns.set_style('darkgrid')
matplotlib.rcParams['font.size'] = 14
matplotlib.rcParams['figure.figsize'] = (9, 5)
matplotlib.rcParams['figure.facecolor'] = '#00000000'

data=electron_df


# **Scatter Plot of Energies of Two Electrons**

# In[79]:


sns.scatterplot(x=data.E1, y=data.E2);
plt.title("Total energy of electron 1 vs Total energy of electron 2")


# Above you can see the scatter plot showing the energy of the electron 1 versus the energy of the electron 2. As you can see (almost) all the data points are contained in the area enclosed by the line (y = 100 - x). This means that there is a limit of what can be the total energy. This is expected because our beam has a certain energy. So then, what happens to the beam energy for the cases that are very near to the origin, i.e., that have a small total energy? Of course, the only products are not these electrons. For different events we have many different products besides these two electrons. So, "lacking" energy is the energy associated with them.

# **Scatter Plots of Total Energy versus Angles for Each Electron**

# In[80]:


fig, axes = plt.subplots(2, 2, figsize=(32, 16))

sns.scatterplot(x=data.eta1, y=data.E1, ax=axes[0, 0])
axes[0,0].set_title("The pseudorapidity of the electron 1 vs Total energy of electron 1")
sns.scatterplot(x=data.phi1, y=data.E1, ax=axes[0, 1])
axes[0,1].set_title("The phi angle of the electron 1 vs Total energy of electron 1")

sns.scatterplot(x=data.eta2, y=data.E2, ax=axes[1, 0])
axes[1,0].set_title("The pseudorapidity of the electron 2 vs Total energy of electron 2")
sns.scatterplot(x=data.phi2, y=data.E2, ax=axes[1, 1])
axes[1,1].set_title("The phi angle of the electron 2 vs Total energy of electron 2")


# Above we have 4 plots. The first row is associated with electron 1 while the second row is associated with electron 2. The plots at the left show the relation between the energy and the pseudorapidity. The plots at the right show the relation between the energy and the phi angle. We see that energy is higher at higher pseudorapidity values. (Minus 2 is high in this sense. Because the minus sign just refers to the other side of the detector. 0 is the smallest value for pseudorapidity.) This is expected because high energy particles are the ones that have high pseudorapidity values. On the other hand, we have a uniform distribution for phi dependence. This is also expected because the 

# **Scatter plot of pseudorapidity of electron 1 and z component of the momentum of electron 1**

# In[20]:


sns.scatterplot(x=data.eta1, y=data.pz1)


# **Scatter plot of pseudorapidity of electron 1 and x component of the momentum of electron 1**

# In[21]:


sns.scatterplot(x=data.eta1, y=data.px1)


# Above we see plots of eta1 versus pz1 and px1, respectively. It is obvious that there is a correlation between eta1 and pz1 but there seems no correlation between eta1 and px1.

# **Histogram of eta1

# In[103]:


plt.hist(data.eta1, bins=np.arange(-4, 4, 0.05));
plt.title("eta1 histogram");
plt.xlabel("eta1 value");
plt.ylabel("Number of events");


# In[106]:


plt.hist([data.eta1, data.eta2], bins=np.arange(-4, 4, 0.3));
plt.legend(['eta1', 'eta2']);
plt.xlabel("eta values");
plt.ylabel("# of events");
plt.title("eta1 and eta2 histogram combined");


# Above we first see a histogram of eta1 values. It seems there is something about eta1 values around 1.5 and -1.5. You see that the number of events around those values are a bit lower, and peaks are around 2.1 and -2.1.  
# Secondly, we see a histogram that combines eta1 and eta2. Here we see that eta 2 makes peaks around 2.2 and -2.2 and these peaks are much more sharper than the peaks of eta1.  
# Notice that, both eta1 and eta2 are symmetric around 0.

# ## Asking and Answering Questions
# 

# #### Q1: What is the mean values of E1 and E2?

# In[108]:


data.describe()


# So we can read mean values above. Mean value of E1 is 36.4 and mean value of E2 is 44.0 . Let's add these two.

# In[109]:


mean_E1 = 36.4
mean_E2 = 44.0
mean_tot = mean_E1 + mean_E2
mean_tot


# #### Q2: At how many events is electron 1 negatively charged?

# In[68]:


e_minus_df = data[data.Q1==-1].Event.count()
e_minus_df


# #### Q3: At how many events is electron 1 positively charged, i.e., it is positron? And number of Q1=1 and Q1=-1 adds up to total events.

# In[70]:


e_plus_df = data[data.Q1==+1].Event.count()
e_plus_df


# In[72]:


e_plus_df + e_minus_df == data.Event.count()


# #### Q4: At how many events is absolute value of px1 bigger than 10?

# In[85]:


a = data[data.px1<-10].Event.count()
a


# In[87]:


b = data[data.px1>10].Event.count()
b


# In[88]:


a + b 


# #### Q5: Is there a relation between pz1 and pz2?

# In[111]:


sns.scatterplot(x="pz1", y="pz2", data=data);
plt.title("Scatter plot of pz1 and pz2");


# Yes, there is a relation between pz1 and pz2. As you can see above, when pz1 and pz2 have same sign, their values spread over an area; but when they have opposite sign, they concentrate about the origin.

# In[ ]:


jovian.commit()


# In[ ]:




