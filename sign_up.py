from tkinter import *
from tkinter import messagebox
import ast

window=Tk()
window.title("Sign Up")
window.geometry('925x500+300+200')
window.configure(bg="#fff")
window.resizable(False, False)

img = PhotoImage(file="images/signup.png")
Label(window,image=img,border=0, bg="white").place(x=50,y=90)


frame=Frame(window,width=350,height=450,bg="#fff")
frame.place(x=480,y=50)

heading=Label(frame, text="Sign Up",fg="#57a1f8",bg="white",font=("Microsoft YaHei UI Light",23,"bold"))
heading.place(x=100,y=-20)

def on_enter(e):
    e.widget.delete(0, 'end')

def on_leave(e, default_text):
    name = e.widget.get()
    if name == '':
        e.widget.insert(0, default_text)

def sign_up():
    # Add your sign up logic here
    pass

email = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 12))
email.place(x=30, y=50)
email.insert(0, "Email")
email.bind('<FocusIn>', on_enter)
email.bind('<FocusOut>', lambda e: on_leave(e, "Email"))
Frame(frame, width=295, height=2, bg='black').place(x=25, y=77)

username = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 12))
username.place(x=30, y=100)
username.insert(0, "Username")
username.bind('<FocusIn>', on_enter)
username.bind('<FocusOut>', lambda e: on_leave(e, "Username"))
Frame(frame, width=295, height=2, bg='black').place(x=25, y=127)

password = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 12))
password.place(x=30, y=150)
password.insert(0, "Password")
password.bind('<FocusIn>', on_enter)
password.bind('<FocusOut>', lambda e: on_leave(e, "Password"))
Frame(frame, width=295, height=2, bg='black').place(x=25, y=177)

confirm_password = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 12))
confirm_password.place(x=30, y=200)
confirm_password.insert(0, "Confirm Password")
confirm_password.bind('<FocusIn>', on_enter)
confirm_password.bind('<FocusOut>', lambda e: on_leave(e, "Confirm Password"))
Frame(frame, width=295, height=2, bg='black').place(x=25, y=227)

Button(frame, width=39, pady=7, text='Sign up', bg='#57a1f8', fg='white', border=0, command=sign_up).place(x=35, y=254)


window.mainloop()