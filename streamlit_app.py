import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
import requests
from datetime import datetime,timedelta

st.title("🍁")
api_key = st.secrets['NEXON_API_KEY']
headers = {
  "x-nxopen-api-key": api_key
}
characterName = st.text_input('캐릭터명을 입력하세요.', '캐릭터명을 입력하세요.')
if characterName and (characterName != "캐릭터명을 입력하세요."):
    urlString_ocid = "https://open.api.nexon.com/maplestory/v1/id?character_name=" + characterName
    response_ocid = requests.get(urlString_ocid, headers = headers)

    ocid = response_ocid.json().get('ocid','')
    if ocid != "":
        urlString_stat = 'https://open.api.nexon.com/maplestory/v1/character/stat?ocid={}&date={}'.format(ocid,(datetime.now()-timedelta(days=1)).strftime('%Y-%m-%d'))

        response_stat = requests.get(urlString_stat, headers = headers)

        st.write(response_stat.json())
    else:
        st.write("캐릭터명 '{}' 를 찾지 못했습니다.".format(characterName))

