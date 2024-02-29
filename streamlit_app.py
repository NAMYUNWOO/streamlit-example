import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
import requests
from datetime import datetime,timedelta

"""
🍁
"""
api_key = st.secrets['NEXON_API_KEY']
headers = {
  "x-nxopen-api-key": api_key
}

characterName = "아델"
urlString_ocid = "https://open.api.nexon.com/maplestory/v1/id?character_name=" + characterName
response_ocid = requests.get(urlString_ocid, headers = headers)

ocid = response_ocid.json()['ocid']

urlString_stat = 'https://open.api.nexon.com/maplestory/v1/character/stat?ocid={}&date={}'.format(ocid,(datetime.now()-timedelta(days=1)).strftime('%Y-%m-%d'))

response_stat = requests.get(urlString_stat, headers = headers)

st.write(response_stat.json())

