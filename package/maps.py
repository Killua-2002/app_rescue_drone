import tkinter as tk
import tkintermapview
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from package.lib import GOV_STATIONS, BOUNDING_BOX

class RescueMap(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.geolocator = Nominatim(user_agent="rescue_app")
        
        self.map_widget = tkintermapview.TkinterMapView(self, corner_radius=0)
        self.map_widget.pack(fill="both", expand=True)
        self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga")
        
        self.map_widget.set_position(10.776, 106.69)
        self.map_widget.set_zoom(13)
        
        self.stations = []
        self.init_gov_stations()

    def init_gov_stations(self):
        for st in GOV_STATIONS:
            marker = self.map_widget.set_marker(
                st["coords"][0], st["coords"][1], 
                text=f"{st['address']} (Drones: {st['drones']})", 
                marker_color_circle="deep sky blue", 
                marker_color_outside="black"
            )
            self.stations.append({"marker": marker, "data": st})

    def add_citizen_request(self, data, color):
        try:
            location = self.geolocator.geocode(data["address"] + ", Hồ Chí Minh, Việt Nam")
            lat, lon = location.latitude, location.longitude
        except:
            lat, lon = 10.78 + (len(self.map_widget.canvas_marker_list) * 0.005), 106.69
            
        popup_text = f"DL: {data['danger_level']}\nTotal: {data['total']}\nI: {data['ill']} - Y: {data['children']} - O: {data['elderly']}\nAdd: {data['address']}"
        
        citizen_marker = self.map_widget.set_marker(lat, lon, text=popup_text, marker_color_outside=color)
        
        self.dispatch_drone(lat, lon, citizen_marker)

    def dispatch_drone(self, target_lat, target_lon, citizen_marker):
        station = self.stations[0]
        
        if station["data"]["drones"] <= 0:
            print("Trạm này đã hết drone!")
            station["marker"].marker_color_circle = "gray"
            station["marker"].draw()
            return
            
        station["data"]["drones"] -= 1
        station["marker"].set_text(f"🏢 {station['data']['address']} (Drones: {station['data']['drones']})")
        
        start_coords = station["data"]["coords"]
        end_coords = (target_lat, target_lon)
        
        path = self.map_widget.set_path([start_coords, end_coords], color="#FF0044", width=3)
        
        drone_marker = self.map_widget.set_marker(
            start_coords[0], start_coords[1], 
            text="🚁 70km/h",
            marker_color_circle="black", 
            marker_color_outside="yellow"
        )
        
        distance_km = geodesic(start_coords, end_coords).kilometers
        
        real_time_seconds = (distance_km / 70) * 3600 
        
        sim_time_seconds = real_time_seconds / 50 
        if sim_time_seconds < 1.5: sim_time_seconds = 1.5
        
        total_frames = int(sim_time_seconds * 60)
        
        lat_step = (end_coords[0] - start_coords[0]) / total_frames
        lon_step = (end_coords[1] - start_coords[1]) / total_frames
        
        drone_data = {
            "marker": drone_marker,
            "path": path,
            "citizen_marker": citizen_marker,
            "current_frame": 0,
            "total_frames": total_frames,
            "lat_step": lat_step,
            "lon_step": lon_step,
            "current_lat": start_coords[0],
            "current_lon": start_coords[1]
        }
        
        self.animate_drone(drone_data)

    def animate_drone(self, drone_data):
        if drone_data["current_frame"] < drone_data["total_frames"]:
            drone_data["current_lat"] += drone_data["lat_step"]
            drone_data["current_lon"] += drone_data["lon_step"]
            drone_data["marker"].set_position(drone_data["current_lat"], drone_data["current_lon"])
            
            drone_data["current_frame"] += 1
            
            self.after(16, self.animate_drone, drone_data)
        else:
            drone_data["marker"].set_text("✅ Đã giao")
            
            drone_data["citizen_marker"].marker_color_outside = "green"
            drone_data["citizen_marker"].draw()
            
            self.after(2000, lambda: drone_data["marker"].delete())
            self.after(2000, lambda: drone_data["path"].delete())