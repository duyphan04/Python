from tkinter import *
from tkinter import messagebox
import ast
import os
from db import connect_to_database


# Rest of your sign_up.py code

window=Tk()
window.title("Leaderboard")
window.geometry('925x700+300+50')
window.configure(bg="#fff")
window.resizable(False, False)

heading = Label(window, text='LEADERBOARD',fg="#57a1f8", bg='white',
                 font=('Century Gothic',50,'bold'))
heading.place(x=260, y=30)

# Connect to the database
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
    frame = Frame(window, bg='white')
    frame.place(x=300, y=50 + i * 80)
    # Create a label inside the frame
    if i in [1, 2, 3]:
        # Load the image
        image = PhotoImage(file=f"./images/crown{i}.png")
        # Resize the image using subsample
        image = image.subsample(10, 10)  # reduce the size by half
        image_label = Label(frame, image=image, bg='white')
        image_label.image = image  # keep a reference to the image
        image_label.pack(side='left', padx=20, pady=20)
        # Create a label for the name and score
        text_label = Label(frame, text=f'{name} with score {score}', bg='white', font=('Century Gothic',20))
        text_label.pack(side='left')
    else:
        label = Label(frame, text=f'Rank {i}: {name} with score {score}', bg='white', font=('Century Gothic',20))
        label.pack(padx=20, pady=20)

window.mainloop()