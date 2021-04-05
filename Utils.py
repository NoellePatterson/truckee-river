import pandas as pd
from datetime import datetime
from climata.usgs import DailyValueIO
import numpy as np
import matplotlib
import matplotlib.pyplot as plt


def import_USGS_flow():
    '''
    easy USGS data import code, only need to run once if storing resulting data
    '''

    # define parameters for each gage: start year, end year, stationID, and data code (0060=flow)
    vista = ['vista', '1899-10-01', '2020-06-01', '10350000', '00060']
    tracy = ['tracy', '1997-10-01', '2020-06-01', '10350340', '00060']
    derby_withdrawl = ['derby_withdrawl', '1966-10-01', '2020-06-01', '10351300', '00060']
    blw_derby = ['blw_derby', '1918-10-01', '2020-06-01', '10351600', '00060']
    wadsworth = ['wadsworth', '1965-10-01', '2020-06-01', '10351650', '00060']
    nixon = ['nixon', '1957-10-01', '2020-06-01', '10351700', '00060']
    farad = ['farad', '1987-10-01', '2021-03-30', '10346000', '00060']
    ltr_gages = [vista, tracy, derby_withdrawl, blw_derby, wadsworth, nixon]
    ltr_gages = [farad]

    for gage in ltr_gages:
        # define parameters for the data type, location, and period of record
        start_day = pd.to_datetime(gage[1])
        end_day = pd.to_datetime(gage[2])
        num_days = (end_day-start_day).days
        station_id = gage[3]
        param_id = gage[4]

        # apply function to pull data from USGS 
        data = DailyValueIO(
        start_date=start_day,
        end_date=end_day,
        station=station_id,
        parameter=param_id,
        )

        # arrange data into lists and convert cfs to cms
        for series in data:
            dates = [r[0] for r in series.data]
            date_print = [r[0].strftime("%m-%d-%Y") for r in series.data]
            cfs_flow = [r[1] for r in series.data]
            cms_flow = [r[1]*.0283168 for r in series.data]

        # Convert to dataframe and  export as a csv
        data = {'date':date_print, 'cms_flow':cms_flow, 'cfs_flow':cfs_flow}
        flow_df = pd.DataFrame(data)
        flow_df[['date','cfs_flow']].to_csv("outputs/{}_flow.csv".format(gage[0]), sep=',', index=False)

    return flow_df

def get_date_1000(flow_df, years):
    # function returns calendar day of first day to reach 1000 cfs per year

    # create separate years column in df
    flow_df['years'] = years
    # append a marker for each year with day (since Jan 1) to reach 1000 cfs
    day1k = pd.DataFrame(np.unique(years), columns = ['year'])
    day1k['day'] = np.empty(len(day1k['year']))
    day1k['apr_q'] = np.empty(len(day1k['year']))
    day1k['day'] = np.NaN
    year_list = np.unique(years)
    for year_index, year_val in enumerate(year_list):
        days = flow_df['cfs_flow'][flow_df['years'] == year_val] # pull out flow for days in the given year
        day_loc = days.index
        day1k['apr_q'][year_index] = np.nanmean(days[80:90])
        # import pdb; pdb.set_trace()
        for day_index, day_flow in enumerate(days):
            if day_flow > 1000:
                day1k['day'][year_index] = day_index
                break
    return(day1k)

