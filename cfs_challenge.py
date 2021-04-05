# 1000 cfs challenge: predict day of water year 2021 that Truckee at Floriston will reach 1000cfs!
# Noelle Patterson
# March 2021

import pandas as pd
import numpy as np
from Utils import get_date_1000
from sklearn import linear_model

# Assemble input data: Floriston cfs, Apr 1 snowpack, avg Apr temp
farad = pd.read_csv('outputs/farad_flow.csv', sep=',', index_col=None, parse_dates=True)

# Two flow metrics: most current date'cfs, smoothed val, and date of 1000cfs

years = []
for i in range(len(farad['date'])):
    years.append(int(farad['date'][i].split('-')[2]))
years_uniq = np.unique(years)
jul_date_1000 = get_date_1000(farad, years)

march_snow = pd.read_csv('march_snow.csv', sep=',', index_col=None)
april_snow = pd.read_csv('april_snow.csv', sep=',', index_col=None)
jul_date_1000['mar_snow'] = march_snow['snow']
jul_date_1000['apr_snow'] = april_snow['snow']

# multi-regression to find this year's date to 1000cfs
df = jul_date_1000
df = df.dropna(axis=0)
X = df[['mar_snow', 'apr_snow', 'apr_q']]
Y = df['day']

regr = linear_model.LinearRegression()
regr.fit(X, Y)
print('Intercept: \n', regr.intercept_)
print('Coefficients: \n', regr.coef_)
# import pdb; pdb.set_trace()
day_predict = regr.predict([[12.8 , 10.4, 576.3]])

import pdb; pdb.set_trace()