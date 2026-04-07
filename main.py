import tkinter as tk
from package.citizen import init_csv
from package.form import CitizenForm
from package.maps import RescueMap
from package.dashboard import StatsDashboard

def main():
    init_csv()
    
    root = tk.Tk()
    root.title("Hệ Thống Phân Phối Drone Cứu Hộ")
    root.geometry("1200x700")
    
    left_frame = tk.Frame(root, width=300, bg="lightgray")
    left_frame.pack(side="left", fill="y")
    left_frame.pack_propagate(False)
    
    right_frame = tk.Frame(root)
    right_frame.pack(side="right", fill="both", expand=True)
    
    dashboard_view = StatsDashboard(left_frame)
    dashboard_view.pack(fill="x")
    
    map_view = RescueMap(right_frame)
    map_view.pack(fill="both", expand=True)
    
    form_view = CitizenForm(
        left_frame, 
        map_callback=map_view.add_citizen_request,
        dash_callback=dashboard_view.update_new_request
    )
    form_view.pack(fill="both", expand=True)

    root.mainloop()

if __name__ == "__main__":
    main()