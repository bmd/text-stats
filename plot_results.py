# do imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# get data
results_file = '2014-09-07-16-08-41_test.csv'
df = pd.read_csv(results_file, index_col = 0)
res = df.plot(kind='kde',
    title='Chi2 Statistic Comparison for 5 Vita\n10,000 iterations; sample size 50%',
    figsize=(15,5),
    xlim=(0,200)
    )
res.set_xlabel('Chi2 Statistic')

res = pd.DataFrame.hist(df,
layout=(5, 1),
alpha=0.75,
bins=[x for x in range(0, 200,5)],
figsize=(10, 30),
sharex=True,
sharey=True
)
res.set_xlabel('Chi2 Statistic')

