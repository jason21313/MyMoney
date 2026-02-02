import pandas as pd
import sections_files.misc_functions as m

#setup for sql queries throughout this file
engine = m.create_engine('sqlite:///user_database.db')
connection = m.sqlite3.connect('user_database.db')
cursor = connection.cursor()
#creates the payment table if it doesn't exist
cursor.execute("""CREATE TABLE IF NOT EXISTS payments (id INTEGER, name TEXT, amount INTEGER, date TEXT, paid BOOLEAN)""")
connection.commit()
connection.close()
#gets today's date
today=m.datetime.date.today().strftime("%B %d, %Y")

"""Function that creates the contents of the payments page"""
def payments(top_text,inner_frame):
    #sets up the frame for the new contents
    m.delete_contents(inner_frame)
    top_text.configure(text="MyPayments")
    inner_frame.grid_columnconfigure(0, weight=1)
    w=inner_frame.winfo_width()
    h=inner_frame.winfo_height()
    #left side of the frame, buttons for functions and today's date
    date=m.ctk.CTkLabel(inner_frame,text=f"Today's Date:\n{today}",text_color="black",font=("Trebuchet MS",30))
    date.grid(row=0,column=0,pady=(10,0))
    create_button=m.ctk.CTkButton(inner_frame,text="Create Payment",command=lambda:create(top_text,inner_frame),font=("Trebuchet MS",30),
                                  width=250,height=60)
    create_button.grid(row=1,column=0)
    pay_button=m.ctk.CTkButton(inner_frame,text="Pay Payment",command=lambda: pay(top_text,inner_frame,w,h),font=("Trebuchet MS",30),
                                  width=250,height=60)
    pay_button.grid(row=2,column=0)
    edit_button=m.ctk.CTkButton(inner_frame,text="Edit Payment",command=lambda: edit(top_text,inner_frame,w,h),font=("Trebuchet MS",30),
                                  width=250,height=60)
    edit_button.grid(row=3,column=0)
    delete_button = m.ctk.CTkButton(inner_frame, text="Delete Payment", command=lambda: delete(top_text,inner_frame,w,h),font=("Trebuchet MS",30),
                                  width=250,height=60)
    delete_button.grid(row=4, column=0)

    #right side of the frame, the scrollable frame that shows all payments for a user
    scroll_frame = m.ctk.CTkScrollableFrame(inner_frame, width=w//2, height=h-425,fg_color="black")#"#d7d7d7")
    scroll_frame.grid(row=0,column=1,rowspan=5,sticky='e',pady=10,padx=10)
    text=m.ctk.CTkLabel(scroll_frame,text=show_payments(),font=("Trebuchet MS",40),text_color="white")
    text.pack(padx=10,pady=10)


"""Function that creates the content for generating new payments"""
def create(top_text,inner_frame):
    m.delete_contents(inner_frame)
    top_text.configure(text="MyCreatePayment")
    name_input=m.ctk.CTkEntry(inner_frame,placeholder_text="Enter a Name for the Payment",width=500,height=35)
    name_input.pack()
    amount_input = m.ctk.CTkEntry(inner_frame, placeholder_text="Enter a Amount for the Payment", width=500, height=35)
    amount_input.pack()
    date_input = m.ctk.CTkEntry(inner_frame, placeholder_text="Enter a Date for the Payment", width=500, height=35)
    date_input.pack()
    new_payment = m.ctk.CTkButton(inner_frame,text="Create Payment",font=("Trebuchet MS",30),
                                  command=lambda: create_payment(top_text,inner_frame,name_input.get().strip(),amount_input.get().strip(),date_input.get().strip()))
    new_payment.pack()

"""
Function that enters the new payment into the database and returns the user to the payments screen
@:param name the name of the payment
@:param amount the amount of the payment
@:param date the date the payment is due
"""
def create_payment(top_text,inner_frame,name,amount,date):
    df = pd.DataFrame({'id':[m.user_id],'name':[name],'amount':[amount],'date':[date],'paid':[False]})
    df.to_sql("payments",con=engine,if_exists="append",index=False)
    payments(top_text,inner_frame)


"""Function that creates the content for the user to set payments as Paid/Unpaid"""
def pay(top_text,inner_frame,w,h):
    #dict of payments that will be changed,key=name value=boolean value(Paid/Unpaid)
    payments_dict={}
    m.delete_contents(inner_frame)
    top_text.configure(text="MyPayingPayments")
    #left side of the frame, shows
    guide_text=m.ctk.CTkLabel(inner_frame,text="Please Enter a Payment Name Below\nThen select Paid or Unpaid",
                              text_color="black",font=("Trebuchet MS",30))
    guide_text.grid(row=0,column=0,pady=(10,0))
    payment_entry=m.ctk.CTkEntry(inner_frame,placeholder_text="Enter Name Here: ",width=300,height=35,font=("Trebuchet MS",30))
    payment_entry.grid(row=1,column=0)
    paid_button=m.ctk.CTkButton(inner_frame,text="Click to make Payment Paid",font=("Trebuchet MS",30),
                                command=lambda: add_payment(payments_dict,payment_entry,True))
    paid_button.grid(row=2,column=0)
    unpaid_button=m.ctk.CTkButton(inner_frame,text="Click to make Payment Unpaid", font=("Trebuchet MS",30),
                                  command=lambda: add_payment(payments_dict,payment_entry,False))
    unpaid_button.grid(row=3,column=0)
    save_changes_button=m.ctk.CTkButton(inner_frame,text="Click to Save Changes",font=("Trebuchet MS",30),
                                        command=lambda: save_pay(top_text,inner_frame,payments_dict))
    save_changes_button.grid(row=4,column=0)

    # right side of the frame, the scrollable frame that shows all payments for a user
    scroll_frame = m.ctk.CTkScrollableFrame(inner_frame, width=w // 2, height=h - 425, fg_color="black")  # "#d7d7d7")
    scroll_frame.grid(row=0, column=1, rowspan=5, sticky='e', pady=10, padx=10)
    text = m.ctk.CTkLabel(scroll_frame, text=show_payments(), font=("Trebuchet MS", 40), text_color="white")
    text.pack(padx=10, pady=10)

"""
Function that adds a payment to the dict of payments to be changed.
@:param payments_dict dict of payments to be changed.
@:param payment_entry the entry where the name of the payment 
        will be drawn from.
@:param paid boolean value of True(Make Paid) or False(Make Unpaid)
"""
def add_payment(payments_dict,payment_entry,paid):
    if paid:
        payments_dict[payment_entry.get().strip()]='TRUE'
    else:
        payments_dict[payment_entry.get().strip()]='FALSE'
    payment_entry.delete(0,'end')

"""Function that updates the database with the payments to be Paid/Unpaid"""
def save_pay(top_text,inner_list,payments_dict):
    for payment in payments_dict:
        with engine.begin() as conn:
            conn.execute(m.text(f"""UPDATE payments SET paid = {payments_dict[payment]} WHERE name = '{payment}'"""))
    payments(top_text,inner_list)


def edit(top_text,inner_frame,w,h):
    m.delete_contents(inner_frame)
    top_text.configure(text="MyEditingPayments")
    # left side of the frame, shows
    guide_text = m.ctk.CTkLabel(inner_frame, text="Please Enter a Payment Name Below",
                                text_color="black", font=("Trebuchet MS", 30))
    guide_text.grid(row=0, column=0, pady=(10, 0))


    # right side of the frame, the scrollable frame that shows all payments for a user
    scroll_frame = m.ctk.CTkScrollableFrame(inner_frame, width=w // 2, height=h - 425, fg_color="black")  # "#d7d7d7")
    scroll_frame.grid(row=0, column=1, rowspan=5, sticky='e', pady=10, padx=10)
    text = m.ctk.CTkLabel(scroll_frame, text=show_payments(), font=("Trebuchet MS", 40), text_color="white")
    text.pack(padx=10, pady=10)


"""Function that creates the content for the user to delete payments"""
def delete(top_text,inner_frame,w,h):
    # list of payments that will be deleted
    payments_list = []
    m.delete_contents(inner_frame)
    top_text.configure(text="MyDeletingPayments")
    # left side of the frame, shows
    guide_text = m.ctk.CTkLabel(inner_frame, text="Please Enter a Payment Name Below\n",
                                text_color="black", font=("Trebuchet MS", 30))
    guide_text.grid(row=0, column=0, pady=(10, 0))
    payment_entry = m.ctk.CTkEntry(inner_frame, placeholder_text="Enter Name Here: ", width=300, height=35,
                                   font=("Trebuchet MS", 30))
    payment_entry.grid(row=1, column=0)
    delete_button=m.ctk.CTkButton(inner_frame,text="Click to Delete Payment",font=("Trebuchet MS", 30),
                                  command=lambda: add_delete(payments_list,payment_entry))
    delete_button.grid(row=2, column=0)
    save_changes_button = m.ctk.CTkButton(inner_frame, text="Click to Save Changes", font=("Trebuchet MS", 30),
                                          command=lambda: save_delete(top_text,inner_frame,payments_list))
    save_changes_button.grid(row=3, column=0)

    # right side of the frame, the scrollable frame that shows all payments for a user
    scroll_frame = m.ctk.CTkScrollableFrame(inner_frame, width=w // 2, height=h - 425, fg_color="black")  # "#d7d7d7")
    scroll_frame.grid(row=0, column=1, rowspan=5, sticky='e', pady=10, padx=10)
    text = m.ctk.CTkLabel(scroll_frame, text=show_payments(), font=("Trebuchet MS", 40), text_color="white")
    text.pack(padx=10, pady=10)

"""
Function that adds a payment to the list of payments to be deleted.
@:param payments_list list of payments to be deleted.
@:param payment_entry the entry where the name of the payment 
        will be drawn from.
"""
def add_delete(payments_list,payment_entry):
    payments_list.append(payment_entry.get().strip())
    payment_entry.delete(0,'end')

"""Function that updates the database with the payments to be Deleted"""
def save_delete(top_text,inner_frame,payments_list):
    for payment in payments_list:
        with engine.begin() as conn:
            conn.execute(m.text(f"""DELETE FROM payments WHERE name = '{payment}'"""))
    payments(top_text,inner_frame)


"""
Function that retrieves all payments for a the current user and turns it into a string to display
@return the sql table of the current user's payments as a string
"""
def show_payments():
    return_string=''
    row_sep="----------------------------------------------"
    data=m.pd.read_sql(f'SELECT name, amount, date, paid FROM payments WHERE id = {m.user_id}',engine).to_string(index=False).split("\n")
    #catch for a user who has no payments
    if data[0][0]=='E':
        return "No Payments"
    for line in data:
        split=line.split(" ")
        for word in split[0:-1]:
            return_string+=word+" "
        #checks to see if the payment is paid or unpaid
        if split[-1] == '0':
            return_string+=' Unpaid'
        else:
            return_string+=' Paid'
        return_string+="\n"+row_sep+"\n"
    return return_string

