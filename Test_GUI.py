# part of the core python gui library
# not importing all of tkinter to save memory and improve performance
import tkinter as tk
import ttkbootstrap as ttk

# Window setup
window = tkk.window(themename ='darkly')


# Setting window size and title
window.geometry("360x600")
window.title("Bunny Weather App V.3")

# widget setup
# Creating tab control
tab_control = ttk.Notebook(window)

# Creating tabs 5 in total
# Tab Home
tab1 = ttk.Frame(tab_control)
tab_control.add(tab1, text = "Home")

# Tab Your Report's
tab2 = ttk.Frame(tab_control)
tab_control.add(tab2, text = "Report Weather")
button2 = ttk.Button(tab2, text="Submit Report")
button2.pack()

# Tab Report Weather
tab3 = ttk.Frame(tab_control)
tab_control.add(tab3, text = "Your Report's")

# Tab Settings
tab4 = ttk.Frame(tab_control)
tab_control.add(tab4, text = "Settings")

# tab About Application
tab5 = ttk.Frame(tab_control)
tab_control.add(tab5, text= "About")

# package tab control
tab_control.pack()

# run the application
window.mainloop()
