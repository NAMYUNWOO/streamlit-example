import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
import requests
from datetime import datetime,timedelta

def stringToFloat(mystr):
    try:
        return float(mystr.strip())
    except:
        return 0.0


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
    characterName = st.text_input(label='캐릭터명1',value='캐릭터명을 입력하고 엔터', placeholder ='캐릭터명을 입력하고 엔터', key=next(widget_id))

with col2:
    characterName2 = st.text_input(label='캐릭터명2',value='캐릭터명을 입력하고 엔터', placeholder ='캐릭터명을 입력하고 엔터', key=next(widget_id))    


charInfo1 = dict()
charInfo2 = dict()
if characterName and (characterName != "캐릭터명을 입력하고 엔터"):
    charInfo1 = getCharInfo(characterName)

if characterName2 and (characterName2 != "캐릭터명을 입력하고 엔터"):
    charInfo2 = getCharInfo(characterName2)    



charClass1 = charInfo1.get('character_class','not_known')
charClass2 = charInfo2.get('character_class','not_known')


df1,df2 = (pd.DataFrame([{'스탯':stringToFloat(i['stat_value']),'스탯명':i['stat_name'].strip(),'캐릭터':characterName}  for i in charInfo1.get('final_stat',[{'stat_name':"",'stat_value':'0.0'}])]),
           pd.DataFrame([{'스탯':stringToFloat(i['stat_value']),'스탯명':i['stat_name'].strip(),'캐릭터':characterName2}  for i in charInfo2.get('final_stat',[{'stat_name':"",'stat_value':'0.0'}])])
           )
df12 = pd.merge(df1,df2, on=['스탯명'],how='outer').fillna({'스탯_x':0.0,'스탯_y':0.0})
if len(df12) == 0:
    df12 = pd.DataFrame({'스탯_x':[0.0],
                         '스탯_y':[0.0],
                         '캐릭터_x':[''],
                         '캐릭터_y':[''],
                         '스탯명':[''],
                         })

df12['스탯율_x'] = [ i/(i+j) if (i+j) != 0.0 else 0.0 for i,j in zip(df12['스탯_x'],df12['스탯_y'])]
df12['스탯율_y'] = [ j/(i+j) if (i+j) != 0.0 else 0.0 for i,j in zip(df12['스탯_x'],df12['스탯_y'])]
df11 = df12[['스탯율_x','스탯_x','스탯명','캐릭터_x']]
df22 = df12[['스탯율_y','스탯_y','스탯명','캐릭터_y']]
df11.columns = [i.replace('_x','') for i in  df11.columns]
df22.columns = [i.replace('_y','') for i in  df22.columns]
df11['캐릭터'] = [df11['캐릭터'].dropna().iloc[0]] * len(df11)
df22['캐릭터'] = [df22['캐릭터'].dropna().iloc[0]] * len(df11)
source = pd.concat([df11,
                df22
               ],

              axis = 0
           )

bars = alt.Chart(source).mark_bar().encode(
    x=alt.X('sum(스탯율):Q').stack('zero'),
    y=alt.Y('스탯명:N'),
    color=alt.Color('캐릭터')
)

text = alt.Chart(source).mark_text(dx=-15, dy=3, color='white').encode(
    x=alt.X('sum(스탯율):Q').stack('zero'),
    y=alt.Y('스탯명:N'),
    detail='캐릭터:N',
    text=alt.Text('sum(스탯):Q', format='.1f')
)


st.altair_chart(bars + text, use_container_width=True)
#st.write(charInfo1)
#st.write(charInfo2)



st.divider()
st.caption('Data based on NEXON Open API')

