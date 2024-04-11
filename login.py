from tkinter import *
from tkinter import messagebox
import mysql.connector
import os

# Function to connect to the database
def connect_to_database():
    return mysql.connector.connect(
        host="localhost",  # Or your database host
        user="root",
        password="puppyduylun365",# Your database password
        database="quiz_app" # Your database name
    )

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
        os.system('python question.py')  # open question.py
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
    os.system('python sign_up.py')
root=Tk()
root.title("Login")
root.geometry('925x500+300+200')
root.configure(bg="#fff")
root.resizable(False, False)

img = PhotoImage(file="images/login.png")
Label(root, image=img, bg="white").place(x=50, y=50)

frame = Frame(root, width=350, height=350,bg="white")
frame.place(x=480,y=70)

heading = Label(frame, text='Sign in',fg="#57a1f8", bg='white',
                 font=('Microsoft YaHei UI Light',23,'bold'))
heading.place(x=100, y=5)


def on_enter(e):
    user.delete(0,'end')

def on_leave(e):
    name=user.get()
    if name == '':
        user.insert(0, "Username")

user = Entry(frame, width=25, fg='black',border=0, bg='white', 
             font=('Microsoft YaHei UI Light', 12))   
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
             font=('Microsoft YaHei UI Light', 12))   
password.place(x=30,y=150)
password.insert(0, "Password")  
password.bind('<FocusIn>', on_enter)
password.bind('<FocusOut>', on_leave)
Frame(frame, width=295, height=2, bg='black').place(x=25, y=177 )


Button(frame, width=39, pady=7, text='Sign in', bg='#57a1f8', fg='white',border=0, command=sign_in).place(x=35,y=204)
label = Label(frame, text="Don't have an account?", bg='white', font=('Microsoft YaHei UI Light', 10))
label.place(x=25,y=270)

sign_up = Button (frame, width=6,text='Sign up', bg='white', fg='#57a1f8',cursor='hand2',border=0, command=sign_up)
sign_up.place(x=180,y=273)

root.mainloop()