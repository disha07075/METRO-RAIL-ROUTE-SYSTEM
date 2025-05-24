import tkinter as tk
from tkinter import ttk, messagebox
import tkintermapview

class MetroSystem:
    def __init__(self):
        self.fare_per_minute = 2.0
        self.stations = {
            0: ("Rajiv Chowk", (28.6326, 77.2191)),
            1: ("Kashmere Gate", (28.6667, 77.2383)),
            2: ("Central Secretariat", (28.6129, 77.2273)),
            3: ("New Delhi", (28.6448, 77.2167)),
            4: ("Chandni Chowk", (28.6507, 77.2334)),
            5: ("AIIMS", (28.5672, 77.2100)),
            6: ("INA", (28.5904, 77.2167)),
            7: ("Hauz Khas", (28.5494, 77.2047)),
            8: ("Saket", (28.5221, 77.2073)),
            9: ("Malviya Nagar", (28.5455, 77.1943)),
            10: ("Lajpat Nagar", (28.5719, 77.2475)),
            11: ("Moolchand", (28.5740, 77.2437)),
            12: ("Nehru Place", (28.5507, 77.2614)),
            13: ("Kalkaji Mandir", (28.5517, 77.2595)),
            14: ("Govindpuri", (28.5355, 77.2671)),
            15: ("Okhla", (28.5447, 77.2684)),
            16: ("Jasola", (28.5470, 77.2731)),
            17: ("Sarita Vihar", (28.5345, 77.2794)),
            18: ("Mohan Estate", (28.5183, 77.2856)),
            19: ("Badarpur Border", (28.4706, 77.2912)),
        }

        # Adjacency list: station_id -> list of (neighbor_id, travel_time_minutes)
        self.adj_list = {
            0: [(1,4)],
            1: [(0,4),(2,5)],
            2: [(1,5),(3,3)],
            3: [(2,3),(4,6)],
            4: [(3,6),(5,4)],
            5: [(4,4),(6,7)],
            6: [(5,7),(7,5)],
            7: [(6,5),(8,6)],
            8: [(7,6),(9,4)],
            9: [(8,4),(10,5)],
            10: [(9,5),(11,8)],
            11: [(10,8),(12,5)],
            12: [(11,5),(13,3)],
            13: [(12,3),(14,6)],
            14: [(13,6),(15,4)],
            15: [(14,4),(16,5)],
            16: [(15,5),(17,6)],
            17: [(16,6),(18,4)],
            18: [(17,4),(19,7)],
            19: [(18,7)],
        }

    def get_station_names(self):
        return [self.stations[i][0] for i in range(len(self.stations))]

    def get_station_id_by_name(self, name):
        for i, (n, _) in self.stations.items():
            if n == name:
                return i
        return None

    def dijkstra(self, start, end):
        import heapq
        n = len(self.stations)
        dist = [float('inf')] * n
        parent = [-1] * n
        dist[start] = 0
        pq = [(0, start)]

        while pq:
            cd, u = heapq.heappop(pq)
            if cd > dist[u]:
                continue
            if u == end:
                break
            for v, w in self.adj_list.get(u, []):
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    parent[v] = u
                    heapq.heappush(pq, (dist[v], v))

        if dist[end] == float('inf'):
            return None, None
        path = []
        cur = end
        while cur != -1:
            path.append(cur)
            cur = parent[cur]
        path.reverse()
        return path, dist[end]

    def get_coords_for_path(self, path):
        return [self.stations[station_id][1] for station_id in path]

    def calculate_fare(self, time):
        return time * self.fare_per_minute

    def update_fare(self, new_fare):
        if new_fare > 0:
            self.fare_per_minute = new_fare
            return True
        return False


class MetroApp:
    def __init__(self, root):
        self.metro = MetroSystem()
        self.root = root
        root.title("Delhi Metro Route Planner")

        # Map Widget
        self.map_widget = tkintermapview.TkinterMapView(root, width=800, height=600, corner_radius=0)
        self.map_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.map_widget.set_position(28.61, 77.23)  # Center on Delhi
        self.map_widget.set_zoom(11)

        # Control Panel Frame
        self.control_frame = tk.Frame(root, padx=10, pady=10)
        self.control_frame.pack(side=tk.RIGHT, fill=tk.Y)

        # Start station dropdown
        tk.Label(self.control_frame, text="Select Start Station:").pack(anchor="w")
        self.start_var = tk.StringVar()
        self.start_combo = ttk.Combobox(self.control_frame, textvariable=self.start_var)
        self.start_combo['values'] = self.metro.get_station_names()
        self.start_combo.pack(fill=tk.X, pady=5)

        # End station dropdown
        tk.Label(self.control_frame, text="Select End Station:").pack(anchor="w")
        self.end_var = tk.StringVar()
        self.end_combo = ttk.Combobox(self.control_frame, textvariable=self.end_var)
        self.end_combo['values'] = self.metro.get_station_names()
        self.end_combo.pack(fill=tk.X, pady=5)

        # Fare input
        tk.Label(self.control_frame, text=f"Fare Rate (₹ per minute):").pack(anchor="w")
        self.fare_var = tk.StringVar(value=str(self.metro.fare_per_minute))
        self.fare_entry = ttk.Entry(self.control_frame, textvariable=self.fare_var)
        self.fare_entry.pack(fill=tk.X, pady=5)

        self.update_fare_button = ttk.Button(self.control_frame, text="Update Fare", command=self.update_fare)
        self.update_fare_button.pack(pady=(0, 10))

        # Find route button
        self.find_route_button = ttk.Button(self.control_frame, text="Find Route", command=self.find_route)
        self.find_route_button.pack(pady=(0, 10))

        # Route info display
        self.route_info = tk.Text(self.control_frame, height=10, width=40, state=tk.DISABLED)
        self.route_info.pack()

        # Keep track of markers and path line
        self.current_markers = []
        self.current_path_line = None

    def update_fare(self):
        try:
            new_fare = float(self.fare_var.get())
            if new_fare <= 0:
                raise ValueError
            self.metro.update_fare(new_fare)
            messagebox.showinfo("Success", f"Fare rate updated to ₹{new_fare:.2f} per minute.")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid positive number for fare rate.")

    def find_route(self):
        start_name = self.start_var.get()
        end_name = self.end_var.get()

        if not start_name or not end_name:
            messagebox.showwarning("Input Error", "Please select both start and end stations.")
            return
        if start_name == end_name:
            messagebox.showinfo("Input Error", "Start and destination stations are the same. Please select different stations.")
            return

        start_id = self.metro.get_station_id_by_name(start_name)
        end_id = self.metro.get_station_id_by_name(end_name)
        if start_id is None or end_id is None:
            messagebox.showerror("Error", "Invalid station selected.")
            return

        path, total_time = self.metro.dijkstra(start_id, end_id)
        if path is None:
            messagebox.showerror("No Route", f"No route found between {start_name} and {end_name}.")
            return

        self.display_route(path, total_time)

    def display_route(self, path, total_time):
        # Clear old markers and path line
        for marker in self.current_markers:
            marker.delete()
        self.current_markers.clear()
        if self.current_path_line:
            self.current_path_line.delete()
            self.current_path_line = None

        coords = self.metro.get_coords_for_path(path)

        # Add markers
        for station_id in path:
            name, (lat, lon) = self.metro.stations[station_id]
            marker = self.map_widget.set_marker(lat, lon, text=name)
            self.current_markers.append(marker)

        # Draw path line
        self.current_path_line = self.map_widget.set_path(coords)

        # Calculate fare
        fare = self.metro.calculate_fare(total_time)

        # Display route info
        route_names = " -> ".join(self.metro.stations[s][0] for s in path)
        self.route_info.config(state=tk.NORMAL)
        self.route_info.delete("1.0", tk.END)
        self.route_info.insert(tk.END, f"Route:\n{route_names}\n\n")
        self.route_info.insert(tk.END, f"Total Travel Time: {total_time} minutes\n")
        self.route_info.insert(tk.END, f"Fare: ₹{fare:.2f}")
        self.route_info.config(state=tk.DISABLED)

        # Center map on start station
        start_lat, start_lon = coords[0]
        self.map_widget.set_position(start_lat, start_lon)
        self.map_widget.set_zoom(13)


if __name__ == "__main__":
    root = tk.Tk()
    app = MetroApp(root)
    root.mainloop()
