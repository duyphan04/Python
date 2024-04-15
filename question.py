import tkinter as tk
from tkinter import messagebox, ttk, Label
from db import connect_to_database
from ttkbootstrap import Style
import mysql.connector
import os
from datetime import datetime

def insert_into_leaderboard(email, score, completion_time):
    connection = connect_to_database()
    cursor = connection.cursor()

    insert_query = f"INSERT INTO leaderboard (email, score, time) VALUES ('{email}', {score}, '{completion_time}');"
    cursor.execute(insert_query)
    connection.commit()
    connection.close()

# Function to handle window close event
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
def get_total_questions():
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM questions;")
    total = cursor.fetchone()[0]
    connection.close()
    return total

# Function to display the current question and choices
def show_question():
    global current_question_id
    question, choices = get_question_and_choices(current_question_id)
    qs_label.config(text=question)

    # Display the choices on the buttons
    for i in range(4):
        choice_btns[i].config(text=choices[i] if i < len(choices) else "", state="normal")  # Reset button state

    # Clear the feedback label and disable the next button
    feedback_label.config(text="")
    next_btn.config(state="disabled")

# Function to check the selected answer and provide feedback
def check_answer(choice):
    global current_question_id, score, total_questions
    correct_answer = get_correct_answer(current_question_id)
    selected_choice = choice_btns[choice].cget("text")

    # Check if the selected choice matches the correct answer
    if selected_choice == correct_answer:
        # Update the score and display it
        score += 1
        score_label.config(text=f"Score: {score}/{total_questions}")
        feedback_label.config(text="Correct!", foreground="green")
    else:
        feedback_label.config(text="Incorrect!", foreground="red")

    # Disable all choice buttons and enable the next button
    for button in choice_btns:
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
        email = get_user_email(logged_in_username)
        completion_time = datetime.now()
        insert_into_leaderboard(email, score, completion_time)
        root.destroy()


# Initialize the score and total questions
score = 0
total_questions = get_total_questions()

# Create the main window
root = tk.Tk()
root.title("Quiz App")
root.geometry("600x500")
style = Style(theme="flatly")



# Configure the font size for the question and choice buttons
style.configure("TLabel", font=("Helvetica", 20))
style.configure("TButton", font=("Helvetica", 16))

# Create the question label
qs_label = ttk.Label(
    root,
    anchor="center",
    wraplength=500,
    padding=10
)
qs_label.pack(pady=10)

# Create the choice buttons
choice_btns = []
for i in range(4):
    button = ttk.Button(
        root,
        command=lambda i=i: check_answer(i)
    )
    button.pack(pady=5)
    choice_btns.append(button)

# Create the feedback label
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

current_question_id = '5b1422651fdde'  # Replace with the actual first qid from your questions table

# Show the first question
show_question()

logged_in_username = os.getenv('USERNAME')
username_label = Label(root, text=logged_in_username)
username_label.pack()

# Override the window close event
root.protocol("WM_DELETE_WINDOW", on_closing)

# Start the main event loop
root.mainloop()




