import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

import pymysql
import streamlit as st

import datetime

today = datetime.date.today()
tomorrow = today + datetime.timedelta(days = 1)
pc_components = ['CPU', 'GPU']
time_range = ['1H', '3H', '6H', '9H', '12H']
date_range = ['Daily', 'Weekly', 'Monthly']

def import_data(table, start_date, end_date):
    connect = pymysql.connect(host = 'localhost', user = 'root', password = '4643', db = 'danawa', charset = 'utf8mb4')
    cur = connect.cursor()
    
    col_sql = "SHOW FULL COLUMNS FROM {}".format(table)
    cur.execute(col_sql)
    col_info = cur.fetchall()
    
    columns = [col[0] for col in col_info]
    
    sql = "SELECT * FROM {} WHERE DATE(CRAWL_DATE) >= '{}' AND DATE(CRAWL_DATE) <= '{}'".format(table,start_date, end_date)
    print(sql)
    
    cur.execute(sql)
    result = cur.fetchall()
    
    connect.close()
    
    df = pd.DataFrame(result, columns = columns)
    
    return df

# Main Title Setting 
st.title("Danawa PC Components Price Report")
st.markdown(
    """
    This Page offers PC component price trends from Danawa, a site that provides price and information for Korean electornic products.
    
    Currently, only CPU and GPU are provided with PC components information. In the future, we will provide more information.
    
    Data is collected every 5 minutes. Therefore, you can check the price information every hour.

    Due to the collection of data and copyright, it is only provided as a personal service.

    Caution: because data was collected locally using crawling automation, data for all times may not exist.

    [See Source Code](https://github.com/SSANGMAN/Danawa)
    """)

# Sidebar Setting
## Condition
st.sidebar.header("Condition")
st.sidebar.markdown("""Choose Condition about Components Type and Time Interval""")
component_box = st.sidebar.selectbox(
    "PC Component: Choose which pc component you want to see.", pc_components)

start_date = st.sidebar.date_input('Start Date: Set the start period for the data to be imported.', today)
end_date = st.sidebar.date_input('End Date: Set the end period for the data to be imported.', tomorrow)
if start_date > end_date:
    st.sidebar.error('Error: End date must fall after start date.')

time_interval = st.sidebar.radio(
    'Time Interval (Hour): Choose Select how often you want to check the information.', options = time_range,
    index = 0)
## Styling
st.sidebar.header("Styling")
st.sidebar.markdown(""" Choose Styling about Visualization """)
popular_slider = st.sidebar.slider(
    'Popular Product: Please select the popularity ranking you want to check.',
    min_value = 1, max_value = 50, value = 1
)
report_type = st.sidebar.radio(
    'Report Type: Please select an output period for the report.', options = date_range,
    index = 2
)

# Main Page
## DataFrame
st.header("DataFrame")
st.markdown(
    """
    Shows the data frames for the selected time period.
    """)
df = import_data(component_box, start_date, end_date)
cols = df.columns.tolist()
selected_time = int(time_interval[:-1]) 
st_ms = st.multiselect("Columns", df.columns.tolist(), default = cols)
filter_df = df.loc[(df['HOUR'] // selected_time != 0) & (df['HOUR'] % int(selected_time) == 0) & (df['RANKING'] <= popular_slider)][st_ms]

if component_box == 'CPU':
    select_brand = st.selectbox("Brand", ["All", "Intel", "AMD"])

    if select_brand == 'All':
        brand_df = filter_df
        st.dataframe(filter_df)

    else:
        if select_brand == "Intel":
            brand_df = filter_df[filter_df['NAME'].str.contains(r'인텔')]
            st.dataframe(filter_df[filter_df['NAME'].str.contains(r'인텔')])
        
        elif select_brand == 'AMD':
            brand_df = filter_df[filter_df['NAME'].str.contains(r'AMD')]
            st.dataframe(filter_df[filter_df['NAME'].str.contains(r'AMD')])

elif component_box == "GPU":
    brand_list = ["All"]
    brand_list.extend(df['BRAND'].unique().tolist())
    select_brand = st.selectbox("Brand", brand_list)

    if select_brand == 'All':
        brand_df = filter_df
        st.dataframe(brand_df)
    else:
        brand_df = filter_df.loc[df['BRAND'] == select_brand]
        st.dataframe(brand_df)
## Line Plot
st.header("Line Plot")
st.markdown(
    """
    Show the Bar plot Which brand is more popular? for the selected time period.

    If there is no data collected during the specified period, an error will occur.
    """
)
### Line Plot Preprocessing
def LinePlotPreprocess(data, process_type):
    if process_type == 'price':
        line_df = pd.pivot_table(data, index = ['CRAWL_DATE', 'HOUR'], columns = 'NAME', values = 'PRICE').reset_index()
    
    elif process_type == 'rank':
        line_df = pd.pivot_table(data, index = ['CRAWL_DATE', 'HOUR'], columns = 'NAME', values = 'RANKING').reset_index()
    
    tmp_time_list = []
    for i in range(len(line_df)):
        time = pd.to_datetime(line_df['HOUR'], format = '%H').astype(str).str.split(" ")[i][1]
        tmp_time_list.append(time)

    line_df['DATE'] = line_df['CRAWL_DATE'].astype(str) + " " + tmp_time_list
    line_df.drop(columns = ['CRAWL_DATE', 'HOUR'], inplace = True)
    line_df.set_index("DATE", inplace = True)
    line_df.columns.name = None

    return line_df
#### About Ranking
st.subheader("RANKING")
st.markdown(
    """ 
    Shows the ranking changes of products during the specified period.
    """
)
#### About Price
ranking_df = LinePlotPreprocess(brand_df, process_type = 'rank')
### Visualization
try:
    st.line_chart(ranking_df)
except ValueError:
    st.error("Invalid period specification, or no collected data exists. Please re-specify the period.")

st.subheader("Price")
st.markdown(
    """ 
    Shows the price changes of products during the specified period.
    """
)
#### About Price
price_df = LinePlotPreprocess(brand_df, process_type = 'price')
### Visualization
try:
    st.line_chart(price_df)
except ValueError:
    st.error("Invalid period specification, or no collected data exists. Please re-specify the period.")