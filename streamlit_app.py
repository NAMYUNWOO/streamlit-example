import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
import requests

"""
test from namyunwoo
# Welcome to Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:.
If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""
api_key = st.secrets['NEXON_API_KEY']
headers = {
  "x-nxopen-api-key": api_key
}

# characterName = "아델"
# urlString = "https://open.api.nexon.com/heroes/v1/id?character_name=" + characterName
# response = requests.get(urlString, headers = headers)

#st.write(str(response.json()))

st.write(api_key)