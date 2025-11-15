from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
# pyright: ignore[reportMissingImports]

# Set the window size
Window.size = (350, 600)

kv = """
MDScreen:
    md_bg_color: 0.9, 0.9, 1, 1 # Light blue/purple background like mockup

    MDBottomNavigation:
        # Tab 1: Home
        MDBottomNavigationItem:
            name: 'screen 1'
            text: 'Home'
            icon: 'home.png'  # Changed icon to match 'Home'

            MDFloatLayout:
                # --- Chicago Weather Card ---
                MDCard:
                    size_hint: .8, .4
                    pos_hint: {"center_x": .5, "center_y": .6}
                    padding: "24dp"
                    spacing: "12dp"
                    orientation: 'vertical'
                    md_bg_color: 1, 1, 1, 1
                    radius: [20, 20, 20, 20]
                    elevation: 8

                    MDLabel:
                        text: 'Chicago'
                        halign: 'center'
                        font_style: 'H5'
                        theme_text_color: "Primary"
                        bold: True

                    Image:
                        # Using 'partly-cloudy.png' as a placeholder for the sun icon
                        # This file was in your new upload list.
                        source: 'partly-cloudy.png'
                        size_hint_y: .4

                    MDLabel:
                        text: "72°F"
                        halign: 'center'
                        font_style: 'H3'
                        bold: True

                    MDLabel:
                        text: "Sunny & Happy"
                        halign: 'center'
                        font_style: 'Subtitle1'
                        theme_text_color: "Secondary"

                MDTextButton:
                    text: "Is this wrong? Help us"
                    pos_hint: {"center_x": .5, "center_y": .28}
                    font_style: 'Subtitle2'


        # Tab 2: Report Weather
        MDBottomNavigationItem:
            name: 'screen 2'
            text: 'Report'
            icon: 'report.png'  # Changed icon to match 'Report'

            MDFloatLayout:
                # --- Report Weather Card ---
                MDCard:
                    size_hint: .8, .6
                    pos_hint: {"center_x": .5, "center_y": .5}
                    padding: "24dp"
                    spacing: "12dp"
                    orientation: 'vertical'
                    md_bg_color: 1, 1, 1, 1
                    radius: [20, 20, 20, 20]
                    elevation: 8

                    MDLabel:
                        text: 'Report Weather!'
                        halign: 'center'
                        font_style: 'H5'
                        bold: True
                        color: (1, 0.4, 0.6, 1) # Pinkish color

                    MDTextField:
                        id: temp_field
                        hint_text: "Current Temp (°F)"
                        helper_text: "e.g., 75"
                        mode: "outlined"
                        radius: [10, 10, 10, 10]

                    MDLabel:
                        text: "Conditions"
                        font_style: 'Subtitle1'
                        padding_y: "12dp"

                    # Using a Spinner for the dropdown.
                    MDSpinner:
                        id: conditions_spinner
                        text: "Sunny" # Default value
                        # UPDATED values based on your new uploaded images
                        values: ["Sunny.png", "partly-cloudy.png", "clouds.png", "rain-cloud.png", "rainfall.png", "snow.png", "stormy.png"]
                        sync_height: True

                    MDRaisedButton:
                        text: "Submit! (Ty!! ✨)"
                        pos_hint: {'center_x': 0.5}
                        md_bg_color: (0.2, 0.8, 0.2, 1) # Greenish color
                        on_release: app.submit_report()
                        elevation: 4
                        radius: [15, 15, 15, 15]


        # Tab 3: Your Reports
        MDBottomNavigationItem:
            name: 'screen 3'
            text: 'Reports'
            icon: 'calendar-text-outline' 

            MDFloatLayout:
                # --- Your Reports Card ---
                MDCard:
                    size_hint: .8, .4
                    pos_hint: {"center_x": .5, "center_y": .6}
                    padding: "24dp"
                    spacing: "12dp"
                    orientation: 'vertical'
                    md_bg_color: 1, 1, 1, 1
                    radius: [20, 20, 20, 20]
                    elevation: 8
                    
                    MDLabel:
                        text: "Your Reports"
                        halign: 'center'
                        font_style: 'H5'
                        bold: True
                        theme_text_color: "Primary"

                    # REPLACED MDIcon with your uploaded Image
                    Image:
                        source: 'pass-fai.png'
                        size_hint_y: .5 # Adjusted size
                        allow_stretch: True
                        keep_ratio: True

                    MDLabel:
                        text: "You haven't reported anything yet!"
                        halign: 'center'
                        font_style: 'Subtitle1'
                        theme_text_color: "Secondary"

        # Tab 4: Settings
        MDBottomNavigationItem:
            name: 'screen 4'
            text: 'Settings'
            icon: 'submit.png' # Changed icon to match 'Settings'

            MDFloatLayout:
                # --- Settings Card ---
                MDCard:
                    size_hint: .8, .4
                    pos_hint: {"center_x": .5, "center_y": .6}
                    padding: "24dp"
                    spacing: "12dp"
                    orientation: 'vertical'
                    md_bg_color: 1, 1, 1, 1
                    radius: [20, 20, 20, 20]
                    elevation: 8

                    MDLabel:
                        text: "Settings"
                        halign: 'center'
                        font_style: 'H5'
                        bold: True
                        color: (0.6, 0.2, 0.8, 1) # Purplish color

                    # REPLACED MDIcon with your uploaded Image
                    Image:
                        source: 'admin.png'
                        size_hint_y: .5 # Adjusted size
                        allow_stretch: True
                        keep_ratio: True

                    MDLabel:
                        text: "Settings are hiding! \n(Just kidding, there are none yet!)"
                        halign: 'center'
                        font_style: 'Subtitle1'
                        theme_text_color: "Secondary"
"""


class WeatherApp(MDApp):

    def build(self):

        self.theme_cls.primary_palette = "Blue"
        return Builder.load_string(kv)

    def submit_report(self):
        # placeholder function for your submit button
        print("Report submitted!")
        pass

# needed to run the app
if __name__ == "__main__":
    WeatherApp().run()