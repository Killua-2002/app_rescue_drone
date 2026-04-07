import tkinter as tk
from tkinter import ttk
from datetime import datetime
from app_rescue_drone.package.citizen import save_citizen_request
from app_rescue_drone.package.lib import calculate_danger_level

class CitizenForm(tk.Frame):
    def __init__(self, parent, map_callback, dash_callback):
        super().__init__(parent)
        self.map_callback = map_callback
        self.dash_callback = dash_callback
        super().__init__(parent)
        self.map_callback = map_callback
        
        ttk.Label(self, text="YÊU CẦU CỨU HỘ", font=("Arial", 14, "bold")).pack(pady=10)
        
        self.entries = {}
        fields = {"address": "Địa chỉ", "total": "Tổng số người", "ill": "Số người bệnh", 
                  "elderly": "Số người già", "children": "Số trẻ em"}
        
        for key, label_text in fields.items():
            frame = tk.Frame(self)
            frame.pack(fill="x", padx=10, pady=5)
            ttk.Label(frame, text=label_text, width=15).pack(side="left")
            entry = ttk.Entry(frame)
            entry.pack(side="right", expand=True, fill="x")
            self.entries[key] = entry
            
        ttk.Button(self, text="Gửi Yêu Cầu", command=self.submit).pack(pady=20)

    def submit(self):
        
        address = self.entries["address"].get()
        total = int(self.entries["total"].get() or 0)
        ill = int(self.entries["ill"].get() or 0)
        old = int(self.entries["elderly"].get() or 0)
        young = int(self.entries["children"].get() or 0)
        
        dl_text, color = calculate_danger_level(ill, young, old, total)
        
        data = {
            "time_collect": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total": total, "ill": ill, "address": address, "elderly": old, 
            "children": young, "danger_level": dl_text, 
            "status_before": "waiting", "time_rescuse": ""
        }
        
        save_citizen_request(data)
        self.map_callback(data, color)
        save_citizen_request(data)
        self.map_callback(data, color)
        
        self.dash_callback(dl_text)