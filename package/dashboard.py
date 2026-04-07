import tkinter as tk
from tkinter import ttk

class StatsDashboard(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.stats = {
            "total_need_rescue": 0,
            "low": 0,
            "med": 0,
            "high": 0,
            "extrem": 0,
            "total_rescued_people": 0
        }
        
        ttk.Label(self, text="📊 BẢNG THỐNG KÊ", font=("Arial", 14, "bold")).pack(pady=(10, 5))
        
        self.labels = {}
        
        self.labels["total_need_rescue"] = ttk.Label(self, text=f"Số gia đình cần cứu hộ: {self.stats['total_need_rescue']}", font=("Arial", 10, "bold"))
        self.labels["total_need_rescue"].pack(anchor="w", padx=15, pady=2)
        
        self.labels["low"] = ttk.Label(self, text=f"  🟢 Low (Thấp): {self.stats['low']}")
        self.labels["low"].pack(anchor="w", padx=15, pady=2)
        
        self.labels["med"] = ttk.Label(self, text=f"  🟡 Med (Vừa): {self.stats['med']}")
        self.labels["med"].pack(anchor="w", padx=15, pady=2)
        
        self.labels["high"] = ttk.Label(self, text=f"  🟠 High (Cao): {self.stats['high']}")
        self.labels["high"].pack(anchor="w", padx=15, pady=2)
        
        self.labels["extrem"] = ttk.Label(self, text=f"  🔴 Extrem (Nguy cấp): {self.stats['extrem']}")
        self.labels["extrem"].pack(anchor="w", padx=15, pady=2)
        
        ttk.Separator(self, orient='horizontal').pack(fill='x', pady=5, padx=10)
        
        self.labels["total_rescued_people"] = ttk.Label(self, text=f"Số người đã được cung cấp: {self.stats['total_rescued_people']}", font=("Arial", 10, "bold"), foreground="green")
        self.labels["total_rescued_people"].pack(anchor="w", padx=15, pady=(2, 10))

    def update_new_request(self, danger_level):
        """Gọi hàm này khi có 1 form mới được điền"""
        self.stats["total_need_rescue"] += 1
        
        if danger_level == "low": self.stats["low"] += 1
        elif danger_level == "med": self.stats["med"] += 1
        elif danger_level == "high": self.stats["high"] += 1
        elif danger_level == "extrem": self.stats["extrem"] += 1
        
        self._refresh_labels()

    def update_rescued(self, people_count):
        """Gọi hàm này khi drone bay tới nơi thành công"""
        self.stats["total_need_rescue"] -= 1
        self.stats["total_rescued_people"] += people_count
        self._refresh_labels()

    def _refresh_labels(self):
        """Cập nhật lại text trên giao diện"""
        self.labels["total_need_rescue"].config(text=f"Số gia đình cần cứu hộ: {self.stats['total_need_rescue']}")
        self.labels["low"].config(text=f"  Low (Thấp): {self.stats['low']}")
        self.labels["med"].config(text=f"  Med (Vừa): {self.stats['med']}")
        self.labels["high"].config(text=f"  High (Cao): {self.stats['high']}")
        self.labels["extrem"].config(text=f"  Extrem (Nguy cấp): {self.stats['extrem']}")
        self.labels["total_rescued_people"].config(text=f"Số người đã được cung cấp: {self.stats['total_rescued_people']}")