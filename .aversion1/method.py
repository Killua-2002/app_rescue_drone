import streamlit as st
import pandas as pd
import pydeck as pdk
import numpy as np
import time

st.set_page_config(layout="wide")
st.title("AI Drone Flood Rescue System 3D - Full Version")


# SESSION STATE


if "rain" not in st.session_state:
    st.session_state.rain = 50

if "water_level" not in st.session_state:
    st.session_state.water_level = 0.5

if "drone_pos" not in st.session_state:
    st.session_state.drone_pos = [106.7009, 10.7769]

if "houses" not in st.session_state:
    st.session_state.houses = pd.DataFrame(columns=[
        "id","lat","lon","people","children","elderly",
        "elevation","rescued"
    ])

houses = st.session_state.houses

# FORM THÊM NHÀ


st.sidebar.header("Thêm nhà cần cứu trợ")

with st.sidebar.form("add_house_form"):
    lat = st.number_input("Vĩ độ (lat)", value=10.7769)
    lon = st.number_input("Kinh độ (lon)", value=106.7009)
    people = st.number_input("Số người", min_value=1, value=3)
    children = st.checkbox("Có trẻ em?")
    elderly = st.checkbox("Có người già?")
    elevation = st.number_input("Độ cao nền nhà (m)", min_value=0.0, value=1.0)
    submitted = st.form_submit_button("Thêm nhà")

    if submitted:
        new_id = len(houses) + 1
        new_row = pd.DataFrame([{
            "id": new_id,
            "lat": lat,
            "lon": lon,
            "people": people,
            "children": children,
            "elderly": elderly,
            "elevation": elevation,
            "rescued": False
        }])
        st.session_state.houses = pd.concat([houses, new_row], ignore_index=True)
        st.success("Đã thêm nhà!")

houses = st.session_state.houses


# MƯA LIÊN TỤC


if st.button("Mưa liên tục"):
    for _ in range(20):
        st.session_state.rain += 3
        st.session_state.water_level = st.session_state.rain * 0.01
        time.sleep(0.1)
        st.rerun()

st.write(f"Rain: {st.session_state.rain} mm")
st.write(f"Water level: {round(st.session_state.water_level,2)} m")


# TÍNH NGẬP & ƯU TIÊN


if not houses.empty:

    houses["flood_depth"] = st.session_state.water_level - houses["elevation"]
    houses["flood_depth"] = houses["flood_depth"].apply(lambda x: x if x > 0 else 0)

    houses["priority"] = (
        houses["flood_depth"] * 10 +
        houses["people"] +
        houses["children"]*5 +
        houses["elderly"]*5
    )

    def get_color(row):
        if row["rescued"]:
            return [0,255,0]
        if row["flood_depth"] > 1:
            return [255,0,0]
        if row["flood_depth"] > 0:
            return [255,165,0]
        return [0,0,255]

    houses["color"] = houses.apply(get_color, axis=1)


# DRONE CỨU


if st.button("Drone cứu nhà nguy cấp nhất"):

    pending = houses[(houses["rescued"]==False) & (houses["flood_depth"]>0)]

    if pending.empty:
        st.warning("Không có nhà cần cứu!")
    else:
        target = pending.sort_values("priority",ascending=False).iloc[0]

        steps = 40
        start_lon, start_lat = st.session_state.drone_pos
        end_lon, end_lat = target["lon"], target["lat"]

        for i in range(steps):
            lon = start_lon + (end_lon - start_lon)*(i/steps)
            lat = start_lat + (end_lat - start_lat)*(i/steps)
            st.session_state.drone_pos = [lon, lat]
            time.sleep(0.02)
            st.rerun()

        houses.loc[houses["id"]==target["id"],"rescued"]=True
        st.success(f"Đã cứu nhà {int(target['id'])}")


# MAP 3D


layers = []

# Water layer
water_layer = pdk.Layer(
    "PolygonLayer",
    data=[{
        "polygon":[
            [106.695,10.773],
            [106.705,10.773],
            [106.705,10.780],
            [106.695,10.780]
        ]
    }],
    get_polygon="polygon",
    get_fill_color=[0,0,255,80],
    get_elevation=st.session_state.water_level*20,
    extruded=True
)
layers.append(water_layer)

# House layer
if not houses.empty:
    house_layer = pdk.Layer(
        "ColumnLayer",
        data=houses,
        get_position='[lon, lat]',
        get_elevation="flood_depth",
        elevation_scale=50,
        radius=40,
        get_fill_color="color",
    )
    layers.append(house_layer)

# Drone layer
drone_df = pd.DataFrame({
    "lon":[st.session_state.drone_pos[0]],
    "lat":[st.session_state.drone_pos[1]]
})

drone_layer = pdk.Layer(
    "ScatterplotLayer",
    data=drone_df,
    get_position='[lon, lat]',
    get_fill_color=[0,255,255],
    get_radius=100,
)
layers.append(drone_layer)

view_state = pdk.ViewState(
    latitude=10.7769,
    longitude=106.7009,
    zoom=16,
    pitch=60,
)

deck = pdk.Deck(
    layers=layers,
    initial_view_state=view_state,
)

st.pydeck_chart(deck)


# BẢNG DỮ LIỆU


st.dataframe(houses)