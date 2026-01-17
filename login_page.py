import customtkinter as ctk
import sqlite3

"""setup piece for the user database"""
connection = sqlite3.connect("user_database.db")
cursor = connection.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS users_new (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT);""")

"""
Function that checks to see if entered username and password are correct
and match with one in the database
"""
def check():
    username=user_entry.get()
    password=passwd_entry.get()
    if username=='u' and password=='p':
        user_entry.configure(text="")
        top.configure(text="You have successfully logged in")
    else:
        top.configure(text="You have not successfully logged in")

"""
Function that transitions from the login page to the signup page 
"""
def signup_page():
    for element in root.winfo_children():
        element.pack_forget()
    frame.pack(pady=(50,10))
    top.configure(text="Enter a Username and Password to Sign Up")
    top.pack(pady=(20,10))
    enter_button.pack_forget()
    new_account_button.pack_forget()
    create_button = ctk.CTkButton(frame, text='Enter', command=lambda: create_account(user_entry.get(),passwd_entry.get()))
    create_button.pack(pady=1)

"""
Function that creates and adds a new account within the user database
@:param username inputted username for account
@:param password inputted password for account
"""
def create_account(username,password):
    try:
        cursor.execute(f"INSERT INTO users_new (username,password) VALUES('{username}','{password}')")
    except sqlite3.IntegrityError:
        print("User already exists")
    # cursor.execute("SELECT * FROM users_new")
    # print(cursor.fetchall())
    connection.commit()
    connection.close()

"""setup piece to create the login page"""
root = ctk.CTk()
root.title("MyMoney Login Page")
h=root.winfo_screenheight()
w=root.winfo_screenwidth()
root.geometry(f"{h}x{w}")
frame = ctk.CTkFrame(root,width=w//4,height=h//2,fg_color='white')
frame.pack(pady=(40,10))
frame.pack_propagate(False)
top=ctk.CTkLabel(frame,text='Welcome to MyMoney\nPlease Login Below',text_color='black')
top.pack(pady=(50,10))
user_entry=ctk.CTkEntry(frame,placeholder_text='Enter Username:')
user_entry.pack(pady=1)
passwd_entry=ctk.CTkEntry(frame,placeholder_text='Enter Password:')
passwd_entry.pack(pady=1)
enter_button=ctk.CTkButton(frame,text='Enter',command=check)
enter_button.pack(pady=1)
new_account_button=ctk.CTkButton(frame,text='Click to make a New Account',command=signup_page,border_color="gray")
new_account_button.pack(pady=20)




#reset table and id
# cursor.execute("DELETE FROM users_new")
# cursor.execute("UPDATE sqlite_sequence SET seq=0 WHERE name='users_new'")

root.mainloop()