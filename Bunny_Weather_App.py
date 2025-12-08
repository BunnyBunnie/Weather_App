import customtkinter as ctk
import random
from tkinter import messagebox
from PIL import Image

# Function to show an about message box
def show_about():
    messagebox.showinfo(
        "About Bunny Weather App",
        "Bunny Weather App V.3\nKephalos LLC\n© 2025 All rights reserved.",
    )

# ------------------Window setup------------------
app = ctk.CTk()
app.geometry("360x600")
app.title("Bunny Weather App V.3")      

# ------------------Appearance settings------------------
ctk.set_appearance_mode("system")

# ------------------Creating tab view------------------
tab_view = ctk.CTkTabview(app)      
tab_view.pack(expand=True, fill="both")

# ------------------Creating tabs------------------

# Adding tabs to the tab view HOME
tab_view.add("Home")
report_tab = tab_view.tab("Home")
submit_button = ctk.CTkButton(report_tab, text="Not the Correct Weather? \n Click Here!", corner_radius=20)
submit_button.pack(side="bottom", pady=20, anchor="s")
submit_button.pack(pady=20)

# Adding tabs to the tab view REPORT WEATHER
tab_view.add("Report Weather")

# Ctk Button Submit Report
report_tab = tab_view.tab("Report Weather")
submit_button = ctk.CTkButton(report_tab, text="Submit Report", corner_radius=20)
submit_button.pack(side="bottom", pady=20, anchor="s")
submit_button.pack(pady=20)

# Adding tabs to the tab view YOUR REPORTS
tab_view.add("Your Reports")
report_tab = tab_view.tab("Your Reports")
submit_button = ctk.CTkButton(report_tab, text="Delete Report", corner_radius=20)
submit_button.pack(side="bottom", pady=20, anchor="s")
submit_button.pack(pady=20)

# Adding tabs to the tab view SETTINGS
tab_view.add("Settings")


# ------------------Adding a button in the About tab to show the about message box------------------

# Adding tabs to the tab view ABOUT
# Create the tab
about_tab = tab_view.add("About")

# Create the About Button
# (Make sure command=show_about matches a function you defined earlier)
about_button = ctk.CTkButton(
    about_tab, 
    text="About App", 
    corner_radius=20, 
    command=show_about
)

# Center it
# We use about_button here, NOT submit_button
about_button.place(relx=0.5, rely=0.5, anchor="center")

# ------------------Running the application------------------

# Runs the application
app.mainloop()      
