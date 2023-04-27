# Password Generation and Storage Application


Required libraries:
* customtkinter - can be installed through pip, pip install tkinter

This application is essentially a password storage and generation application that allows users to store their existing passwords in a sqlite database as well as generate a strong password. The application uses a database with two tables, one to store the master password and recovery email and the other to store the users passwords and the account information associated with them. The application was developed using python with libraries such as tkinter and customtkinter for the frontend of the application. sqlite was used for making the database as this application is meant to be a locally running application. Currently the user is only able to insert passwords and update the master password.