# part of the core python gui library
# not importing all of tkinter to save memory and improve performance
import tkinter as tk
from tkinter import ttk

# Window setup
root = tk.Tk()

# Setting window size and title
root.geometry("360x600")
root.title("Bunny Weather App V.3")

# Tab Home
# Tab Report Weather
# Tab Your Report's
# Tab Settings
# tab About Application 

# Creating tabs
tab_control = ttk.Notebook(root)
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab3 = ttk.Frame(tab_control)
tab4 = ttk.Frame(tab_control)
tab5 = ttk.Frame(tab_control)
tab_control.add(tab1, text='Home')
tab_control.add(tab2, text='Report Weather')
tab_control.add(tab3, text="Your Report's")
tab_control.add(tab4, text='Settings')  
tab_control.add(tab5, text='About')
tab_control.pack(expand=1, fill='both')

# run the application
root.mainloop()
