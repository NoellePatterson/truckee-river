import pandas as pd
from functools import reduce
import datetime


def process_flow():
    ''' 
    Calculate changes in flow across stream gages of the Lower Truckee River
    '''

    # import csv's, set flow columns to unique names
    vista = pd.read_csv('outputs/vista_flow.csv', sep=',', index_col=0, parse_dates=True, header=0, names=['vista'])
    vista = vista.loc['19581001':] # Avoid date parsing errors by starting Vista data when rest of data starts

    tracy = pd.read_csv('outputs/tracy_flow.csv', sep=',', index_col=0, parse_dates=True, header=0, names=['tracy'])
    derby_withdrawl = pd.read_csv('outputs/derby_withdrawl_flow.csv', sep=',', index_col=0, parse_dates=True, header=0, names=['derby_withdrawl'])
    blw_derby = pd.read_csv('outputs/blw_derby_flow.csv', sep=',', index_col=0, parse_dates=True, header=0, names=['blw_derby'])
    blw_derby = blw_derby.loc['19581001':] # Avoid date parsing errors by starting blw derby data when rest of data starts

    wadsworth = pd.read_csv('outputs/wadsworth_flow.csv', sep=',', index_col=0, parse_dates=True, header=0, names=['wadsworth'])
    nixon = pd.read_csv('outputs/nixon_flow.csv', sep=',', index_col=0, parse_dates=True, header=0, names=['nixon'])
    nixon = nixon.loc['19971001':] # Avoid date parsing errors by starting nixon data when rest of data starts

    # 1. Align flow columns by date so dates match across rows. 
    data_frames = [vista, tracy, derby_withdrawl, blw_derby, wadsworth, nixon]
    for df in data_frames:
        df.index.name='date'
    df_merged = reduce(lambda  left,right: pd.merge(left,right,on=['date'], how='outer'), data_frames).fillna('')
    
    df_merged = df_merged.loc['19971001':] # Start df where all data records align at 10/1/1997
    df_merged = df_merged.apply(pd.to_numeric) # Convert all values to numeric for later processing
    
    # 2. Adjust flow of downstream gages to account for withdrawl from Derby Dam. 
    df_merged['blw_derby_adj'] = df_merged['blw_derby'].add(df_merged['derby_withdrawl'])  
    df_merged['wadsworth_adj'] = df_merged['wadsworth'].add(df_merged['derby_withdrawl'])  
    df_merged['nixon_adj'] = df_merged['nixon'].add(df_merged['derby_withdrawl'])  

    # 3. Calculate differences across gages. Account for seasonality and varying location start and end points. 
    # Positive values indicate losing reach, negative values are gaining reach. 
    deltas = pd.DataFrame(columns = ['vista_tracy'])
    deltas['vista_tracy'] = df_merged['vista'] - df_merged['tracy']
    deltas['tracy_derby'] = df_merged['tracy'] - df_merged['blw_derby_adj']
    deltas['derby_wadsworth'] = df_merged['blw_derby_adj'] - df_merged['wadsworth_adj']
    deltas['wadsworth_nixon'] = df_merged['wadsworth_adj'] - df_merged['nixon_adj']
    deltas['vista_nixon'] = df_merged['vista'] - df_merged['nixon_adj']

    # Separate delta values to compare seasonal differences
    deltas['month'] = pd.DatetimeIndex(deltas.index).month
    months = ['jan', 'feb', 'march', 'april', 'may', 'june', 'july', 'aug', 'sept', 'oct', 'nov', 'dec']
    # New summary df to store average monthly and annual deltas across sites
    summary_deltas = pd.DataFrame(columns = ['month', 'vista_tracy', 'tracy_derby', 'derby_wadsworth', 'wadsworth_nixon', 'vista_nixon'])
    summary_deltas = summary_deltas.append(deltas.mean(), ignore_index=True) # add annual averages to summary data table
    summary_deltas.iloc[0,0] = 'all_year' # add meaningful label in df for annual averages

    for index, month in enumerate(months):
        summary_data = deltas[deltas['month'] == index+1].mean() # Take average of deltas for each month
        summary_deltas = summary_deltas.append(summary_data, ignore_index=True) # add to summary table

    # output a summary 
    summary_deltas.to_csv('outputs/flow_summary.csv', index=False)
    import pdb; pdb.set_trace()

    # 4. Find a creative way to visualize. 

    return
