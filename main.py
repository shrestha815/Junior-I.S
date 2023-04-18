import tkinter
from tkinter import ttk
import customtkinter as tk
import random
import string
import sqlite3 as sq
import traceback
import sys


#tasks create a table for passwords, display table in stored passwords window, login validation

def init_db():
    try:
        database_connection = sq.connect('password_database.db')
        cursor = database_connection.cursor()
        print("Connection Successful")

        table_creation_query = """CREATE TABLE user_passwords (
                                username text,
                                password text,
                                email text 
            );"""

        #table_insertion_query = "INSERT INTO user_passwords VALUES('shrestha815','password','sshrestha24@wooster.edu')"
        cursor.execute(table_creation_query)
        database_connection.commit()
        database_connection.close()

    except sq.Error as error:
        print("Failure to connect")


class App(tk.CTk):
    def __init__(self):
        super().__init__()

        # main_window
        self.title("Password Manager")
        self.geometry("600x440")
        self.main_window()
        self._set_appearance_mode("System")

    def login(self):
        self.withdraw()
        main_window = tk.CTkToplevel(self)
        main_window.geometry('700x520')
        main_window.title("Password Manager")
        init_db()



    def password_recovery_window(self):
        self.withdraw()
        window = tk.CTkToplevel(self)
        window.geometry('700x520')
        window.title("Recover Password")

        recovery_frame = tk.CTkFrame(master=window, width=320, height=360, corner_radius=15)
        recovery_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        label_recovery_window = tk.CTkLabel(master=window, text="Recover Password", anchor='n', font=('Open Sans', 25))
        label_recovery_window.pack(padx=10, pady=5, fill='both')

        password_recovery = tk.CTkEntry(master=recovery_frame, width=220, placeholder_text= "Enter New Password")

    def main_window(self):

        frame = tk.CTkFrame(master=self, width=320, height=360, corner_radius=15)
        frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        login_label = tk.CTkLabel(master=frame, text="Enter Master Password", font=('Open Sans', 19), anchor="center")
        login_label.place(x=55, y=45)

        password_entry = tk.CTkEntry(master=frame, width=220, placeholder_text='Password', show="*")
        password_entry.place(x=50, y=165)

        login_button = tk.CTkButton(master=frame, width=220, text="Login", command=self.login, corner_radius=6)
        login_button.place(x=50, y=240)

        password_recover = tk.CTkLabel(master=frame, text="Forgot password?", font=('Open Sans', 12))
        password_recover.place(x=155, y=195)
        password_recover.bind("<Button-1>", lambda e: self.password_recovery_window())




if __name__ == "__main__":
    app = App()
    app.mainloop()


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
    main_window.geometry('700x520')
    main_window.title("Password Manager")

    # widgets

    label_main_window = tk.CTkLabel(main_window, text="Stored Passwords", anchor='n', font=('Open Sans', 20))
    label_main_window.pack(padx=10, pady=(40, 20), fill='both')

    table = ttk.Treeview(main_window)
    table.place(relx=0.5, rely=0.5, width=646, height=410, anchor=tkinter.CENTER)

    table.configure(
        columns=(
            "Username"
            "Password"
        )
    )

    main_window.mainloop()


def open_new_window():
    app.destroy()
    new_window = tk.CTk()
    new_window.geometry("750x450")
    new_window.title("Password Recovery")
    label_new_window = tk.CTkLabel(new_window, text="Recover Password", anchor='n', font=('Open Sans', 25))
    label_new_window.pack(padx=10, pady=5, fill='both')

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


def generate_password_window():
    print("Generated Password: ", password_generator(16))


def password_generator(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    generated_password = ''.join(random.choice(characters) for i in range(length))
    return generated_password


password_generation = tk.CTkButton(master=frame, width=220, text="Generate a Password",
                                   command=generate_password_window, corner_radius=6)
password_generation.place(x=50, y=290)

password_recover = tk.CTkLabel(master=frame, text="Forgot password?", font=('Open Sans', 12))
password_recover.place(x=155, y=195)
password_recover.bind("<Button-1>", lambda e: open_new_window())

print("")

app.mainloop()

