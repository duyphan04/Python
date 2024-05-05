import tkinter as tk
from tkinter import messagebox, ttk, Label
from db import connect_to_database
from ttkbootstrap import Style
import os
from datetime import datetime
import sys
import time

# Add a global variable for the remaining time
remaining_time = 10

# Add a global variable for tracking whether an answer has been selected
answer_selected = False

# Function to update the remaining time
def update_remaining_time():
    global remaining_time, answer_selected
    if remaining_time > 0:
        remaining_time -= 1
        time_label.config(text=f"Time: {remaining_time}s")
        root.after(1000, update_remaining_time)
    elif not answer_selected:
        next_question()  # Automatically move to the next question when the time is up and no answer has been selected

def insert_into_leaderboard(email, score, completion_time):
    connection = connect_to_database()
    cursor = connection.cursor()

    insert_query = f"INSERT INTO leaderboard (email, score, time) VALUES ('{email}', {score}, '{completion_time}');"
    cursor.execute(insert_query)
    connection.commit()
    connection.close()

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()

def get_user_email(username):
    connection = connect_to_database()
    cursor = connection.cursor(dictionary=True)

    email_query = f"SELECT email FROM user WHERE name = '{username}';"
    cursor.execute(email_query)
    email_record = cursor.fetchone()
    email = email_record["email"] if email_record else None

    connection.close()
    return email

def get_number_of_choices(question_id):
    cursor.execute(f"SELECT choice FROM questions WHERE qid = '{question_id}'")
    result = cursor.fetchone()
    return result[0] if result is not None else 0

# Function to get a single question and its choices from the database
def get_question_and_choices(question_id):
    connection = connect_to_database()
    cursor = connection.cursor(dictionary=True)

    # Get the question
    question_query = f"SELECT qns FROM questions WHERE qid = '{question_id}';"
    cursor.execute(question_query)
    question_record = cursor.fetchone()
    question = question_record["qns"] if question_record else None

    # Get the choices
    choices_query = f"SELECT `option` FROM options WHERE qid = '{question_id}';"
    cursor.execute(choices_query)
    choices_records = cursor.fetchall()
    choices = [choice["option"] for choice in choices_records] if choices_records else []



    connection.close()
    return question, choices

# Function to get the correct answer from the database
def get_correct_answer(question_id):
    connection = connect_to_database()
    cursor = connection.cursor(dictionary=True)

    answer_query = f"SELECT ansid FROM answer WHERE qid = '{question_id}';"
    cursor.execute(answer_query)
    answer_record = cursor.fetchone()
    correct_answer_id = answer_record["ansid"] if answer_record else None

    correct_answer_query = f"SELECT `option` FROM options WHERE optionid = '{correct_answer_id}';"
    cursor.execute(correct_answer_query)
    correct_answer_record = cursor.fetchone()
    correct_answer = correct_answer_record["option"] if correct_answer_record else None

    connection.close()
    return correct_answer

# Function to get the total number of questions from the database
def get_total_questions(eid):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT MAX(sn) FROM questions WHERE eid = %s;", (eid,))
    total = cursor.fetchone()[0]
    connection.close()
    return total


# Function to display the current question and choices
def show_question():
    global current_question_id, remaining_time, answer_selected
    question, choices = get_question_and_choices(current_question_id)
    qs_label.config(text=question)
    num_choices = get_number_of_choices(current_question_id)
    # Display the choices on the buttons
    for i in range(num_choices):
        choice_btns[i].config(text=choices[i] if i < len(choices) else "", state="normal")  # Reset button state

    # Clear the feedback label and disable the next button
    feedback_label.config(text="")
    next_btn.config(state="disabled")

    # Start the countdown and reset answer_selected
    remaining_time = 10  # Reset the remaining time to 10 seconds
    answer_selected = False
    update_remaining_time()

# Function to check the selected answer and provide feedback
def check_answer(choice):
    global current_question_id, score, total_questions, remaining_time, answer_selected
    correct_answer = get_correct_answer(current_question_id)
    selected_choice = choice_btns[choice].cget("text")

    # Stop the countdown and mark that an answer has been selected
    remaining_time = 0
    answer_selected = True

    # Check if the selected choice matches the correct answer
    if selected_choice == correct_answer:
        # Update the score and display it
        score += 1
        score_label.config(text=f"Score: {score}/{total_questions}")
        feedback_label.config(text="Correct!", foreground="green")
    else:
        feedback_label.config(text="Incorrect!", foreground="red")

    # Disable all choice buttons and add a tick before the correct answer
    for button in choice_btns:
        if button.cget("text") == correct_answer:
            button.config(text=f"✓ {button.cget('text')}")
            button.config(state="disabled")
        else:
            button.config(state="disabled")
        
    next_btn.config(state="normal")


    
    
# Function to move to the next question
def next_question():
    global current_question_id, total_questions
    # Get the next question id from the database
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute(f"SELECT qid FROM questions WHERE sn > (SELECT sn FROM questions WHERE qid = '{current_question_id}') ORDER BY sn LIMIT 1;")
    next_question_record = cursor.fetchone()
    connection.close()

    if next_question_record:
        current_question_id = next_question_record[0]
        show_question()
    else:
        # If all questions have been answered, display the final score and end the quiz
        messagebox.showinfo("Quiz Completed", f"Quiz Completed! Final score: {score}/{total_questions}")
        email = get_user_email(os.getenv('USERNAME'))
        completion_time = datetime.now()
        insert_into_leaderboard(email, score, completion_time)
        root.destroy()


# Initialize the score and total questions
score = 0
eid = sys.argv[1]
total_questions = get_total_questions(eid)

# Create the main window
root = tk.Tk()
root.title("Quiz App")
root.geometry("925x700+300+50")
style = Style(theme="flatly")



# Configure the font size for the question and choice buttons
style.configure("TLabel", font=("Century Gothic", 20))
style.configure("TButton", font=("Century Gothic", 16))

# Create the question label
qs_label = ttk.Label(
    root,
    anchor="center",
    wraplength=500,
    padding=10
)
qs_label.pack(pady=10)


choice_btns = []
for i in range(4):
    button = ttk.Button(
        root,
        command=lambda i=i: check_answer(i)
    )
    button.pack(pady=5)
    choice_btns.append(button)

feedback_label = ttk.Label(
    root,
    anchor="center",
    padding=10
)
feedback_label.pack(pady=10)

# Create the score label
score_label = ttk.Label(
    root,
    text=f"Score: 0/{total_questions}",
    anchor="center",
    padding=10
)
score_label.pack(pady=10)

# Create the next button
next_btn = ttk.Button(
    root,
    text="Next",
    command=next_question,
    state="disabled"
)
next_btn.pack(pady=10)

# Add a label to the GUI to display the remaining time
time_label = ttk.Label(
    root,
    text=f"Time remaining: {remaining_time}s",
    anchor="center",
    foreground="red",
    padding=10
)
time_label.pack(pady=10)

conn = connect_to_database()
cursor = conn.cursor()

cursor.execute(f"SELECT qid FROM questions WHERE eid = '{eid}' ORDER BY sn LIMIT 1")
result = cursor.fetchone()

if result is not None:
    current_question_id = result[0]  # Replace with the actual first qid from your questions table

show_question()

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()




