import customtkinter as ctk
import random
from tkinter import messagebox
from PIL import Image
import requests
from datetime import datetime

# ------------------ Configuration ------------------
# Your WeatherAPI.com Key
API_KEY = "12496438e2544317ba8210933250812"
# Default Location: Chicago (Zip 60601)
DEFAULT_LOCATION = "60601"

# ------------------ Functions ------------------


def show_about():
    messagebox.showinfo(
        "About Bunny Weather App",
        "Bunny Weather App V.3.2\nKephalos LLC\n© 2025 All rights reserved.",
    )


def switch_to_report():
    # Switches the view to the "Report Weather" tab
    tab_view.set("Report Weather")


def get_icon(condition_text):
    """Maps WeatherAPI condition text to emojis"""
    if not condition_text:
        return "☁️"

    # Normalize text to lowercase for easier matching
    cond = condition_text.lower()

    if "sunny" in cond or "clear" in cond:
        return "☀️"
    if "partly cloudy" in cond:
        return "⛅"
    if "cloudy" in cond or "overcast" in cond:
        return "☁️"
    if "mist" in cond or "fog" in cond:
        return "🌫️"
    if "rain" in cond or "drizzle" in cond:
        return "🌧️"
    if "snow" in cond or "blizzard" in cond or "ice" in cond:
        return "❄️"
    if "thunder" in cond:
        return "⚡"

    return "☁️"  # Default fallback


def search_location():
    """Gets the zip from the entry box and loads weather"""
    user_zip = zip_entry.get().strip()
    if user_zip:
        load_weather(user_zip)
    else:
        # If empty, just reload default
        load_weather(DEFAULT_LOCATION)


def load_weather(location=DEFAULT_LOCATION):
    """Fetches weather for the specific location provided using WeatherAPI.com"""
    # Update header to show we are loading
    header_label.configure(text=f"Loading {location}...")

    try:
        # WeatherAPI URL (Forecast endpoint for 2 days to get 24h data)
        # q=location handles Zip Codes automatically
        url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={location}&days=2&aqi=no&alerts=no"

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            # --- 1. Update Current Header ---
            current_temp = data["current"]["temp_f"]
            desc = data["current"]["condition"]["text"]
            location_name = data["location"]["name"]

            header_label.configure(
                text=f"{location_name}\n{int(current_temp)}°F\n{desc}"
            )

            # --- 2. Clear old forecast widgets ---
            for widget in weather_scroll_frame.winfo_children():
                widget.destroy()

            # --- 3. Build 24-hour timeline ---
            now_hour = datetime.now().hour

            # WeatherAPI returns 'forecastday' list. [0] is today, [1] is tomorrow.
            today_hours = data["forecast"]["forecastday"][0]["hour"]
            tomorrow_hours = data["forecast"]["forecastday"][1]["hour"]

            upcoming_hours = []

            # Add today's remaining hours
            for h in today_hours:
                # Time format comes as "YYYY-MM-DD HH:MM"
                time_str = h["time"]
                # Parse the hour integer from the string
                h_dt = datetime.strptime(time_str, "%Y-%m-%d %H:%M")

                if h_dt.hour >= now_hour:
                    upcoming_hours.append(h)

            # Add tomorrow's hours to fill 24 slots if needed
            needed = 24 - len(upcoming_hours)
            if needed > 0:
                upcoming_hours.extend(tomorrow_hours[:needed])

            # --- 4. Display the rows ---
            for item in upcoming_hours:
                time_str = item["time"]  # "2025-12-08 14:00"

                # Format time nicely (e.g., "02:00 PM")
                try:
                    dt_obj = datetime.strptime(time_str, "%Y-%m-%d %H:%M")
                    formatted_time = dt_obj.strftime("%I:%M %p")
                except:
                    formatted_time = time_str

                temp = int(item["temp_f"])
                condition_text = item["condition"]["text"]
                icon = get_icon(condition_text)

                # Create a row frame
                row_frame = ctk.CTkFrame(weather_scroll_frame, fg_color="transparent")
                row_frame.pack(fill="x", pady=5)

                # Time
                ctk.CTkLabel(row_frame, text=formatted_time, width=80, anchor="w").pack(
                    side="left", padx=10
                )
                # Icon
                ctk.CTkLabel(row_frame, text=icon, width=30).pack(side="left", padx=5)
                # Temp
                ctk.CTkLabel(row_frame, text=f"{temp}°F", width=50, anchor="e").pack(
                    side="right", padx=10
                )
        else:
            header_label.configure(text="Error: Location\nNot Found.")
            print("API Error:", response.text)

    except Exception as e:
        print("Crash Error:", e)
        header_label.configure(text="Check Internet\nConnection.")


# ------------------Window setup------------------
app = ctk.CTk()
app.geometry("360x650")
app.title("Bunny Weather App V.3.2")

# ------------------Appearance settings------------------
ctk.set_appearance_mode("system")

# ------------------Creating tab view------------------
tab_view = ctk.CTkTabview(app)
tab_view.pack(expand=True, fill="both")

# ------------------Creating tabs------------------

# --- HOME TAB ---
tab_view.add("Home")
home_tab = tab_view.tab("Home")

# -- Zip Code Input Frame --
input_frame = ctk.CTkFrame(home_tab, fg_color="transparent")
input_frame.pack(pady=(10, 5))

zip_entry = ctk.CTkEntry(input_frame, placeholder_text="Enter Zip Code", width=140)
zip_entry.pack(side="left", padx=5)

search_btn = ctk.CTkButton(
    input_frame, text="Search", width=60, command=search_location
)
search_btn.pack(side="left", padx=5)
# -------------------------------

# Header
header_label = ctk.CTkLabel(
    home_tab, text="Loading...", font=("Arial", 20, "bold"), justify="center"
)
header_label.pack(pady=10)

# Scrollable Frame for Hours
weather_scroll_frame = ctk.CTkScrollableFrame(home_tab, label_text="24-Hour Forecast")
weather_scroll_frame.pack(expand=True, fill="both", padx=10, pady=5)

# Refresh Button
refresh_btn = ctk.CTkButton(home_tab, text="Refresh Weather", command=search_location)
refresh_btn.pack(pady=5)

# "Not Correct" Button -> Links to Report Tab
submit_button_home = ctk.CTkButton(
    home_tab,
    text="Not the Correct Weather? \n Click Here!",
    corner_radius=20,
    fg_color="#FF5733",
    hover_color="#C70039",
    command=switch_to_report,
)
submit_button_home.pack(side="bottom", pady=10)


# --- REPORT WEATHER TAB ---
tab_view.add("Report Weather")
report_tab = tab_view.tab("Report Weather")

ctk.CTkLabel(
    report_tab, text="Report Incorrect Weather", font=("Arial", 18, "bold")
).pack(pady=20)

ctk.CTkLabel(report_tab, text="What is the actual condition?").pack(pady=5)
condition_menu = ctk.CTkOptionMenu(
    report_tab, values=["Sunny", "Rainy", "Cloudy", "Snowy", "Stormy"]
)
condition_menu.pack(pady=5)

ctk.CTkLabel(report_tab, text="What is the actual temperature?").pack(pady=5)
temp_entry = ctk.CTkEntry(report_tab, placeholder_text="e.g. 72")
temp_entry.pack(pady=5)

ctk.CTkLabel(report_tab, text="Additional Comments:").pack(pady=5)
comment_entry = ctk.CTkTextbox(report_tab, height=100)
comment_entry.pack(pady=5, padx=20, fill="x")

submit_button_report = ctk.CTkButton(report_tab, text="Submit Report", corner_radius=20)
submit_button_report.pack(side="bottom", pady=20, anchor="s")


# --- YOUR REPORTS TAB ---
tab_view.add("Your Reports")
your_reports_tab = tab_view.tab("Your Reports")
submit_button_delete = ctk.CTkButton(
    your_reports_tab, text="Delete Report", corner_radius=20
)
submit_button_delete.pack(side="bottom", pady=20, anchor="s")


# --- SETTINGS TAB ---
tab_view.add("Settings")


# --- ABOUT TAB ---
about_tab = tab_view.add("About")
about_button = ctk.CTkButton(
    about_tab, text="About App", corner_radius=20, command=show_about
)
about_button.place(relx=0.5, rely=0.5, anchor="center")

# ------------------Running the application------------------
# Load default weather (60601) after 500ms
app.after(500, lambda: load_weather(DEFAULT_LOCATION))
app.mainloop()
