import customtkinter as ctk

def check():
    username=user_entry.get()
    password=passwd_entry.get()
    if username=='u' and password=='p':
        user_entry.configure(text="")
        top.configure(text="You have successfully logged in")
    else:
        top.configure(text="You have not successfully logged in")

def signup_page():
    for element in root.winfo_children():
        element.pack_forget()
    top.configure(text="Enter a Username and Password to Sign Up")
    top.pack(pady=(20,10))
    new_user_entry = ctk.CTkEntry(root, placeholder_text='Enter Username:')
    new_user_entry.pack(pady=1)
    new_passwd_entry = ctk.CTkEntry(root, placeholder_text='Enter Password:')
    new_passwd_entry.pack(pady=1)
    create_button = ctk.CTkButton(root, text='Enter')
    create_button.pack(pady=1)

root = ctk.CTk()
root.title("MyMoney Login Page")
h=root.winfo_screenheight()
w=root.winfo_screenwidth()
root.geometry(f"{h}x{w}")

top=ctk.CTkLabel(root,text='Welcome to MyMoney\nPlease Login Below')
top.pack(pady=(20,10))

user_entry=ctk.CTkEntry(root,placeholder_text='Enter Username:')
user_entry.pack(pady=1)
passwd_entry=ctk.CTkEntry(root,placeholder_text='Enter Password:')
passwd_entry.pack(pady=1)

enter_button=ctk.CTkButton(root,text='Enter',command=check)
enter_button.pack(pady=1)

new_account_button=ctk.CTkButton(root,text='Click to make a New Account',command=signup_page,border_color="gray")
new_account_button.pack(pady=20)

root.mainloop()