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
    pay_button=m.ctk.CTkButton(inner_frame,text="Pay Payment",command=pay,font=("Trebuchet MS",30),
                                  width=250,height=60)
    pay_button.grid(row=2,column=0)
    edit_button=m.ctk.CTkButton(inner_frame,text="Edit Payment",command=edit,font=("Trebuchet MS",30),
                                  width=250,height=60)
    edit_button.grid(row=3,column=0)
    delete_button = m.ctk.CTkButton(inner_frame, text="Delete Payment", command=delete,font=("Trebuchet MS",30),
                                  width=250,height=60)
    delete_button.grid(row=4, column=0)

    #right side of the frame, the scrollable frame that shows all payments for a user
    scroll_frame = m.ctk.CTkScrollableFrame(inner_frame, width=w//2, height=h-425,fg_color="black")#"#d7d7d7")
    scroll_frame.grid(row=0,column=1,rowspan=5,sticky='e',pady=10,padx=10)
    text=m.ctk.CTkLabel(scroll_frame,text=show_payments(),font=("Trebuchet MS",40),text_color="white")
    text.pack(padx=10,pady=10)

"""
Function that creates the content for generating new payments
"""
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
                                  command=lambda: create_payment(top_text,inner_frame,name_input.get(),amount_input.get(),date_input.get()))
    new_payment.pack()

"""
Function that enters the new payment into the database and returns the user to the payments screen
@param name the name of the payment
@param amount the amount of the payment
@param date the date the payment is due
"""
def create_payment(top_text,inner_frame,name,amount,date):
    df = pd.DataFrame({'id':[m.user_id],'name':[name],'amount':[amount],'date':[date],'paid':[False]})
    df.to_sql("payments",con=engine,if_exists="append",index=False)
    payments(top_text,inner_frame)

def pay():
    print('paying')

def edit():
    print("Editing Payments")

def delete():
    print("Deleting Payment")

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
        print(split)
        print(split[-1])
        for word in split[0:-1]:
            return_string+=word+" "
        #checks to see if the payment is paid or unpaid
        if split[-1] == '0':
            return_string+=' Unpaid'
        else:
            return_string+=' Paid'
        return_string+="\n"+row_sep+"\n"
    return return_string

