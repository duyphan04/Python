from tkinter import *
from tkinter import messagebox
import ast
import os
from db import connect_to_database


# Rest of your sign_up.py code

window=Tk()
window.title("Sign Up")
window.geometry('925x500+300+200')
window.configure(bg="#fff")
window.resizable(False, False)

img = PhotoImage(file="images/signup.png")
Label(window,image=img,border=0, bg="white").place(x=50,y=90)


frame=Frame(window,width=350,height=450,bg="#fff")
frame.place(x=480,y=40)

heading=Label(frame, text="CREATE ACCOUNT",fg="#57a1f8",bg="white",font=("Century Gothic",23,"bold"))
heading.place(x=35,y=0)

def on_enter(e):
    e.widget.delete(0, 'end')

def on_leave(e, default_text):
    name = e.widget.get()
    if name == '':
        e.widget.insert(0, default_text)


def sign_up():
    # Get the data from the entry fields
    username_data = username.get()
    password_data = password.get()
    confirm_password_data = confirm_password.get()
    email_data = email.get()
    role_data = "USER"

    # Check if password and confirm password are the same
    if password_data != confirm_password_data:
        messagebox.showerror("Error", "Passwords do not match!")
        return

    # Connect to the database
    db_connection = connect_to_database()
    cursor = db_connection.cursor()

    # Insert the data into the user table
    insert_query = "INSERT INTO user (name, password, email, role) VALUES (%s, %s, %s, %s)"
    cursor.execute(insert_query, (username_data, password_data, email_data, role_data))

    # Commit the changes and close the connection
    db_connection.commit()
    cursor.close()
    db_connection.close()

    messagebox.showinfo("Success", "Account created successfully!")
    window.destroy()
    os.system('python login.py')

def sign_in():
    # Add your sign in logic here
    window.destroy()
    os.system('python login.py')

email = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Century Gothic', 12))
email.place(x=30, y=80)
email.insert(0, "Email")
email.bind('<FocusIn>', on_enter)
email.bind('<FocusOut>', lambda e: on_leave(e, "Email"))
Frame(frame, width=295, height=2, bg='black').place(x=25, y=107)

username = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Century Gothic', 12))
username.place(x=30, y=130)
username.insert(0, "Username")
username.bind('<FocusIn>', on_enter)
username.bind('<FocusOut>', lambda e: on_leave(e, "Username"))
Frame(frame, width=295, height=2, bg='black').place(x=25, y=157)

password = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Century Gothic', 12))
password.place(x=30, y=180)
password.insert(0, "Password")
password.bind('<FocusIn>', on_enter)
password.bind('<FocusOut>', lambda e: on_leave(e, "Password"))
Frame(frame, width=295, height=2, bg='black').place(x=25, y=207)

confirm_password = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Century Gothic', 12))
confirm_password.place(x=30, y=230)
confirm_password.insert(0, "Confirm Password")
confirm_password.bind('<FocusIn>', on_enter)
confirm_password.bind('<FocusOut>', lambda e: on_leave(e, "Confirm Password"))
Frame(frame, width=295, height=2, bg='black').place(x=25, y=257)

sign_up = Button(frame, width=39, pady=7, text='Sign up', bg='#57a1f8', fg='white', border=0, command=sign_up)
sign_up.place(x=35, y=284)

label=Label(frame, text="Already have an account?", bg='white', font=('Century Gothic', 10))
label.place(x=25, y=350)

sign_in = Button(frame, font=("Century", 10, "underline"), width=6, text='Sign in', bg='white', fg='#57a1f8', cursor='hand2', border=0, command=sign_in)
sign_in.place(x=210,y=348)

window.mainloop()