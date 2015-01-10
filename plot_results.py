### DUMP THIS INTO IPYTHON ####
# do imports first
import pandas as pd
import glob
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
from ggplot import *

# get data loaded into iPython
most_recent_results = max(glob.glob(os.path.join('outputs', '*.csv')))
df = pd.read_csv(most_recent_results, index_col = 0)

df2 = pd.melt(df2)

# plot all self-vs-self comparisons
ggplot(
    aes(
        x='value',
        colour='variable'
    ),
    data=df
) + \
geom_density(
    aes(
        fill=True,
        alpha=0.1
    ),
    trim=False
)
#plot the avg curve

ggplot() + geom_density()
ggplot(aes(x='value'), data=df2) + geom_density(aes(x='value', data=df2, fill=True, alpha=0.1), trim=False)



ggplot(aes(x='Chi2 Statistic', colour='Comparison Text'), data=df) + geom_density(aes(fill=True, alpha=0.1), trim=False)

plt = ggplot(aes(x='Chi2 Statistic'), data=df)
plt = plt + geom_density(aes(fill=True, alpha=0.1), trim=False)
plt = plt + geom_density(aes(x='value'), fill=True, alpha=0.1, data=df2, trim=False)
plt + geom_density(aes(x='Chi2 Statistic', colour='Comparison Text'), data=df3, fill=True, alpha=0.1, trim=False)


ggplot(aes(x='Chi2 Statistic', colour='Base Text'), data=df3) + geom_density()