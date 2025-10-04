import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.network.urlrequest import UrlRequest
from kivy.utils import platform
from kivy.core.window import Window
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem

# --- mobile experience ---
#if platform != "android" and platform != "ios":
#    Window.size = (400, 700)


class bunny_weather_app(App):
    """
    The main class for the Bunny Weather App.
    It handles UI creation, API requests, and user interactions.
    """

    def build(self):
        """
        Build the user interface for the application with a TabbedPanel.
        """


        # --- Main Layout: Tabbed Panel ---
        self.root = TabbedPanel(do_default_tab=False)

        # --- Tab 1: Weather Search ---
        tab_weather = TabbedPanelItem(text="Weather")
        weather_layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        search_bar_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        self.city_input = TextInput(
            hint_text="Enter City Name",
            multiline=False,
            font_size=20,
            size_hint_x=0.7,
            background_color=(1, 1, 1, 0.8),
            foreground_color=(0, 0, 0, 1),
        )
        search_button = Button(
            text="Search",
            size_hint_x=0.3,
            background_color=(0.2, 0.6, 0.8, 1),
            color=(1, 1, 1, 1),
            font_size=20,
        )
        search_button.bind(on_press=self.search_weather)
        search_bar_layout.add_widget(self.city_input)
        search_bar_layout.add_widget(search_button)
        weather_layout.add_widget(search_bar_layout)

        self.weather_label = Label(
            text="Enter a city to see the weather.",
            font_size=24,
            color=(0.1, 0.1, 0.1, 1),
            align="center",
            valign="middle",
        )
        weather_layout.add_widget(self.weather_label)
        tab_weather.add_widget(weather_layout)
        self.root.add_widget(tab_weather)

        # --- Tab 2: Live Reports ---
        tab_reports = TabbedPanelItem(text="Live Reports")
        reports_page_layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        reports_page_layout.add_widget(
            Label(
                text="Live Reports from Users",
                size_hint_y=None,
                height=40,
                font_size=22,
                bold=True,
                color=(0.2, 0.2, 0.2, 1),
            )
        )
        scroll_view = ScrollView(size_hint=(1, 1))
        self.reports_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.reports_layout.bind(minimum_height=self.reports_layout.setter("height"))
        scroll_view.add_widget(self.reports_layout)
        reports_page_layout.add_widget(scroll_view)
        tab_reports.add_widget(reports_page_layout)
        self.root.add_widget(tab_reports)

        # --- Tab 3: Submit Report ---
        tab_submit = TabbedPanelItem(text="Submit")
        user_input_layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        self.name_input = TextInput(
            hint_text="Your Name (Optional)", size_hint_y=None, height=40, font_size=18
        )
        self.report_input = TextInput(
            hint_text="What's the weather like where you are?", font_size=18
        )
        submit_button = Button(
            text="Submit Report",
            size_hint_y=None,
            height=50,
            background_color=(0.1, 0.7, 0.3, 1),  # A nice green
            color=(1, 1, 1, 1),
            font_size=20,
        )
        submit_button.bind(on_press=self.submit_report)
        user_input_layout.add_widget(self.name_input)
        user_input_layout.add_widget(self.report_input)
        user_input_layout.add_widget(submit_button)
        tab_submit.add_widget(user_input_layout)
        self.root.add_widget(tab_submit)

        # --- Tab 4: Settings ---
        tab_Settings = TabbedPanelItem(text="Settings")
        Settings_text = (
            "[b]Bunny Weather App[/b]\n\n"
            "Version 1.1\n\n"
            "Work in Progress"
            "This app provides real-time weather data "
            "powered by OpenWeatherMap and allows users "
            "to share their own local weather observations."
        )
        Settings_label = Label(
            text=Settings_text,
            font_size=18,
            color=(0.1, 0.1, 0.1, 1),
            align="center",
            valign="middle",
            padding=(20, 20),
            markup=True,
        )
        tab_Settings.add_widget(Settings_label)
        self.root.add_widget(tab_Settings)

        # Set the default tab to be the first one
        self.root.switch_to(tab_weather)

        return self.root

    def search_weather(self, instance):
        """
        Called when the search button is pressed.
        It fetches weather data for the entered city. 
        """
        # no API yet
        city = self.city_input.text.strip()
        if not city:
            self.weather_label.text = "Please enter a city name."
            return

        if self.api_key == "YOUR_API_KEY_HERE":
            self.weather_label.text = (
                "Error:\nPlease set your OpenWeatherMap API key in the main.py file."
            )
            return

        # Construct the API URL
        url = f"API URL"
        UrlRequest(
            url,
            on_success=self.update_weather,
            on_failure=self.show_error,
            on_error=self.show_error,
        )
        self.weather_label.text = f"Searching for {city}..."

    def update_weather(self, request, result):
        """
        Callback function for a successful API request.
        Updates the weather label with the fetched data.
        """
        try:
            name = result["name"]
            country = result["sys"]["country"]
            temp = result["main"]["temp"]
            condition = result["weather"][0]["description"].capitalize()
            self.weather_label.text = f"{name}, {country}\n{temp}°C\n{condition}"
        except KeyError:
            self.weather_label.text = "Could not find weather data for that city."
        except Exception as e:
            self.weather_label.text = f"An error occurred: {e}"

    def show_error(self, request, error):
        """
        Callback function for a failed or errored API request.
        """
        self.weather_label.text = "Error: Could not connect or find city.\nPlease check your spelling and connection."
        print(f"API Request Error: {error}")

    def submit_report(self, instance):
        """
        Called when the submit button is pressed.
        Adds a user's weather report to the scrollable list.
        """
        name = self.name_input.text.strip() or "Anonymous"
        report_text = self.report_input.text.strip()

        if not report_text:
            return  # Don't submit an empty report

        # Create a formatted label for the new report
        report_widget = Label(
            text=f"[b]{name} says:[/b]\n{report_text}",
            font_size=18,
            color=(0, 0, 0, 1),
            size_hint_y=None,
            height=80,
            markup=True,
            padding=(10, 10),
        )

        # Add a background to the report label
        with report_widget.canvas.before:
            from bunny_weather_app import Color, RoundedRectangle

            Color(0.85, 0.85, 0.9, 1)  # A light grey-blue
            RoundedRectangle(
                pos=report_widget.pos, size=report_widget.size, radius=[10]
            )

        # Bind position and size updates
        report_widget.bind(pos=self._update_report_bg, size=self._update_report_bg)

        # Add to the layout (at the top)
        self.reports_layout.add_widget(
            report_widget, index=len(self.reports_layout.children)
        )

        # Clear input fields
        self.name_input.text = ""
        self.report_input.text = ""

        # Switch to the reports tab to show the new submission
        # The second tab is at index 1 (0-indexed list of children)
        if len(self.root.tab_list) > 1:
            self.root.switch_to(self.root.tab_list[1])

    def _update_report_bg(self, instance, value):
        """
        Update the background of the report widget when its size or position changes.
        """
        instance.canvas.before.clear()
        with instance.canvas.before:
            from bunny_weather_app.graphics import Color, RoundedRectangle

            Color(0.85, 0.85, 0.9, 1)
            RoundedRectangle(pos=instance.pos, size=instance.size, radius=[10])


if __name__ == "__main__":
    bunny_weather_app().run()
