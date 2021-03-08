import streamlit as st
import pandas as pd 


st.write("Hi my name is Jason")
st.write("This app will show HDB prices")

import urllib
url = 'https://data.gov.sg/api/action/datastore_search?resource_id=42ff9cfe-abe5-4b54-beda-c88f9bb438ee&limit=5'
fileobj = urllib.urlopen(url)
print fileobj.read()