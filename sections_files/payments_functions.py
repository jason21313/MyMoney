import sections_files.misc_functions as m

engine = m.create_engine('sqlite:///user_database.db')

today=m.datetime.date.today().strftime("%B %d, %Y")

u_id=int(m.user_id)
"""Function that creates the contents of the payments page"""
def payments(top_text,inner_frame):
    m.delete_contents(inner_frame)
    top_text.configure(text="MyPayments")
    inner_frame.grid_columnconfigure(0, weight=1)
    w=inner_frame.winfo_width()
    h=inner_frame.winfo_height()
    #left side
    date=m.ctk.CTkLabel(inner_frame,text=f"Today's Date:\n{today}",text_color="black",font=("Trebuchet MS",30))
    date.grid(row=0,column=0,pady=(10,0))
    create_button=m.ctk.CTkButton(inner_frame,text="Create Payment",command=create,font=("Trebuchet MS",30),
                                  width=250,height=60)
    create_button.grid(row=1,column=0)
    pay_button=m.ctk.CTkButton(inner_frame,text="Pay Payment",command=pay,font=("Trebuchet MS",30),
                                  width=250,height=60)
    pay_button.grid(row=2,column=0)
    edit_button=m.ctk.CTkButton(inner_frame,text="Edit Payment",command=edit,font=("Trebuchet MS",30),
                                  width=250,height=60)
    edit_button.grid(row=3,column=0)
    delete_button = m.ctk.CTkButton(inner_frame, text="Delete Payment", command=delete,font=("Trebuchet MS",30),
                                  width=250,height=60)
    delete_button.grid(row=4, column=0)


    scroll_frame = m.ctk.CTkScrollableFrame(inner_frame, width=w//2, height=h-425,fg_color="black")#"#d7d7d7")
    scroll_frame.grid(row=0,column=1,rowspan=5,sticky='e',pady=10,padx=10)
    text=m.ctk.CTkLabel(scroll_frame,text=show_payments(),font=("Trebuchet MS",20),text_color="white")
    text.pack(padx=10,pady=10)


def pay():
    print("Paying Payment")

def create():
    print("Creating Payment")

def edit():
    print("Editing Payments")

def delete():
    print("Deleting Payment")

def show_payments():
    return_string=''
    row_sep="-------------------------------"
    data=m.pd.read_sql('SELECT * FROM users_new',engine).to_string().split("\n")
    for line in data:
        return_string+=line+"\n"+row_sep+"\n"
    return return_string

