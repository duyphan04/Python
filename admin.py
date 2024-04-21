from tkinter import *
from tkinter import simpledialog
from db import connect_to_database
import random
import string

window=Tk()
window.title("Admin Panel")
window.geometry('925x700+300+50')
window.configure(bg="#fff")
window.resizable(False, False)

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

def create_quiz():
    home_page_lb = Label(window, text="Choose your topic, you want to add question", font=('Century Gothic',25,'bold'), bg="white")
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
        label = Label(window, text=title, font=('Century Gothic',20), bg="white", cursor="hand2")
        label.place(x=380, y=y_position)
        label.bind("<Button-1>", lambda event, eid=eid: create_question(event, eid))
        y_position += 80  

def generate_qid():
    # Generate a random string of 11 characters
    random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=11))
    # Add '5b' at the beginning
    return '5b' + random_string

def create_question(event, eid):
    dialog = CustomDialog(window, title="Create new question", prompt="Please enter the question:")
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
    dialog = CustomDialog(window, title="Create new answer", prompt="Please enter the number of answers:")
    num_answers = int(dialog.result)
    answers = []
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("UPDATE questions SET choice = %s WHERE qid = %s", (num_answers, qid))
    conn.commit()
    conn.close()
    for i in range(num_answers):
        dialog = CustomDialog(window, title="Create new answer", prompt="Please enter answer #{}:".format(i+1))
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
    dialog = CustomDialog(window, title="Select correct answer", prompt="Please enter the number of the correct answer:")
    correct_answer_index = int(dialog.result) - 1 
    correct_answer, correct_option_id = answers[correct_answer_index]  # Get the answer and its option_id
    # Save the correct answer to the database
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO answer (qid, ansid) VALUES (%s, %s)", (qid, correct_option_id))    
    conn.commit()
    conn.close()

create_question_button = Button(window, text="Create new question", command=create_quiz, font=("Century Gothic", 30), bg="#57a1f8", fg="white")
create_question_button.pack()

window.mainloop()