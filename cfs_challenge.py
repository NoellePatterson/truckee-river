# 1000 cfs challenge: predict day of water year 2021 that Truckee at Floriston will reach 1000cfs!
# Noelle Patterson
# March 2021

import pandas as pd
import numpy as np
from Utils import get_date_1000

# Assemble input data: Floriston cfs, Apr 1 snowpack, avg Apr temp
farad = pd.read_csv('outputs/farad_flow.csv', sep=',', index_col=None, parse_dates=True)

# Two flow metrics: most current date'cfs, smoothed val, and date of 1000cfs

years = []
for i in range(len(farad['date'])):
    years.append(int(farad['date'][i].split('-')[2]))
years_uniq = np.unique(years)
jul_date_1000 = get_date_1000(farad, years)

# build table with all annual vals
annual_vals = pd.DataFrame(years_uniq)
import pdb; pdb.set_trace()

# multi-regression to find this year's date to 1000cfs
