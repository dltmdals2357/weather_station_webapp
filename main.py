import streamlit as st
import requests
import os
import xmltodict
import datetime
# import streamlit_extras
from weather_code import w_value                # w_value['PTY'][0]  => 강수형태

#api use : getVilageFcst

service_key = os.environ.get('STATION_WEATHER_API_KEY')
now = datetime.datetime.now()
year = now.strftime('%Y')
month = now.strftime('%m')
day = now.strftime("%d")
basedate = f'{year}{month}{day}'
hour = now.strftime('%H')
minute = now.strftime('%M')
background = "#218CE3"
nx=63
ny=127

background_sun = "rgb(50, 130, 246)"
background_cloud = "rgb(90, 135, 246)"
background_cloud_2 = "rgb(60, 80, 150)"

w_info = {}
desig_num = ['02', '05', '08', '11', '14', '17', '20', '23']

current_day = f'{year}.{month}.{day}'
current_time = f'{hour} : {minute}'

for num in desig_num:
    if int(hour) >= int(num) and abs(int(num) - int(hour)) < 3:
        current_time_code = f'{num}00'

url = f"http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst?serviceKey={service_key}&numOfRows=10&pageNo=1&base_date={basedate}&base_time={current_time_code}&nx={nx}&ny={ny}"
response = requests.get(url)
print(url)

img = ""
img2 = ""

if response.status_code == 200:
    dict_data = xmltodict.parse(response.content)
    item_list = dict_data["response"]["body"]["items"]["item"]

centered_text_style = """
    <style>
        div {
            text-align: center;
            justify-content: center;
        }
        .highlight {
            font-size: 50px;
            font-weight: light;
        }
    </style>
"""                     # display: flex;

if 'background' not in st.session_state:
    st.session_state.background = background_sun

background_style = f"""
    <style>
        stApp {{
            background-color: {st.session_state.background};

        }}
    </style>
"""

st.markdown(centered_text_style, unsafe_allow_html=True)
st.markdown(background_style, unsafe_allow_html = True)
print(background_style)

for item in item_list:
    if item["category"] == "SKY":
        if item["fcstValue"] == "1":
            w_info[item["category"]] = "맑음"
            img = "./image/SKY/sun_c.png"
            st.session_state.background = background_sun
        elif item["fcstValue"] == "3":
            w_info[item["category"]] = "구름많음"
            img = "./image/SKY/cloud_lot.png"
            st.session_state.background = background_cloud
        elif item["fcstValue"] == "4":
            w_info[item["category"]] = "흐림"
            img = "./image/SKY/cloud.png"
            st.session_state.background = background_cloud_2
    elif item["category"] == "PTY":
        if item["fcstValue"] == "0":
            w_info[item["category"]] = "없음"
            img2 = "./image/PTY/none.png"
        elif item["fcstValue"] == "1":
            w_info["fcstValue"] == "비"
            img2 = "./image/PTY/rain.png"
        elif item["fcstValue"] == "2":
            w_info["fcstValue"] == "비/눈"
            img2 = "./image/PTY/snow_rain.png"
        elif item["fcstValue"] == "3":
            w_info["fcstValue"] == "눈"
            img2 = "./image/PTY/snow.png"
        elif item["fcstValue"] == "4":
            w_info["fcstValue"] == "소나기"
            img2 = "./image/PTY/shower.png"
    elif item["category"] == "PCP":
        if item["fcstValue"] == "강수없음":
            w_info[item["category"]] = '0' + w_value[item["category"]][1]
        else:
            w_info[item["category"]] = item["fcstValue"] + w_value[item["category"]][1]
    else:
        w_info[item["category"]] = item["fcstValue"] + w_value[item["category"]][1]



st.image(img, width=120)
st.write(f"<span class='highlight'>{w_info['TMP']} </span>", unsafe_allow_html=True)
st.write(f"<h4> {w_info['SKY']} </h4>", unsafe_allow_html=True)
st.write(' ')
st.write(' ')
st.image(img2, width=60)
st.write(f"<h6> 강수확률 : {w_info['POP']} &emsp; 강수량 : {w_info['PCP']}</h6>", unsafe_allow_html=True)


# st.write(item_list)
# st.write(w_info)                    # {"TMP" : "1", "UUU" : "1.3" , ...}


st.write(' ')
st.subheader(current_time)
st.write(' ')
st.markdown("서울특별시")
st.markdown("강동구 고덕 제1동")

st.write(current_day)
