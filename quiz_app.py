import tkinter as tk
from tkinter import *
from db import connect_to_database
import os
from tkinter import simpledialog
import random
import string
import pandas as pd
from tkinter import filedialog,messagebox

root = tk.Tk()
root.geometry('925x500+300+200')
root.configure(bg="#fff")
root.title('Main Form')

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

def edit_account():
    # Connect to the database
    db_connection = connect_to_database()

    # Create a cursor
    cursor = db_connection.cursor()

    # Execute the query
    cursor.execute(f"SELECT * FROM user WHERE name = '{get_username()}'")

    # Fetch the result
    user = cursor.fetchone()

    # Now `user` is a tuple containing the user's information
    # You can access the information like this:
    name, college, email, password, role = user

    # Close the connection
    cursor.close()
    db_connection.close()


    # Create a new frame for the edit account page
    edit_account_page_fm = tk.Frame(main_fm, bg="#fff")

    # Create labels and entry fields for each piece of user information
    # The entry fields are pre-filled with the current information
    name_label = tk.Label(edit_account_page_fm, text="Name", bg="white")
    name_label.pack()
    name_entry = tk.Entry(edit_account_page_fm)
    name_entry.insert(0, name)
    name_entry.pack()

    college_label = tk.Label(edit_account_page_fm, text="COLLEGE", bg="white")
    college_label.pack()
    college_entry = tk.Entry(edit_account_page_fm)
    if college is not None:
        college_entry.insert(0, college)
    else:
        college_entry.insert(0, "")
    college_entry.pack()

    email_label = tk.Label(edit_account_page_fm, text="EMAIL", bg="white")
    email_label.pack()
    email_entry = tk.Entry(edit_account_page_fm)
    email_entry.insert(0, email)
    email_entry.pack()

    password_label = tk.Label(edit_account_page_fm, text="PASSWORD", bg="white")
    password_label.pack()
    password_entry = tk.Entry(edit_account_page_fm)
    password_entry.insert(0, password)
    password_entry.pack()

    role_label = tk.Label(edit_account_page_fm, text="ROLE", bg="white")
    role_label.pack()
    role_entry = tk.Entry(edit_account_page_fm)
    role_entry.insert(0, role)
    role_entry.pack()

    def save_changes():
        # Get the updated information
        updated_name = name_entry.get()
        updated_college = college_entry.get()
        updated_email = email_entry.get()
        updated_password = password_entry.get()
        updated_role = role_entry.get()

        # Connect to the database
        db_connection = connect_to_database()

        # Create a cursor
        cursor = db_connection.cursor()

        # Execute the update query
        query = """
            UPDATE user
            SET name = %s, college = %s, email = %s, 
                password = %s, role = %s
            WHERE name = %s
        """
        cursor.execute(query, (updated_name, updated_college, updated_email, updated_password, updated_role, get_username()))

        # Commit the changes
        db_connection.commit()

        # Close the connection
        cursor.close()
        db_connection.close()

        messagebox.showinfo("Success", "Changes saved successfully")

    # Create a button to save the changes
    save_button = tk.Button(edit_account_page_fm, text="SAVE", command=save_changes)
    save_button.pack()

    # Finally, pack the frame
    edit_account_page_fm.pack(fill = tk.BOTH, expand=True)

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
        home_page_lb = Label(admin_page_fm, text="Choose the topic, you want to add question", font=('Century Gothic',25,'bold'), bg="white", cursor="hand2")
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
        num_answers = 4
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
    # Code Test Edit Admin
    
    def edit_question(event, eid):
      
        def show_question(qid, qns, optn):
            # Clear the edit_page_fm before showing a new question
        
          
            class EditQuestionDialog(simpledialog.Dialog):
                def __init__(self, master, qid, qns, optn, title=None):
                    self.qid = qid
                    self.qns = qns
                    self.optn = optn
                    super().__init__(master, title=title)


                def body(self, master):
                    self.qid_label = Label(master, text=f"Question ID: {self.qid}", font=("Century Gothic", 16))
                    self.qid_label.grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="w")

                    self.question_label = Label(master, text="Question:", font=("Century Gothic", 14))
                    self.question_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
                    self.question_entry = Entry(master, font=("Century Gothic", 14))
                    self.question_entry.insert(tk.END, self.qns)
                    self.question_entry.grid(row=1, column=1, padx=10, pady=5)

                    self.option_entries = []
                    for i, (opt, opt_id) in enumerate(self.optn):
                        option_label = Label(master, text=f"Option {i+1}:", font=("Century Gothic", 14))
                        option_label.grid(row=i+2, column=0, padx=10, pady=5, sticky="w")
                        option_entry = Entry(master, font=("Century Gothic", 14))
                        option_entry.insert(tk.END, opt)
                        option_entry.grid(row=i+2, column=1, padx=10, pady=5)
                        self.option_entries.append(option_entry)
                    self.answer_label = Label(master, text="Answer:", font=("Century Gothic", 14))
                    self.answer_label.grid(row=len(optn)+2, column=0, padx=10, pady=5, sticky="w")
                    self.answer_entry = Entry(master, font=("Century Gothic", 14))
                    self.answer_entry.grid(row=len(optn)+2, column=1, padx=10, pady=5)
                    save_button = Button(master, text="Save Changes", font=("Century Gothic", 14), command=lambda: save_changes(self))
                    save_button.grid(row=len(optn)+3, column=0, columnspan=1, pady=1)
                    remove_button = Button(master, text="Remove", font=("Century Gothic", 14), command=lambda: remove_changes(self))
                    remove_button.grid(row=len(optn)+3, column=2, columnspan=1, pady=1)
                    return self.question_entry
                def buttonbox(self):
                    pass
                def apply(self):
                    question_text = self.question_entry.get()
                    option_texts = [entry.get() for entry in self.option_entries]
                    print(question_text, option_texts)
               
            dialog = EditQuestionDialog(edit_page_fm, qid, qns, optn, title="Edit Question")
            dialog.mainloop()
       
        def save_changes(dialog):
            # Save question information to the database
            update_question(dialog.qid, dialog.question_entry.get())

            # Save option information to the database
            for i, entry in enumerate(dialog.option_entries):
                if i < len(dialog.optn):
                    option_id = dialog.optn[i][1]  # Get optionid value from dialog.options
                    update_option(option_id, entry.get())
                else:
                    print(f"Error: No option found for index {i}")

            answer_entry_value = dialog.answer_entry.get()
            if answer_entry_value.isdigit():
                correct_answer_index = int(answer_entry_value) - 1
                if correct_answer_index < len(dialog.optn):
                    new_answer = dialog.optn[correct_answer_index][1]
                    update_answer(dialog.qid, new_answer)
                else:
                    print(f"Error: No answer found for index {correct_answer_index}")
            else:
                print("Error: Invalid input for answer. Please enter a number.")

            messagebox.showinfo("Success", "Changes saved successfully!")
        def remove_changes(dialog):
            # Implement the logic to remove the question, its options, and answer from the database
            remove_question(dialog.qid)
            messagebox.showinfo("Success", "Question removed successfully!")

        def remove_question(qid):
            conn = connect_to_database()
            cursor = conn.cursor()
            # Delete options associated with the question
            cursor.execute("DELETE FROM options WHERE qid = %s", (qid,))
            # Delete answer associated with the question
            cursor.execute("DELETE FROM answer WHERE qid = %s", (qid,))
            # Delete the question itself
            cursor.execute("DELETE FROM questions WHERE qid = %s", (qid,))
            conn.commit()
            conn.close()
        def get_options_for_question(qid):
            conn = connect_to_database()
            cursor = conn.cursor()
            cursor.execute("SELECT `option`,`optionid` FROM options WHERE qid = %s", (qid,))
            options = cursor.fetchall()
            conn.close()
            return options

        def update_question(qid, new_text):
            conn = connect_to_database()
            cursor = conn.cursor()
            cursor.execute("UPDATE questions SET qns = %s WHERE qid = %s", (new_text, qid))
            conn.commit()
            conn.close()

        def update_option(optionid, new_text):
            conn = connect_to_database()
            cursor = conn.cursor()
            cursor.execute("UPDATE options SET `option` = %s WHERE `optionid` = %s", (new_text, optionid))
            conn.commit()
            conn.close()
        def update_answer(qid, new_ansid):
            conn = connect_to_database()
            cursor = conn.cursor()
            cursor.execute("UPDATE answer SET `ansid` = %s WHERE `qid` = %s", (new_ansid, qid))
            conn.commit()
            conn.close()

        # Create a new frame for editing questions
        edit_window = tk.Toplevel(root)
        edit_window.title("Edit Questions")

        # Set the size of the window
        window_width = 600
        window_height = 600
        edit_window.geometry(f"{window_width}x{window_height}")

        # Get the screen size
        screen_width = edit_window.winfo_screenwidth()
        screen_height = edit_window.winfo_screenheight()

        # Calculate the position to center the window
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)

        # Position the window
        edit_window.geometry(f"+{position_right}+{position_top}")

        # Tạo một canvas để chứa danh sách câu hỏi
        canvas = tk.Canvas(edit_window, bg="#fff")
        canvas.pack(side="left", fill="both", expand=True)

        # Thêm thanh cuộn
        scrollbar = tk.Scrollbar(edit_window, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Tạo một frame để chứa các câu hỏi
        edit_page_fm = tk.Frame(canvas, bg="#fff")
        canvas.create_window((0, 0), window=edit_page_fm, anchor="nw")

        # Lấy danh sách câu hỏi từ cơ sở dữ liệu
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT qid, qns, choice FROM questions WHERE eid = %s", (eid,))
        questions = cursor.fetchall()
        conn.close()

        # Tạo danh sách nút cho mỗi câu hỏi
        for qid, qns, choice in questions:
            optn = get_options_for_question(qid)
            question_button = tk.Button(edit_page_fm, text=f"Question ID: {qid}\nQuestion: {qns}", font=("Century Gothic", 14),
                                        command=lambda qid=qid, qns=qns, optn=optn: show_question(qid, qns, optn))
            question_button.pack(pady=5)
        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        edit_page_fm.bind("<Configure>", on_frame_configure)


    def edit_quiz():
        home_page_lb = Label(admin_page_fm, text="Choose the topic, you want to edit question", font=('Century Gothic',25,'bold'), bg="white", cursor="hand2")
        home_page_lb.place(x=150, y=150)

        conn = connect_to_database()
        cursor = conn.cursor()

        cursor.execute("SELECT eid, title FROM quiz")
        quizzes = cursor.fetchall()

        conn.close()

        y_position = 250
        for quiz in quizzes:
            eid, title = quiz
            label = Label(admin_page_fm, text=title, font=('Century Gothic',20), bg="white", cursor="hand2")
            label.place(x=380, y=y_position)
            label.bind("<Button-1>", lambda event, eid=eid: edit_question(event, eid))
            y_position += 80
    def import_file():
        file_path = filedialog.askopenfilename()
        if file_path:
        # Kết nối đến cơ sở dữ liệu MySQL
            conn = connect_to_database()
            cursor = conn.cursor()
            try:
                df = pd.read_excel(file_path,header= 0)
                for _, row in df.iterrows():
                        eid, qid, qns, choice, answer, *options = row  # Sử dụng *options để lấy tất cả giá trị còn lại
                        cursor.execute("SELECT COUNT(*) FROM questions WHERE eid = %s", (eid,))
                        result = cursor.fetchone()
                        if result[0] == 0:
                            # Nếu eid không tồn tại, bạn có thể xử lý ở đây hoặc bỏ qua câu hỏi này
                            continue
                        cursor.execute("SELECT MAX(sn) FROM questions WHERE eid = %s", (eid,))
                        result = cursor.fetchone()
                        max_sn = result[0] if result[0] is not None else 0
                        next_sn = max_sn + 1  
                        # Thêm câu hỏi vào bảng questions
                        cursor.execute("INSERT INTO questions (eid, qid, qns, choice,sn) VALUES (%s, %s, %s, %s, %s)", (eid, qid, qns, choice,next_sn))
                        otp = [None] * choice
                        for idx in range(choice):
                            option_text = options[idx] 
                            option_id = generate_qid()
                            otp[idx] =option_id
                            cursor.execute("INSERT INTO options (qid, `option`, optionid) VALUES (%s, %s, %s)", (qid, option_text, option_id))
                        # Thêm đáp án vào bảng answer
                        answerid= otp[answer-1]
                        cursor.execute("INSERT INTO answer (qid, ansid) VALUES (%s, %s)", (qid, answerid))
                        # Thêm các lựa chọn vào bảng options
                        
                conn.commit()
                # Thông báo import thành công
                messagebox.showinfo("Success", "Import data successfully!")
            except Exception as e:
                # Rollback nếu có lỗi
                conn.rollback()
                messagebox.showerror("Error", f"Error occurred: {str(e)}")

            finally:
                # Đóng kết nối
                cursor.close()
                conn.close()
    # nut export
    def export_file():
        try:
            # Kết nối đến cơ sở dữ liệu MySQL
            conn = connect_to_database()
            cursor = conn.cursor()

            # Truy vấn dữ liệu từ bảng questions
            cursor.execute("SELECT eid, qid, qns, choice, sn FROM questions")
            questions_data = cursor.fetchall()
            questions_df = pd.DataFrame(questions_data, columns=['eid', 'qid', 'qns', 'choice', 'sn'])

            # Truy vấn dữ liệu từ bảng options
            cursor.execute("SELECT qid, `option`, optionid FROM options")
            options_data = cursor.fetchall()
            options_df = pd.DataFrame(options_data, columns=['qid', 'option', 'optionid'])

            # Truy vấn dữ liệu từ bảng answer
            cursor.execute("SELECT qid, ansid FROM answer")
            answer_data = cursor.fetchall()
            answer_df = pd.DataFrame(answer_data, columns=['qid', 'ansid'])

            # Truy vấn dữ liệu từ bảng user
            cursor.execute("SELECT name, college, email, password, role FROM user")
            user_data = cursor.fetchall()
            user_df = pd.DataFrame(user_data, columns=['name', 'college', 'email', 'password', 'role'])

            # Truy vấn dữ liệu từ bảng quiz
            cursor.execute("SELECT id, eid, title, total, date FROM quiz")
            quiz_data = cursor.fetchall()
            quiz_df = pd.DataFrame(quiz_data, columns=['id', 'eid', 'title', 'total', 'date'])

            # Truy vấn dữ liệu từ bảng leaderboard
            cursor.execute("SELECT id, email, score, time FROM leaderboard")
            leaderboard_data = cursor.fetchall()
            leaderboard_df = pd.DataFrame(leaderboard_data, columns=['id', 'email', 'score', 'time'])

            # Yêu cầu người dùng chọn nơi lưu file Excel
            file_path = filedialog.asksaveasfilename(defaultextension=".xlsx")

            if file_path:
                # Tạo một Excel Writer object
                with pd.ExcelWriter(file_path) as writer:
                    # Xuất DataFrame của từng bảng ra một sheet riêng biệt trong file Excel
                    questions_df.to_excel(writer, sheet_name='questions', index=False)
                    options_df.to_excel(writer, sheet_name='options', index=False)
                    answer_df.to_excel(writer, sheet_name='answer', index=False)
                    user_df.to_excel(writer, sheet_name='user', index=False)
                    quiz_df.to_excel(writer, sheet_name='quiz', index=False)
                    leaderboard_df.to_excel(writer, sheet_name='leaderboard', index=False)

                # Thông báo xuất thành công
                messagebox.showinfo("Success", "Export data successfully!")
        except Exception as e:
            # Hiển thị thông báo lỗi nếu có lỗi xảy ra
            messagebox.showerror("Error", f"Error occurred: {str(e)}")
        finally:
            # Đóng kết nối
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    # Nut Edit 

    create_question_button = Button(admin_page_fm, text="Create new question", command=create_quiz, font=("Century Gothic", 20), bg="#fff", cursor="hand2", bd=0)
    create_question_button.pack()
    edit_question_button = Button(admin_page_fm, text="Edit Questions", font=("Century Gothic", 20), bg="#fff", command=edit_quiz, cursor='hand2', bd=0)
    edit_question_button.pack()
    import_question_button = Button(admin_page_fm, text="Import", font=("Century Gothic", 10), bg="#fff",fg='#57a1f8', cursor='hand2', command=import_file)
    import_question_button.pack()
    import_question_button.place(x=850, y=0, width=80, height=20)
    export_question_button = Button(admin_page_fm, text="Export", font=("Century Gothic", 10), bg="#fff", fg='#57a1f8', cursor='hand2', command=export_file)
    export_question_button.pack()
    export_question_button.place(x=850, y=30, width=80, height=20)
    admin_page_fm.pack(fill = tk.BOTH, expand=True)

def settings_page():
    settings_page_fm = tk.Frame(main_fm, bg="#fff")

    settings_page_lb = Button(settings_page_fm, text="LOG OUT", font=('Century Gothic',20), bg="white", command=log_out, cursor="hand2", bd=0)
    settings_page_lb.pack(pady = 5)

    edit_account_lb = Button(settings_page_fm, text="EDIT ACCOUNT", font=('Century Gothic',20), bg="white", command=edit_account, cursor="hand2", bd=0)
    edit_account_lb.pack(pady = 10)

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