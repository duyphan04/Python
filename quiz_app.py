from tkinter import *
from tkinter import messagebox
from db import connect_to_database
import os

root=Tk()
root.title("Main Menu")
root.geometry('925x500+300+200')
root.configure(bg="#fff")
root.resizable(False, False)

taskbar = None
username_label = None

def get_username() :
    return os.getenv('USERNAME')  # Get the username from the environment variable

def get_role() :
    conn = connect_to_database()
    c = conn.cursor()

    # Get the username from the environment variable
    username = os.getenv('USERNAME')

    # Execute a query to get the role
    c.execute("SELECT role FROM user WHERE name = %s", [username])
    role = c.fetchone()[0]  # Get the first result

    return role  # Return the role

def open_question(event):
    username = get_username()
    os.system(f'set USERNAME={username} && python question.py')

def open_leaderboard(event):
    os.system('python leaderboard.py')

def show_taskbar(event):
    global taskbar, username_label
    if taskbar is None:
        # Create a new window (taskbar)
        taskbar = Toplevel(root)
        taskbar.configure(bg="#fffacd")  # Set the background color

        # Get the position of the image
        x = root.winfo_x() + img_label.winfo_x() + img_label.winfo_width() - 87
        y = root.winfo_y() + img_label.winfo_y() + img_label.winfo_height() + 75
        # Set the position of the taskbar
        taskbar.geometry(f'130x387+{x}+{y}')  # Adjust size to your needs
        taskbar.overrideredirect(1)  # Remove window decorations

        username = get_username()
        role = get_role()
        username_label = Label(root, text=f"Hi, {username}|{role}", font=('Century Gothic',10), bg="white")
        username_label.place(x=800, y=65)
        
        # Add some content to the taskbar
        home_label = Label(taskbar, text="Home", font=('Century Gothic',12), bg="#fffacd", cursor="hand2")
        home_label.pack(pady=17, padx=10, anchor="w")
        home_label.bind("<Button-1>", open_question)

        Label(taskbar, text="Account", font=('Century Gothic',12), bg="#fffacd").pack(pady=17, padx=10, anchor="w")

        leaderboard_label = Label(taskbar, text="Leaderboard",font=('Century Gothic',12),bg="#fffacd")
        leaderboard_label.pack(pady=17, padx=10, anchor="w")
        leaderboard_label.bind("<Button-1>", open_leaderboard)

        Label(taskbar, text="Statistic",font=('Century Gothic',12),bg="#fffacd").pack(pady=17, padx=10, anchor="w")
        Label(taskbar, text="Setting",font=('Century Gothic',12),bg="#fffacd").pack(pady=17, padx=10, anchor="w")
    else:
        taskbar.destroy()
        taskbar = None
        username_label.place_forget()

img = PhotoImage(file="images/user.png")
img_label = Label(root, image=img, bg="white")
img_label.place(x=820, y=0)
img_label.bind("<Button-1>", show_taskbar)

root.mainloop()