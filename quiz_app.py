import tkinter as tk
from tkinter import *
from db import connect_to_database
import os
from tkinter import simpledialog
import random
import string
from tkinter import messagebox

root = tk.Tk()
root.geometry('925x500+300+200')
root.configure(bg="#fff")
root.title('Test')

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

class CustomDialog(simpledialog.Dialog):
    def __init__(self, parent, title=None, prompt=None):
        self.prompt = prompt
        super().__init__(parent, title=title)

    def body(self, master):
        Label(master, text=self.prompt, font=("Century Gothic", 20)).grid(row=0)
        self.entry = Entry(master, font=("Century Gothic", 20))
        self.entry.grid(row=1)
        return self.entry

    def apply(self):
        self.result = self.entry.get()

def switch(indicator_lb, page):

    for child in options_fm.winfo_children() :
        if isinstance(child, tk.Label):
            child['bg'] = 'SystemButtonFace'

    indicator_lb['bg']= "#0097e8"

    for fm in main_fm.winfo_children():
        fm.destroy()
        root.update()

    page()

def switch_if_admin(indicator_lb, page):
    role = get_role()
    if role == 'ADMIN':
        switch(indicator_lb, page)
    else:
        messagebox.showerror("Error", "Access denied. Only admins can access this feature.")


def open_question(event, eid):
    os.system(f'python question.py {eid}')

def home_page():
    home_page_fm = tk.Frame(main_fm, bg="#fff")

    home_page_lb = Label(home_page_fm, text="LET, PLAY", font=('Century Gothic',20, 'bold'), bg="white")
    home_page_lb.pack(pady = 40)

    conn = connect_to_database()
    cursor = conn.cursor()

    # Execute the query
    cursor.execute("SELECT eid, title FROM quiz")
    quizzes = cursor.fetchall()

    # Close the connection
    conn.close()

    # Create labels
    y_position = 120
    for quiz in quizzes:
        eid, title = quiz
        label = Label(home_page_fm, text=title, font=('Century Gothic',20), bg="white", cursor="hand2")
        label.place(x=370, y=y_position)
        label.bind("<Button-1>", lambda event, eid=eid: open_question(event, eid))
        y_position += 80  # Update y_position for the next label

    home_page_fm.pack(fill = tk.BOTH, expand=True)
def admin_page():
    admin_page_fm = tk.Frame(main_fm, bg="#fff")

    def create_quiz():
        home_page_lb = Label(admin_page_fm, text="Choose your topic, you want to add question", font=('Century Gothic',25,'bold'), bg="white")
        home_page_lb.place(x=150, y=150)

        conn = connect_to_database()
        cursor = conn.cursor()

        # Execute the query
        cursor.execute("SELECT eid, title FROM quiz")
        quizzes = cursor.fetchall()

        conn.close()

        # Create labels
        y_position = 250
        for quiz in quizzes:
            eid, title = quiz
            label = Label(admin_page_fm, text=title, font=('Century Gothic',20), bg="white", cursor="hand2")
            label.place(x=380, y=y_position)
            label.bind("<Button-1>", lambda event, eid=eid: create_question(event, eid))
            y_position += 80  

    def generate_qid():
        # Generate a random string of 11 characters
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=11))
        # Add '5b' at the beginning
        return '5b' + random_string

    def create_question(event, eid):
        dialog = CustomDialog(admin_page_fm, title="Create new question", prompt="Please enter the question:")
        question = dialog.result
        if question is not None and question != '':
            qid = generate_qid()
            conn = connect_to_database()
            cursor = conn.cursor()

            cursor.execute("SELECT MAX(sn) FROM questions WHERE eid = %s", (eid,))
            result = cursor.fetchone()
            max_sn = result[0] if result[0] is not None else 0
            next_sn = max_sn + 1  
    
            cursor.execute("INSERT INTO questions (qid, eid, qns, sn) VALUES (%s, %s, %s, %s)", (qid, eid, question, next_sn))
            conn.commit()
            conn.close()
            create_answers(qid)
        else:
            print("No question was entered.")

    def create_answers(qid):
        dialog = CustomDialog(admin_page_fm, title="Create new answer", prompt="Please enter the number of answers:")
        num_answers = int(dialog.result)
        answers = []
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("UPDATE questions SET choice = %s WHERE qid = %s", (num_answers, qid))
        conn.commit()
        conn.close()
        for i in range(num_answers):
            dialog = CustomDialog(admin_page_fm, title="Create new answer", prompt="Please enter answer #{}:".format(i+1))
            answer = dialog.result
            option_id = generate_qid()
            answers.append((answer, option_id))  # Store the answer and its option_id as a tuple
            conn = connect_to_database()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO options (qid, `option`, optionid) VALUES (%s, %s, %s)", (qid, answer, option_id))
            conn.commit()
            conn.close()
        select_correct_answer(qid, answers)

    def select_correct_answer(qid, answers):
        dialog = CustomDialog(admin_page_fm, title="Select correct answer", prompt="Please enter the number of the correct answer:")
        correct_answer_index = int(dialog.result) - 1 
        correct_answer, correct_option_id = answers[correct_answer_index]  # Get the answer and its option_id
        # Save the correct answer to the database
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO answer (qid, ansid) VALUES (%s, %s)", (qid, correct_option_id))    
        conn.commit()
        conn.close()

    create_question_button = Button(admin_page_fm, text="Create new question", command=create_quiz, font=("Century Gothic", 20), bg="#fff")
    create_question_button.pack()

    admin_page_fm.pack(fill = tk.BOTH, expand=True)

def settings_page():
    settings_page_fm = tk.Frame(main_fm, bg="#fff")

    settings_page_lb = Button(settings_page_fm, text="LOG OUT", font=('Century Gothic',20), bg="white", command=log_out)
    settings_page_lb.pack(pady = 40)


    settings_page_fm.pack(fill = tk.BOTH, expand=True)

def leaderboard_page():
    leaderboard_page_fm = tk.Frame(main_fm, bg="#fff")

    leaderboard_page_lb = tk.Label(leaderboard_page_fm, text="LEADERBOARD", font=('Century Gothic',20), bg="white")
    leaderboard_page_lb.pack(pady = 20)

    db_connection = connect_to_database()
    cursor = db_connection.cursor()

    # Execute the SQL query
    cursor.execute("SELECT email, score FROM leaderboard ORDER BY score DESC")

    # Fetch all the rows
    rows = cursor.fetchall()

    # Close the connection
    cursor.close()
    db_connection.close()

    # Loop through the rows
    # Connect to the database
    db_connection = connect_to_database()
    cursor = db_connection.cursor()

    cursor.execute("""
        SELECT user.name, MAX(leaderboard.score) AS max_score
        FROM leaderboard 
        INNER JOIN user ON leaderboard.email = user.email 
        GROUP BY user.name 
        ORDER BY max_score DESC
    """)
    # Fetch all the rows
    rows = cursor.fetchall()

    # Close the connection
    cursor.close()
    db_connection.close()

    # Loop through the rows
    for i, row in enumerate(rows, start=1):
        name, score = row
        # Create a frame for each row
        frame = Frame(leaderboard_page_fm, bg='white')
        frame.place(x=320, y=30 + i * 60)
        # Create a label inside the frame
        if i in [1, 2, 3]:
            # Load the image
            image = PhotoImage(file=f"./images/crown{i}.png")
            # Resize the image using subsample
            image = image.subsample(10, 10)  # reduce the size by half
            image_label = Label(frame, image=image, bg='white')
            image_label.image = image  # keep a reference to the image
            image_label.pack(side='left', padx=10, pady=10)
            # Create a label for the name and score
            text_label = Label(frame, text=f'{name} with score {score}', bg='white', font=('Century Gothic',10))
            text_label.pack(side='left')
        else:
            label = Label(frame, text=f'Rank {i}: {name} with score {score}', bg='white', font=('Century Gothic',10))
            label.pack(padx=10, pady=10)

    leaderboard_page_fm.pack(fill = tk.BOTH, expand=True)

def show_taskbar(event):
    global taskbar
    if taskbar is None:
        username = get_username()
        role = get_role()
        username_label = Label(main_fm, text=f"Hi, {username}|{role}", font=('Century Gothic',10), bg="white")
        username_label.place(x=0, y=15)
    else:
        taskbar.destroy()
        taskbar = None
        username_label.place_forget()

def log_out() : 
    root.destroy()
    os.system('python login.py')

options_fm = tk.Frame(root)

home_btn = tk.Button(options_fm, text='HOME',bd =0, bg="#fff", fg="#0097e8" ,cursor="hand2",activeforeground='#0097e8',
                     command = lambda: switch(indicator_lb=home_indicator_lb, page=home_page))
home_btn.place(x=150, y=0, width=150,height=50)
home_indicator_lb = tk.Label(options_fm,bg="#0097e8")
home_indicator_lb.place(x=175, y=35, width=100, height=2)

admin_btn = tk.Button(options_fm, text='ADMIN',bd =0, bg="#fff", fg="#0097e8" ,cursor="hand2",activeforeground='#0097e8',
                       command = lambda: switch_if_admin(indicator_lb=admin_indicator_lb, page=admin_page))
admin_btn.place(x=300, y=0, width=150,height=50)
admin_indicator_lb = tk.Label(options_fm)
admin_indicator_lb.place(x=325, y=35, width=100, height=2)


leaderboard_btn = tk.Button(options_fm, text='LEADERBOARD',bd =0, bg="#fff", fg="#0097e8" ,cursor="hand2",activeforeground='#0097e8',
                            command = lambda: switch(indicator_lb=leaderboard_indicator_lb, page=leaderboard_page))
leaderboard_btn.place(x=450,y=0, width=150,height=50)
leaderboard_indicator_lb = tk.Label(options_fm)
leaderboard_indicator_lb.place(x=475, y=35, width=100, height=2)


settings_btn = tk.Button(options_fm, text='SETTINGS', bd =0, bg="#fff", fg="#0097e8" ,cursor="hand2",activeforeground='#0097e8',
                            command = lambda: switch(indicator_lb=settings_indicator_lb, page=settings_page))

settings_btn.place(x=600, y=0, width=150,height=50)
settings_indicator_lb = tk.Label(options_fm)
settings_indicator_lb.place(x=625, y=35, width=100, height=2)



options_fm.pack(pady = 5)
options_fm.pack_propagate(False)
root.update() 
options_fm.configure(bg="#fff",width=root.winfo_width(), height=50)

main_fm = tk.Frame(root, bg="#fff")
main_fm.pack(fill='both', expand=True)

img = PhotoImage(file="images/user.png")
img_label = Label(root, image=img, bg="#fff", cursor="hand2")
img_label.place(x=0, y=0)
img_label.bind("<Button-1>", show_taskbar)


home_page()

root.mainloop()