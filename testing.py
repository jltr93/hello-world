import streamlit as st
import pandas as pd 
import numpy as np 
import requests
import json

import requests
import matplotlib.pyplot as plt
import seaborn as sns

from scipy.stats import norm
from sklearn.preprocessing import StandardScaler
from scipy import stats
import warnings

#get data from api
response = requests.get('https://data.gov.sg/api/action/datastore_search?resource_id=42ff9cfe-abe5-4b54-beda-c88f9bb438ee&limit=200000')
#convert data to json format to be consumed by pandas
response2 = response.json()
#result is a dictionary, choose the key to display the correct list
result = response2.get('result')
#choose second key
records = result.get('records')
#convert to json and assign to new variable
json_string = json.dumps(records)
#consumed by pandas
df = pd.read_json(json_string)

###transformation
#split year-month of sale string
df[['year_of_sale','month_of_sale']] = df.month.str.split("-",expand=True)
#split remaining_lease_years string
df[['remaining_lease_years','yeartext','remaining_lease_months','monthtext']] = df.remaining_lease.str.split(" ",expand=True)
#split storey min_max string
df[['storey_range_min','storey_range_max']]=df.storey_range.str.split(" TO ",expand=True)
#insert new column with datetime format for date of sale
df['date_of_sale']= pd.to_datetime(df['month'])
#change python None to NaN remaining_lease_months, monthtext
df.remaining_lease_months.fillna(value=0,inplace=True)
df.monthtext.fillna(value=0,inplace=True)
#change required type to int, for comparison
df = df.astype({"floor_area_sqm":int,"resale_price":int,"lease_commence_date":int,"year_of_sale":int,"month_of_sale":int,"remaining_lease_years":int,"remaining_lease_months":int,"storey_range_min":int,"storey_range_max":int})
#calculate average storey (can be used as actual floor)
df['storey_average']=df[['storey_range_min','storey_range_max']].mean(axis=1)
#drop unwanted columns
df=df.drop(columns=['yeartext','monthtext'])




st.markdown("## This app will show HDB resale prices")

st.markdown("First we start by getting data from public domain and converting it into a dataframe")
st.markdown("First 5 rows of the data")
st.dataframe(df.head(),2000)

st.markdown("Next we perform simple EDA(Exploratory Data Analysis) to get a better understanding of the columns and how they correlate(or not) with one another")


with st.echo(code_location='below'):
    import matplotlib.pyplot as plt

    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)

    ax.scatter(
        df["date_of_sale"],
        df["resale_price"],
    )

    ax.set_xlabel("date_of_sale")
    ax.set_ylabel("resale_price")

    st.write(fig)


st.write("*Data is from public domain, [here](https://data.gov.sg).*")