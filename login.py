from tkinter import *
from tkinter import messagebox
from db import connect_to_database
import mysql.connector
import os

def authentication(username, password):
    connection = connect_to_database()
    cursor = connection.cursor(dictionary=True) 

    # get user record
    user_query = f"SELECT * FROM user WHERE name = '{username}';"
    cursor.execute(user_query)
    user_record = cursor.fetchone()

    if user_record is None:
        return False  # user does not exist

   # check if the provided password matches the one in the database
    if user_record["password"] == password:
        return True

    return False

def sign_in():
    global password
    entered_password = password.get()
    entered_username = user.get()

    if authentication(entered_username, entered_password):
        os.system('python question.py')
    else:
        messagebox.showerror("Error", "Invalid username or password")

def sign_up():
    root.destroy()
    os.system('python sign_up.py')

root=Tk()
root.title("Login")
root.geometry('925x500+300+200')
root.configure(bg="#fff")
root.resizable(False, False)

img = PhotoImage(file="images/login.png")
Label(root, image=img, bg="white").place(x=50, y=50)

frame = Frame(root, width=350, height=500,bg="white")
frame.place(x=480,y=40)

heading = Label(frame, text='LOGIN',fg="#57a1f8", bg='white',
                 font=('Century Gothic',23,'bold'))
heading.place(x=110, y=5)


def on_enter(e):
    user.delete(0,'end')

def on_leave(e):
    name=user.get()
    if name == '':
        user.insert(0, "Username")

user = Entry(frame, width=25, fg='black',border=0, bg='white', 
             font=('Century Gothic', 12))   
user.place(x=30,y=80)
user.insert(0, "Username")  
user.bind('<FocusIn>', on_enter)
user.bind('<FocusOut>', on_leave)
Frame(frame, width=295, height=2, bg='black').place(x=25, y=107 )



def on_enter(e):
    password.delete(0,'end')

def on_leave(e):
    name=password.get()
    if name == '':
        password.insert(0, "Password")

password = Entry(frame, width=25, fg='black',border=0, bg='white', 
             font=('Century Gothic', 12))   
password.place(x=30,y=150)
password.insert(0, "Password")  
password.bind('<FocusIn>', on_enter)
password.bind('<FocusOut>', on_leave)
Frame(frame, width=295, height=2, bg='black').place(x=25, y=177 )


Button(frame, width=39, pady=7, text='Login', bg='#57a1f8', fg='white',border=0, command=sign_in).place(x=35,y=204)

label = Label(frame, text="Don't have an account?", bg='white', font=('Century Gothic', 10))
label.place(x=25,y=250)

sign_up = Button(frame, width=6, text='Sign up', bg='white', fg='#57a1f8', cursor='hand2', border=0, command=sign_up, font=("Century", 10, "underline"))
sign_up.place(x=200,y=248)

orLabel = Label(frame,text="----------------------------------OR-----------------------------------"
                ,bg="white",font=('Century Gothic', 10))
orLabel.place(x=25,y=280)

facebook_logo = PhotoImage(file="images/facebook.png")
Label(frame, image=facebook_logo, bg="white").place(x=95, y=320)

google_logo = PhotoImage(file="images/google.png")
Label(frame, image=google_logo, bg="white").place(x=155, y=320)

github_logo = PhotoImage(file="images/github.png")
Label(frame, image=github_logo, bg="white").place(x=215, y=320)

root.mainloop()