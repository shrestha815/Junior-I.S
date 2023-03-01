import tkinter
import customtkinter as tk
import random
import string
import sqlite3 as sq

tk.set_appearance_mode("System")
tk.set_default_color_theme("blue")

# drawing the login window
app = tk.CTk()
app.geometry("600x440")
app.title("Login")


# navigation to the main window
def login():

    app.destroy()
    main_window = tk.CTk()
    main_window.geometry("1920x1080")
    main_window.title("Password Manager")
    main_window_frame = tk.CTkFrame(master= main_window, width=1920,height=1080,corner_radius=15)
    main_window_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
    main_window.mainloop()

def open_new_window():
    app.destroy()
    new_window = tk.CTk()
    new_window.geometry("600x440")
    new_window.title("Password Recovery")

    new_frame = tk.CTkFrame(master=new_window, width=320, height=360, corner_radius=15)
    new_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    password_reset = tk.CTkEntry(master=new_frame, width=220, placeholder_text='Enter new Password', show="*")
    password_reset.place(x=50, y=165)

    validation_entry = tk.CTkEntry(master=new_frame, width=220, placeholder_text='Re-Type Password', show="*")
    validation_entry.place(x=50, y=200)

    new_window.mainloop()



frame = tk.CTkFrame(master=app, width=320, height=360, corner_radius=15)
frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

login_label = tk.CTkLabel(master=frame, text="Enter master password", font=('Open Sans', 19), anchor="e")
login_label.place(x=50, y=45)

password_entry = tk.CTkEntry(master=frame, width=220, placeholder_text='Password', show="*")
password_entry.place(x=50, y=165)

login_button = tk.CTkButton(master=frame, width=220, text="Login", command=login, corner_radius=6)
login_button.place(x=50, y=240)


password_recover = tk.CTkLabel(master=frame, text="Forgot password?", font=('Open Sans', 12))
password_recover.place(x=155, y=195)
password_recover.bind("<Button-1>", lambda e: open_new_window())


app.mainloop()

