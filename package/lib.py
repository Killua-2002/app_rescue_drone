import math

BOUNDING_BOX = {
    "left": (10.776, 106.591),   # 1758 TL10
    "top": (10.828, 106.685),    # 12 Phan Văn Trị
    "right": (10.770, 106.772),  # Nguyễn Thị Định
    "bottom": (10.725, 106.719)  # 101 Tôn Dật Tiên
}

GOV_STATIONS = (
    {"address": "Trạm 1 (Quận 1)", "coords": (10.7769, 106.7009), "drones": 10},
    {"address": "Trạm 2 (Tân Bình)", "coords": (10.8018, 106.6569), "drones": 10}
)

DRONE_SPEED_KMH = 150

def calculate_danger_level(ill, young, old, total):
    vulnerable = ill + young + old
    if vulnerable >= total or ill > 2: return "extrem", "red"
    elif vulnerable > 0: return "high", "orange"
    else: return "low", "yellow"