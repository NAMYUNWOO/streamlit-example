import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
import requests
from datetime import datetime,timedelta


def getCharInfo(characterName):
    charInfo1 = dict()
    urlString_ocid = "https://open.api.nexon.com/maplestory/v1/id?character_name=" + characterName
    response_ocid = requests.get(urlString_ocid, headers = headers)

    ocid = response_ocid.json().get('ocid','')
    if ocid != "":
        urlString_stat = 'https://open.api.nexon.com/maplestory/v1/character/stat?ocid={}&date={}'.format(ocid,(datetime.now()-timedelta(days=1)).strftime('%Y-%m-%d'))

        response_stat = requests.get(urlString_stat, headers = headers)
        charInfo1 = response_stat.json()
        charInfo1['res'] = 'found'
    else:
        charInfo1 = dict()
        charInfo1['res'] =  "캐릭터명 '{}' 를 찾지 못했습니다.".format(characterName)
    return charInfo1

    

st.title("🍁")
api_key = st.secrets['NEXON_API_KEY']
headers = {
  "x-nxopen-api-key": api_key
}
widget_id = (id for id in range(1, 100_00))

col1, col2 = st.columns(2)
with col1:
    characterName = st.text_input(label='캐릭터명1', value='캐릭터명을 입력하세요.', key=next(widget_id))

with col2:
    characterName2 = st.text_input(label='캐릭터명2', value='캐릭터명을 입력하세요.', key=next(widget_id))    


charInfo1 = dict()
charInfo2 = dict()
if characterName and (characterName != "캐릭터명을 입력하세요."):
    charInfo1 = getCharInfo(characterName)

if characterName2 and (characterName2 != "캐릭터명을 입력하세요."):
    charInfo2 = getCharInfo(characterName2)    


st.write(charInfo1)
st.write(charInfo2)



st.divider()
st.caption('Data based on NEXON Open API')

