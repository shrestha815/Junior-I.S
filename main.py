# Required Imports
import tkinter
from tkinter import ttk
import customtkinter as tk
import random
import string
import sqlite3 as sq
import traceback
import sys

# Function that initializes the database, creating the database and the required tables.


def init_db():
    try:
        database_connection = sq.connect('password_database.db')
        cursor = database_connection.cursor()
        print("Connection Successful")

        table_creation_query = """CREATE TABLE IF NOT EXISTS user_passwords (
                                account text,
                                username text,
                                password text,
                                email text 
            );"""

        master_password_table = """CREATE TABLE IF NOT EXISTS master_password (
                                master_password text
            );"""
        cursor.execute(master_password_table)
        cursor.execute(table_creation_query)
        database_connection.commit()
        database_connection.close()

    except sq.Error as error:
        print("Failure to connect")


def generate(entry_box):
    entry_box.delete(0, tk.END)
    characters = string.ascii_letters + string.digits + string.punctuation
    generated_password = ''.join(random.choice(characters) for i in range(15))
    print("Call")
    return generated_password


class App(tk.CTk):
    def __init__(self):
        super().__init__()
        # variables used for insertion into the database
        self.email_entry = tk.StringVar()
        self.username = tk.StringVar()
        self.account = tk.StringVar()
        self.password = tk.StringVar()
        self.generated_entry = None
        # Database Initialization
        init_db()
        # main_window
        self.title("Password Manager")
        self.geometry("600x440")

        # Variables
        self.password_holder = tk.StringVar()
        self.email_holder = tk.StringVar()
        self.password_reset = tk.StringVar()
        self.password_reset_verification = tk.StringVar()

        self.main_window()
        self._set_appearance_mode("System")

    def generate_password(self):
        self.withdraw()
        active_window = tk.CTkToplevel(self)
        active_window.geometry('800x620')
        active_window.title("Password Entry")
        active_window.focus_set()
        self.password = tk.StringVar()

        active_frame = tk.CTkFrame(master=active_window, width=700, height=520, corner_radius=15)
        active_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        self.generated_entry = tk.CTkEntry(master=active_frame, textvariable=self.password, width=220)
        self.generated_entry.place(x=50, y=365)

        generate_button = tk.CTkButton(master=active_frame, width=220, text="Generate",
                                       command=self.generate2, corner_radius=6)
        generate_button.place(x=50, y=430)

        account_label = tk.CTkLabel(master=active_frame, text="Account Name", font=('Open Sans', 15), anchor="center")
        account_label.place(x=50, y=200)

        account_entry = tk.CTkEntry(master=active_frame, textvariable=self.account, width=220)
        account_entry.place(x=50, y=240)

        username_label = tk.CTkLabel(master=active_frame, text="Username", font=('Open Sans', 15))
        username_label.place(x=300, y=200)

        username_entry = tk.CTkEntry(master=active_frame, textvariable=self.username, width=220)
        username_entry.place(x=300, y=240)

        email_label = tk.CTkLabel(master=active_frame, text="Email", font=('Open Sans', 15))
        email_label.place(x=300, y=340)

        email_entry = tk.CTkEntry(master=active_frame, textvariable=self.email_entry, width=220)
        email_entry.place(x=300, y=365)

        submit_button = tk.CTkButton(master=active_frame, width=220, text="Submit",
                                     command=self.submit_entry, corner_radius=6)
        submit_button.place(x=300, y=430)

    def submit_entry(self):
        database_connection = sq.connect('password_database.db')
        cursor = database_connection.cursor()
        print("connection successful")

        user_name = self.username.get()
        email = self.email_entry.get()
        password = self.password.get()
        account = self.account.get()
        table_insertion_query = "INSERT INTO user_passwords VALUES(?,?,?,?)"
        cursor.execute(table_insertion_query, (account, user_name, password, email))
        database_connection.commit()
        database_connection.close()

    def generate2(self):
        self.generated_entry.delete(0, tk.END)
        characters = string.ascii_letters + string.digits + string.punctuation
        generated_password = ''.join(random.choice(characters) for i in range(15))
        print(self.password)
        # return generated_password
        self.generated_entry.insert(0, generated_password)
        print("Checking")

    def login(self):
        database_connection = sq.connect('password_database.db')
        cursor = database_connection.cursor()
        password = self.password_holder.get()
        master_password_query = """SELECT master_password FROM master_password;"""
        cursor.execute(master_password_query)
        fetched_record = cursor.fetchone()
        password_actual = fetched_record[0]

        if password == password_actual:
            password = ""
            print("Success!")
            self.withdraw()
            main_window = tk.CTkToplevel(self)
            main_window.geometry('700x520')
            main_window.title("Password Manager")

            label_main_window = tk.CTkLabel(main_window, text="Stored Passwords", anchor='n', font=('Open Sans', 20))
            label_main_window.pack(padx=10, pady=(40, 20), fill='both')

            cursor.execute("""SELECT * from user_passwords;""")
            storage = cursor.fetchall()
            columns = ('account', 'username', 'password', 'email')

            table = ttk.Treeview(main_window,columns=columns, selectmode='browse', show="headings")
            table.heading('account', text='Account')
            table.heading('username', text='Username')
            table.heading('password', text='Password')
            table.heading('email', text='Email')

            for records in storage:
                table.insert("", tk.END, values=(records[0], records[1], records[2], records[3]))

            table.place(relx=0.5, rely=0.5, width=1000, height=410, anchor=tkinter.CENTER)

            insert_password_button = tk.CTkButton(master=main_window, width=220, text="Insert a password",
                                                  command=self.generate_password, corner_radius=6)
            insert_password_button.place(x=50, y=440)

        elif password != password_actual:

            error_message_label = tk.CTkLabel(master=self,
                                                text="The password you have entered is incorrect. Please try again.",
                                                text_color="red", font=('Open Sans', 10), anchor="center")
            error_message_label.place(x=150, y=330)

    def password_recovery_window(self):
        self.withdraw()
        window = tk.CTkToplevel(self)
        window.geometry('700x520')
        window.title("Recover Password")

        recovery_frame = tk.CTkFrame(master=window, width=320, height=360, corner_radius=15)
        recovery_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        label_recovery_window = tk.CTkLabel(master=recovery_frame,
                                            text="Enter the email associated with your master password", anchor='w',
                                            font=('Open Sans', 11))
        label_recovery_window.place(x=50, y=35)

        email_entry = tk.CTkEntry(master=recovery_frame, textvariable=self.email_holder,
                                  width=220,placeholder_text='Email')
        email_entry.place(x=50, y=70)

        new_password_label = tk.CTkLabel(master=recovery_frame, text="Enter your new master password",
                                         anchor="center", font=('Open Sans', 11))
        new_password_label.place(x=50, y=100)

        master_password_entry = tk.CTkEntry(master=recovery_frame, textvariable=self.password_reset, width=220)
        master_password_entry.place(x=50, y=130)

        submit_button = tk.CTkButton(master=recovery_frame, width=220, text="Submit",
                                     command=self.recover_query, corner_radius=6)
        submit_button.place(x=50, y=270)

    def recover_query(self):
        database_connection = sq.connect('password_database.db')
        cursor = database_connection.cursor()
        recovery_email = self.email_holder.get()

        cursor.execute("""SELECT email FROM master_password;""")
        fetched_email = cursor.fetchone()
        email_actual = fetched_email[0]
        cursor.close()

        if recovery_email == email_actual:
            print("Success")
            database_connection = sq.connect('password_database.db')
            cursor = database_connection.cursor()
            new_password = self.password_reset.get()

            update_query = """UPDATE master_password 
                            SET master_password = ?
                            WHERE email = ?;"""

            cursor.execute(update_query, (new_password, recovery_email))
            database_connection.commit()
            cursor.close()
            self.withdraw()

        else:
            print("You failed")
            cursor.close()

    def main_window(self):

        frame = tk.CTkFrame(master=self, width=320, height=360, corner_radius=15)
        frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        login_label = tk.CTkLabel(master=frame, text="Enter Master Password", font=('Open Sans', 19), anchor="center")
        login_label.place(x=55, y=45)

        # username_entry = tk.CTkEntry(master=frame, width=220, placeholder_text='Username')
        # username_entry.place(x=50, y=130)

        password_entry_label = tk.CTkLabel(master=frame, text="Password", font=('Open Sans', 14), anchor="center")
        password_entry_label.place(x=50,y=130)
        password_entry = tk.CTkEntry(master=frame, textvariable=self.password_holder,
                                     width=220, show="*")
        password_entry.place(x=50, y=165)

        login_button = tk.CTkButton(master=frame, width=220, text="Login", command=self.login, corner_radius=6)
        login_button.place(x=50, y=240)

        password_recover = tk.CTkLabel(master=frame, text="Forgot password?", font=('Open Sans', 12))
        password_recover.place(x=155, y=195)
        password_recover.bind("<Button-1>", lambda e: self.password_recovery_window())


if __name__ == "__main__":
    app = App()
    app.mainloop()
