# part of the core python gui library
# not importing all of tkinter to save memory and improve performance
import tkinter as tk
from tkinter import ttk

# Window setup
root = tk.Tk()

# Setting window size and title
root.geometry("360x600")
root.title("Bunny Weather App V.3")

# widget setup
# Creating tab control
tab_control = ttk.Notebook(root)

# Creating tabs 5 in total
# Tab Home
tab1 = ttk.Frame(tab_control)
label1 = ttk.Label(tab1, text = "Home")

# Tab Your Report's
tab2 = ttk.Frame(tab_control)
label2 = ttk.Label(tab2, text = "Report Weather")

# Tab Report Weather
tab3 = ttk.Frame(tab_control)
label3 = ttk.Label(tab3, text = "Your Report's")

# Tab Settings
tab4 = ttk.Frame(tab_control)
label4 = ttk.Label(tab4, text = "Settings")

# tab About Application
tab5 = ttk.Frame(tab_control)
label5 = ttk.Label(tab5, text = "About")

# package tab control
tab_control.pack()

# run the application
root.mainloop()
