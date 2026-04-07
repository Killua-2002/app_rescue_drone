import streamlit as st
import plotly.graph_objects as go
import numpy as np
import time
from sklearn.linear_model import LinearRegression

st.set_page_config(layout="wide")
st.title("SMART FLOOD AI + GPS DRONE RESCUE SYSTEM")


# FORM ĐĂNG KÝ TRƯỚC LŨ


if "houses" not in st.session_state:
    st.session_state.houses = []

st.sidebar.header("Đăng ký hộ dân (trước khi lũ xảy ra)")

house_id = st.sidebar.text_input("House ID")
gps_x = st.sidebar.number_input("GPS X", -5.0, 5.0, 0.0)
gps_y = st.sidebar.number_input("GPS Y", -5.0, 5.0, 0.0)
people = st.sidebar.number_input("Số người", 1, 20, 1)
needs = st.sidebar.text_input("Nhu yếu phẩm cần")

if st.sidebar.button("Thêm hộ dân"):
    st.session_state.houses.append({
        "id": house_id,
        "x": gps_x,
        "y": gps_y,
        "people": people,
        "needs": needs,
        "status": "safe"
    })


# WATER SYSTEM


water_speed = st.slider("Tốc độ nước dâng", 0.001, 0.05, 0.01)

if "water_height" not in st.session_state:
    st.session_state.water_height = 0.2
    st.session_state.history = []

st.session_state.water_height += water_speed
water_height = st.session_state.water_height
st.session_state.history.append(water_height)


# TERRAIN


x = np.linspace(-5,5,40)
y = np.linspace(-5,5,40)
X, Y = np.meshgrid(x,y)
Z_ground = 0.3*np.sin(X)*np.cos(Y)
Z_water = water_height + 0.1*np.sin(X+time.time())*np.cos(Y+time.time())

fig = go.Figure()

fig.add_trace(go.Surface(
    x=X,y=Y,z=Z_ground,
    colorscale="Greens",
    showscale=False
))

fig.add_trace(go.Surface(
    x=X,y=Y,z=Z_water,
    colorscale="Blues",
    opacity=0.5,
    showscale=False
))


# DRONE LOGIC


drone_x, drone_y = 0, 0
rescued_this_round = False

for house in st.session_state.houses:
    ground_level = 0.3*np.sin(house["x"])*np.cos(house["y"])
    flooded = water_height > ground_level + 1.0

    if flooded and house["status"] == "safe":
        house["status"] = "flooded"

    # Drone cứu nhà bị ngập chưa cứu
    if house["status"] == "flooded" and not rescued_this_round:
        drone_x = house["x"]
        drone_y = house["y"]
        house["status"] = "rescued"
        rescued_this_round = True
        st.warning(f"Drone cứu nhà {house['id']} - {house['people']} người - Cần: {house['needs']}")

    # Màu theo trạng thái
    if house["status"] == "safe":
        color = "red"
    elif house["status"] == "flooded":
        color = "purple"
    else:
        color = "green"

    fig.add_trace(go.Scatter3d(
        x=[house["x"]],
        y=[house["y"]],
        z=[ground_level+1],
        mode="markers",
        marker=dict(size=12,color=color),
        name=house["id"]
    ))

# Drone hiển thị
fig.add_trace(go.Scatter3d(
    x=[drone_x],
    y=[drone_y],
    z=[3],
    mode="markers",
    marker=dict(size=10,color="yellow"),
    name="Drone"
))


# DASHBOARD INFO


total = len(st.session_state.houses)
rescued = len([h for h in st.session_state.houses if h["status"]=="rescued"])
flooded = len([h for h in st.session_state.houses if h["status"]=="flooded"])

col1,col2,col3 = st.columns(3)
col1.metric("Tổng hộ dân", total)
col2.metric("Đang ngập", flooded)
col3.metric("Đã cứu", rescued)


# LAYOUT


fig.update_layout(
    scene=dict(
        zaxis=dict(range=[-1,4])
    ),
    margin=dict(l=0,r=0,b=0,t=30)
)

st.plotly_chart(fig, use_container_width=True)

