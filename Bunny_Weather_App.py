import customtkinter as ctk
import random
from tkinter import messagebox, filedialog
from PIL import Image
import requests
from datetime import datetime

# ------------------ Configuration ------------------
API_KEY = "12496438e2544317ba8210933250812"
DEFAULT_LOCATION = "60601"

# Global Variables
current_unit = "F"
saved_reports = []  # List to store reports in memory


# ------------------ Functions ------------------

def show_about():
    messagebox.showinfo(
        "About Bunny Weather App",
        "Bunny Weather App V.3.5\nKephalos LLC\n© 2025 All rights reserved.",
    )


def switch_to_report():
    tab_view.set("Report Weather")


def get_icon(condition_text):
    if not condition_text:
        return "☁️"
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
    if "snow" in cond or "blizzard" in cond:
        return "❄️"
    if "thunder" in cond:
        return "⚡"
    return "☁️"


def search_location():
    user_zip = zip_entry.get().strip()
    if user_zip:
        load_weather(user_zip)
    else:
        load_weather(DEFAULT_LOCATION)


def change_appearance_mode(new_appearance_mode):
    ctk.set_appearance_mode(new_appearance_mode)


def change_unit_event(new_unit):
    global current_unit
    current_unit = new_unit
    search_location()


# --- Report Handling Functions ---


def submit_report():
    """Saves the data from the Report Form to the list"""
    cond = condition_menu.get()
    temp = temp_entry.get()
    comment = comment_entry.get("1.0", "end-1c")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if not temp:
        messagebox.showwarning("Missing Info", "Please enter a temperature.")
        return

    # Create a report dictionary
    new_report = {
        "time": timestamp,
        "condition": cond,
        "temp": temp,
        "comment": comment,
    }

    saved_reports.append(new_report)

    # Clear inputs
    temp_entry.delete(0, "end")
    comment_entry.delete("1.0", "end")
    messagebox.showinfo("Success", "Report Submitted!")

    # Update the View
    update_reports_list()
    tab_view.set("Your Reports")


def update_reports_list():
    """Refreshes the scrollable frame in Your Reports tab"""
    # Clear current list
    for widget in reports_scroll_frame.winfo_children():
        widget.destroy()

    if not saved_reports:
        ctk.CTkLabel(reports_scroll_frame, text="No reports submitted yet.").pack(
            pady=20
        )
        return

    # Add each report as a card
    for i, report in enumerate(saved_reports):
        card = ctk.CTkFrame(reports_scroll_frame, fg_color=("gray85", "gray25"))
        card.pack(fill="x", pady=5, padx=5)

        # Text info
        info_text = f"DATE: {report['time']}\nACTUAL: {report['condition']}, {report['temp']}°\nNOTE: {report['comment']}"
        ctk.CTkLabel(card, text=info_text, justify="left", anchor="w").pack(
            side="left", padx=10, pady=5
        )


def delete_all_reports():
    """Clears the list"""
    if messagebox.askyesno("Delete", "Are you sure you want to delete ALL reports?"):
        saved_reports.clear()
        update_reports_list()


def export_to_txt():
    """Saves reports to a text file"""
    if not saved_reports:
        messagebox.showwarning("Empty", "No reports to export.")
        return

    # Open file dialog
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text file", "*.txt")],
        title="Save Reports",
    )

    if file_path:
        try:
            with open(file_path, "w") as f:
                f.write("--- BUNNY WEATHER APP REPORTS ---\n\n")
                for report in saved_reports:
                    f.write(f"Timestamp: {report['time']}\n")
                    f.write(f"Condition: {report['condition']}\n")
                    f.write(f"Temperature: {report['temp']}\n")
                    f.write(f"Comments: {report['comment']}\n")
                    f.write("-" * 30 + "\n")
            messagebox.showinfo("Success", "Reports exported successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file: {e}")


# --------------------------------------


def load_weather(location=DEFAULT_LOCATION):
    header_label.configure(text=f"Loading {location}...")
    try:
        url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={location}&days=2&aqi=no&alerts=no"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            # Unit Selection
            if current_unit == "F":
                temp_val = data["current"]["temp_f"]
                unit_str = "°F"
            else:
                temp_val = data["current"]["temp_c"]
                unit_str = "°C"

            desc = data["current"]["condition"]["text"]
            location_name = data["location"]["name"]

            header_label.configure(
                text=f"{location_name}\n{int(temp_val)}{unit_str}\n{desc}"
            )

            for widget in weather_scroll_frame.winfo_children():
                widget.destroy()

            now_hour = datetime.now().hour
            today_hours = data["forecast"]["forecastday"][0]["hour"]
            tomorrow_hours = data["forecast"]["forecastday"][1]["hour"]
            upcoming_hours = []

            for h in today_hours:
                h_dt = datetime.strptime(h["time"], "%Y-%m-%d %H:%M")
                if h_dt.hour >= now_hour:
                    upcoming_hours.append(h)

            needed = 24 - len(upcoming_hours)
            if needed > 0:
                upcoming_hours.extend(tomorrow_hours[:needed])

            for item in upcoming_hours:
                time_str = item["time"]
                try:
                    dt_obj = datetime.strptime(time_str, "%Y-%m-%d %H:%M")
                    formatted_time = dt_obj.strftime("%I:%M %p")
                except:
                    formatted_time = time_str

                if current_unit == "F":
                    row_temp = item["temp_f"]
                else:
                    row_temp = item["temp_c"]

                icon = get_icon(item["condition"]["text"])

                row_frame = ctk.CTkFrame(weather_scroll_frame, fg_color="transparent")
                row_frame.pack(fill="x", pady=5)
                ctk.CTkLabel(row_frame, text=formatted_time, width=80, anchor="w").pack(
                    side="left", padx=10
                )
                ctk.CTkLabel(row_frame, text=icon, width=30).pack(side="left", padx=5)
                ctk.CTkLabel(
                    row_frame, text=f"{int(row_temp)}{unit_str}", width=50, anchor="e"
                ).pack(side="right", padx=10)
        else:
            header_label.configure(text="Error: Location\nNot Found.")
    except Exception as e:
        print("Crash Error:", e)
        header_label.configure(text="Check Internet\nConnection.")


# ------------------Window setup------------------
# THIS WAS THE LINE CAUSING THE ERROR: FIXED! I did not have ctk capatalized after the ctk. for the window. 
app = ctk.CTk()

app.geometry("360x650")
app.title("Bunny Weather App V.3.5")
ctk.set_appearance_mode("System")

# ------------------Creating tab view------------------
tab_view = ctk.CTkTabview(app)
tab_view.pack(expand=True, fill="both")

# --- HOME TAB ---
tab_view.add("Home")
home_tab = tab_view.tab("Home")

# tab frame
input_frame = ctk.CTkFrame(home_tab)
input_frame.pack(pady=(10, 5))

# Allows the person to enter their zipcode for accurate weather. 
zip_entry = ctk.CTkEntry(input_frame, placeholder_text="Enter Zip Code", width=140)
zip_entry.pack(side="left", padx=5)

# Search Button
search_btn = ctk.CTkButton(
    input_frame, text="Search", width=60, command=search_location
)
search_btn.pack(side="left", padx=5)

header_label = ctk.CTkLabel(
    home_tab, text="Loading...", font=("Arial", 20, "bold"), justify="center"
)
header_label.pack(pady=10)

# The 24 hr weather scroll. 
weather_scroll_frame = ctk.CTkScrollableFrame(home_tab, label_text="24-Hour Forecast")
weather_scroll_frame.pack(expand=True, fill="both", padx=10, pady=5)

# Refresh button
refresh_btn = ctk.CTkButton(home_tab, text="Refresh Weather", command=search_location)
refresh_btn.pack(pady=5)

submit_button_home = ctk.CTkButton(
    home_tab,
    text="Not the Correct Weather? \n Click Here!",
    corner_radius=20,
    
    # Button Color
    fg_color="#FF334B",
    # Hover Color
    hover_color="#C70039",
    # Goes to the Report Weather Tab
    command=switch_to_report,
)
submit_button_home.pack(side="bottom", pady=10)


# --- REPORT WEATHER TAB ---

# Report Weather Tab
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

submit_button_report = ctk.CTkButton(
    report_tab, text="Submit Report", corner_radius=20, command=submit_report
)
submit_button_report.pack(side="bottom", pady=20, anchor="s")


# --- YOUR REPORTS TAB ---
tab_view.add("Your Reports")
your_reports_tab = tab_view.tab("Your Reports")

reports_scroll_frame = ctk.CTkScrollableFrame(
    your_reports_tab, label_text="Saved Reports"
)
reports_scroll_frame.pack(expand=True, fill="both", padx=10, pady=10)

btn_frame = ctk.CTkFrame(your_reports_tab, fg_color="transparent")
btn_frame.pack(side="bottom", pady=20)
export_btn = ctk.CTkButton(
    btn_frame, text="Export TXT", fg_color="green", command=export_to_txt
)
export_btn.pack(side="left", padx=5)
delete_btn = ctk.CTkButton(
    btn_frame, text="Delete All", fg_color="red", command=delete_all_reports
)
delete_btn.pack(side="left", padx=5)


# --- SETTINGS TAB ---
tab_view.add("Settings")
settings_tab = tab_view.tab("Settings")
ctk.CTkLabel(settings_tab, text="Appearance Mode:", font=("Arial", 14, "bold")).pack(
    pady=(20, 5)
)
appearance_mode_menu = ctk.CTkSegmentedButton(
    settings_tab, values=["Light", "Dark", "System"], command=change_appearance_mode
)
appearance_mode_menu.pack(pady=5)
appearance_mode_menu.set("System")
ctk.CTkLabel(settings_tab, text="Temperature Unit:", font=("Arial", 14, "bold")).pack(
    pady=(20, 5)
)
unit_menu = ctk.CTkSegmentedButton(
    settings_tab, values=["F", "C"], command=change_unit_event
)
unit_menu.pack(pady=5)
unit_menu.set("F")


# --- ABOUT TAB ---
tab_view.add("About")
ctk.CTkButton(
    tab_view.tab("About"), text="About App", corner_radius=20, command=show_about
).place(relx=0.5, rely=0.5, anchor="center")

# ------------------Run------------------
app.after(500, lambda: load_weather(DEFAULT_LOCATION))
app.mainloop()