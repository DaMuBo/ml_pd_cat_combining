# ml_pd_cat_combining
A small repositiory for transforming data before the usage of for example an One Hot Encoding to reduce the resulting dimensions

# Description

Introduces a small class which can be used to create an Object which holds the information about a dataframe and his structures. So it can "learn" how to transform the values in an dataframe and reduce the resulting dimensions of the column ( the number of unique values) based on a threshold.


# Usage
* from ml_cat_combiner import *

### Initialize the class
  * cat_reducer = ml_combining()

### fit the object based on input dataframe
  * cat_reducer.fit(df)

for adjusting the threshold below the data should be generalized just change the value( Values between 0,1):
  * cat_reducer.fit(df, threshold = 0.002)
  
 for changing the mapping function ( standard = map) add the value for it in the fit function. There are 3 allowed values for this function:
 * 'map': is mapping all unknown values to the defined generalisation
 * 'ignore' : is ignoring the unknown values and keeps the original value as output
 * 'unseen' : is creating a second generalisation "unknown" in which all new / unknown values are going to be transformed
  ** cat_reducer.fit(df, unseen_data='map')
  
  

### transform the values of a new dataframe
  * transformd_df = cat_reducer.transform(df)

### load model
  * cat_reducer.load_model(Pathtosavedmodell)

### save model
  * cat_reducer.save_model(Pathtomodell)

# Author / Contact
Daniel M.
