import sections_files.misc_functions as m

first="joe"
last="shmoe"
email="joeshmoe@gmail.com"
dob="01/01/2000"

"""Function that creates the contents of the accounts page"""
def profile(top_text,inner_frame,root):
    m.delete_contents(inner_frame)
    top_text.configure(text="MyProfile")
    first_name=m.ctk.CTkLabel(inner_frame,text=f"First Name: {first[0].upper()}{first[1:]} ",font=("Trebuchet MS",30),text_color="black")
    first_name.grid(row=0,column=0,pady=100,padx=50)
    last_name=m.ctk.CTkLabel(inner_frame,text=f"Last Name: {last[0].upper()}{last[1:]} ",font=("Trebuchet MS",30),text_color="black")
    last_name.grid(row=0,column=2,pady=100,padx=50)
    email_text=m.ctk.CTkLabel(inner_frame,text=f"Email: {email} ",font=("Trebuchet MS",30),text_color="black")
    email_text.grid(row=1,column=0,pady=50,padx=50)
    dob_text=m.ctk.CTkLabel(inner_frame,text=f"Date of Birth: {dob} ",font=("Trebuchet MS",30),text_color="black")
    dob_text.grid(row=1,column=2,pady=50,padx=50)
    edit_profile_button=m.ctk.CTkButton(inner_frame,text="Click to Edit Profile",font=("Trebuchet MS",30),
                                      command=lambda: edit_profile(top_text,inner_frame,root),width=125,height=40)
    edit_profile_button.grid(row=2,column=0,pady=(50,0),padx=50)
    logout_button=m.ctk.CTkButton(inner_frame,text="Press to Logout", width=125,height=40,
                                font=("Trebuchet MS",30),command=lambda: logout(root))
    logout_button.grid(row=2,column=2,pady=(50,0),padx=50)
    delete_account_button = m.ctk.CTkButton(inner_frame, text="Delete Account", font=("Trebuchet MS", 25),width=123,height=40,hover_color="#420D09",
                                          fg_color="#960019", command=lambda: delete_safeguard(delete_account_button,inner_frame,root))
    delete_account_button.grid(row=3,column=1,pady=(0,5),padx=50)

"""Function that creates entries so the user can update/change their personal info"""
def edit_profile(top_text,inner_frame,root):
    m.delete_contents(inner_frame)
    top_text.configure(text="MyEditProfile")
    first_text=m.ctk.CTkLabel(inner_frame,text="Please enter your First Name Below",font=("Trebuchet MS",30),text_color="black")
    first_text.grid(row=0,column=0,pady=(150,0),padx=(100,0))
    first_name_input=m.ctk.CTkEntry(inner_frame,placeholder_text="Enter Here: ",font=("Trebuchet MS",15),
                                  width=300,height=40,fg_color="lightgray",text_color="#4A4A4A")
    first_name_input.grid(row=1,column=0,pady=(0,100),padx=(100,0))
    last_text = m.ctk.CTkLabel(inner_frame, text="Please enter your Last Name Below", font=("Trebuchet MS", 30),text_color="black")
    last_text.grid(row=0,column=2,pady=(150,0),padx=(0,225))
    last_name_input=m.ctk.CTkEntry(inner_frame,placeholder_text="Enter Here: ",font=("Trebuchet MS",15),
                                 width=300,height=40,fg_color="lightgray",text_color="#4A4A4A")
    last_name_input.grid(row=1,column=2,pady=(0,100),padx=(0,225))
    email_text = m.ctk.CTkLabel(inner_frame, text="Please enter your Email Below", font=("Trebuchet MS", 30),text_color="black")
    email_text.grid(row=2,column=0,pady=0,padx=(100,0))
    email_input=m.ctk.CTkEntry(inner_frame,placeholder_text="Enter Here: ",font=("Trebuchet MS",15),
                             width=300,height=40,fg_color="lightgray",text_color="#4A4A4A")
    email_input.grid(row=3,column=0,pady=(0,100),padx=(100,0))
    dob_text = m.ctk.CTkLabel(inner_frame, text="Please enter your Date of Birth Below", font=("Trebuchet MS", 30),text_color="black")
    dob_text.grid(row=2,column=2,pady=0,padx=(0,225))
    dob_input=m.ctk.CTkEntry(inner_frame,placeholder_text="Enter Here(dd/mm/yyyy): ",font=("Trebuchet MS",15),
                           width=300,height=40,fg_color="lightgray",text_color="#4A4A4A")
    dob_input.grid(row=3,column=2,pady=(0,100),padx=(0,225))
    save_changes_button=m.ctk.CTkButton(inner_frame,text="Save Changes",font=("Trebuchet MS",25),height=70,width=175,
                                      command=lambda: save_changes(first_name_input.get().strip(),last_name_input.get().strip(),
                                                                   email_input.get().strip(),dob_input.get().strip(),
                                                                   top_text,inner_frame,root,save_changes_button))
    save_changes_button.grid(row=4,column=1,pady=25)

"""Function that updates user's personal info and returns the user to the account page"""
def save_changes(new_first_name,new_last_name,new_email,new_dob,top_text,inner_frame,root,save_changes_button):
    global first,last,email,dob
    if new_first_name!="":first=new_first_name
    if new_last_name!="":last=new_last_name
    if new_email!="":email=new_email
    if new_dob!="":dob=new_dob
    save_changes_button.destroy()
    profile(top_text,inner_frame,root)

"""Function that forces the user to enter their password to delete account"""
def delete_safeguard(delete_account_button,inner_frame,root):
    delete_account_button.configure(state="disabled")
    password_entry=m.ctk.CTkEntry(inner_frame,placeholder_text="Enter Password:",
                                font=("Trebuchet MS",15),width=175,height=40)
    password_entry.grid(row=4,column=1,pady=5,padx=0)
    actually_delete_button=m.ctk.CTkButton(inner_frame,text="Actually Delete Account",font=("Trebuchet MS",18),fg_color="#960019",
                                         hover_color="#420D09",command=lambda: delete_account(password_entry.get().strip(),inner_frame,root))
    actually_delete_button.grid(row=5,column=1,pady=5,padx=0)

"""Function that deletes the user from the database and then logs the user out"""
def delete_account(password,inner_frame,root):
    if password=="temp":
        logout(root)
    else:
        error=m.ctk.CTkLabel(inner_frame,text="Incorrect Password",font=("Trebuchet MS",25),text_color="red")
        error.grid(row=6,column=1,pady=0)
        root.after(4000,error.destroy)

"""Function that logs the user out and then tells them to close the app"""
def logout(root):
    m.delete_contents(root)
    root.update_idletasks()
    h = root.winfo_screenheight()
    w = root.winfo_screenwidth()
    gradient_frame = m.ctg.GradientFrame(root, colors=("#6f2da8", "#5bb2fe"), direction="vertical",
                                       height=10,width=w // 4, corner_radius=50)
    gradient_frame.pack(pady=(100, 0))
    gradient_frame.pack_propagate(False)
    frame = m.ctk.CTkFrame(root, width=w // 4, height=h // 3 -100, fg_color='white', corner_radius=0)
    frame.pack_propagate(False)
    frame.pack()
    text=m.ctk.CTkLabel(frame,text="Thank you for using MyMoney\n\nClose the Application\nto Finish!",text_color="black",
                      font=("Trebuchet MS",25,"bold"))
    text.pack(pady=50)
