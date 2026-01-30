from main_page import *
from PIL import Image

#setup piece for the user database
connection = sqlite3.connect("user_database.db")
cursor = connection.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS users_new (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT);""")

"""function that is used for developmental purposes of resetting the database"""
def reset_db():
    cursor.execute("DELETE FROM users_new")
    cursor.execute("UPDATE sqlite_sequence SET seq=0 WHERE name='users_new'")
    connection.commit()
    connection.close()

"""function that allows for switch between login and main pages"""
def start_main(r):
    gradient_frame.destroy()
    frame.destroy()
    create_main(r)

"""
Function that checks to see if entered username and password are correct
and match with one in the database
"""
def login():
    u=user_entry.get().strip()
    p=passwd_entry.get().strip()
    cursor.execute("SELECT * FROM users_new WHERE username = ? AND password = ? LIMIT 1", (u,p))
    results = cursor.fetchone()
    if results is None:
        new_account_button.pack_forget()
        error_message.pack(pady=(10,0))
        new_account_button.pack(pady=(30,20))
        root.after(4000,error_message.destroy)
    else:
        create_user_id(u,p)
        root.unbind('<Return>')
        # root.unbind('<r>')
        start_main(root)
        connection.close()

"""
Function that transitions from the login page to the signup page 
"""
def signup_page():
    for element in root.winfo_children():
        element.pack_forget()
    root.bind("<Return>", lambda e: create_account(user_entry.get().strip(),passwd_entry.get().strip()))
    error_message.pack_forget()
    gradient_frame.pack(pady=(100,0))
    frame.pack(pady=(0,10))
    img_frame.pack(pady=(50,20))
    top.configure(text="To create an Account\nPlease Enter a Username\nand Password")
    image_text.pack_forget()
    enter_button.pack_forget()
    details.pack_forget()
    new_account_button.pack_forget()
    create_button = ctk.CTkButton(frame, text='Sign Up', width=225,
                                  command=lambda: create_account(user_entry.get().strip(),passwd_entry.get().strip()))
    create_button.pack(pady=1)

"""
Function that creates and adds a new account within the user database
@:param username inputted username for account
@:param password inputted password for account
"""
def create_account(username,password):
    try:
        cursor.execute(f"INSERT INTO users_new (username,password) VALUES('{username}','{password}')")
        create_user_id(username,password)
    except sqlite3.IntegrityError:
        error_message.configure(text="Username already exists")
        error_message.pack()
        root.after(4000,error_message.destroy)
        return None
    connection.commit()
    connection.close()
    return start_main(root)

#setup piece to create the login page / behind the scenes things
root = ctk.CTk()
ctk.set_appearance_mode("system")
cursor.execute("SELECT * FROM users_new")
print(cursor.fetchall())
root.title("MyMoney Login Page")
root.update_idletasks()
root.after(1, root.state, 'zoomed')
h=root.winfo_screenheight()
w=root.winfo_screenwidth()
root.bind('<Return>', lambda e: login())
root.bind('<Escape>', lambda e: root.destroy())
# root.bind('<r>', lambda e: reset_db())

#setup that creates all the elements on the login page
gradient_frame=ctg.GradientFrame(root, colors=("#6f2da8","#5bb2fe"), direction="vertical",
                                 height=10,width=w//4,corner_radius=50)
gradient_frame.pack(pady=(100,0))
gradient_frame.pack_propagate(False)
frame = ctk.CTkFrame(root,width=w//4,height=h//3+50,fg_color='white',corner_radius=0)
frame.pack_propagate(False)
frame.pack()
img_frame=ctk.CTkFrame(frame,fg_color='white',corner_radius=0)
img_frame.pack_propagate(False)
img_frame.pack(pady=(30,5),anchor="center")
img=Image.open("white_background.png")
image=ctk.CTkImage(light_image=img,dark_image=img,size=(100,100))
image_text=ctk.CTkLabel(img_frame,image=image,text="")
image_text.grid(row=0,column=0)
top=ctk.CTkLabel(img_frame,text='Welcome Back to MyMoney',text_color='black',
                 font=("trebuchet ms",25,"underline"))
top.grid(row=0,column=1)
details=ctk.CTkLabel(frame,text="Please Login to your Account Below",text_color='black',
                     font=("trebuchet ms",25))
details.pack(pady=(0,10))
user_entry=ctk.CTkEntry(frame,placeholder_text='Enter Username:',
                        font=("Trebuchet MS",15),width=250)
user_entry.pack(pady=10)
passwd_entry=ctk.CTkEntry(frame,placeholder_text='Enter Password:',
                          font=("Trebuchet MS",15),width=250)
passwd_entry.pack(pady=(0,10))
enter_button=ctk.CTkButton(frame,text='Log In',command=login,font=("Trebuchet MS",15),width=225)
enter_button.pack(pady=1)
error_message = ctk.CTkLabel(frame,text='Incorrect username or password',
                             text_color='red',font=("Trebuchet MS",15))
new_account_button=ctk.CTkButton(frame,text='Click to make a New Account',
                                 command=signup_page,font=("Trebuchet MS",15))
new_account_button.pack(pady=(30,20))

root.mainloop()