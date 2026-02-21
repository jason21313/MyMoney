from numpy.ma.core import inner
from sqlalchemy.testing.plugin.plugin_base import start_test_class_outside_fixtures

import sections_files.misc_functions as m

#setup for sql queries throughout this file
engine=m.create_engine('sqlite:///user_database.db')
connection = m.sqlite3.connect('user_database.db')
cursor = connection.cursor()
#create table
cursor.execute("""CREATE TABLE IF NOT EXISTS tracking_new (id INTEGER, Name TEXT, Date TEXT,Category TEXT, Payee TEXT, Amount INTEGER, Total INTEGER)""")
connection.commit()
connection.close()


"""Function that creates the contents of the tracking page"""
def tracking(top_text,inner_frame):
    data = m.pd.read_sql_query(f"SELECT Name,Date,Category,Payee,Amount,Total FROM tracking_new WHERE id = {m.user_id}", engine).to_string()
    m.delete_contents(inner_frame)
    top_text.configure(text="MyTracking")
    guide_text = m.ctk.CTkLabel(inner_frame, text="Please Select an Account",text_color='black',
                                font=("Trebuchet MS", 35,'bold'))
    add_account_button = m.ctk.CTkButton(inner_frame, text='Add',font=("Trebuchet MS", 35),
                                         width=250,height=60)
    #checks to see if user has any accounts or not
    if data[0][0]=="E":
        #if not it prompts them to create an account
        guide_text.configure(text="Please Enter a Name and Total\n To create an Account")
        guide_text.grid(row=0, column=0)
        name_entry = m.ctk.CTkEntry(inner_frame, placeholder_text="Enter Name:", height=40,
                                    width=250, font=("Trebuchet MS", 25))
        name_entry.grid(row=1, column=0, padx=400, pady=10)
        total_entry = m.ctk.CTkEntry(inner_frame, placeholder_text="Enter Total:", height=40,
                                     width=250, font=("Trebuchet MS", 25))
        total_entry.grid(row=2, column=0, padx=400, pady=10)
        add_account_button.grid(row=3, column=0, padx=400, pady=10)
        add_account_button.configure(
            command=lambda: add_account(top_text, inner_frame, name_entry.get(), total_entry.get()))
    else:
        #otherwise brings a user to an account selection screen
        guide_text.grid(row=0, column=0, columnspan=5, padx=400, pady=10)
        accounts_frame = m.ctk.CTkScrollableFrame(inner_frame, width=800, height=400)
        accounts_frame.grid(row=1, column=0, columnspan=5,pady=5)
        create_accounts(top_text,inner_frame,accounts_frame)
        #functionality to add and delete accounts
        name_entry = m.ctk.CTkEntry(inner_frame, placeholder_text="Enter Name:", height=40,
                                    width=250, font=("Trebuchet MS", 25))
        total_entry = m.ctk.CTkEntry(inner_frame, placeholder_text="Enter Total:", height=40,
                                     width=250, font=("Trebuchet MS", 25))
        add_account_button.configure(command=lambda: add_new(top_text, inner_frame,add_account_button,name_entry,total_entry))
        add_account_button.grid(row=2, column=1,pady=10)
        cancel_button = m.ctk.CTkButton(inner_frame, text='Cancel', font=("Trebuchet MS",35),width=250,height=60,
                                        command=lambda: cancel(top_text,inner_frame,name_entry,total_entry,add_account_button,delete_account_button))
        cancel_button.grid(row=2, column=2,pady=10)
        delete_account_button = m.ctk.CTkButton(inner_frame, text='Delete',font=("Trebuchet MS", 35),width=250,height=60,
                                                command=lambda: delete_account(top_text, inner_frame, delete_account_button,name_entry))
        delete_account_button.grid(row=2, column=3,pady=10)

"""Function that gives user ability to create new account"""
def add_new(top_text,inner_frame,add_account_button,name_entry,total_entry):
    name_entry.grid(row=3, column=1)
    total_entry.grid(row=3, column=3)
    add_account_button.configure(
        command=lambda: add_account(top_text, inner_frame, name_entry.get(), total_entry.get()))

"""Function that adds account"""
def add_account(top_text,inner_frame,name,total):
    df = m.pd.DataFrame({"id":[m.user_id],"Name":[name],"Amount":[0],"Total":[total]})
    df.to_sql("tracking_new",con=engine,if_exists='append',index=False)
    tracking(top_text,inner_frame)

"""Function that gives user ability to delete an account"""
def delete_account(top_text,inner_frame,delete_account_button,name_entry):
    name_entry.grid(row=3, column=1,columnspan=3)
    delete_account_button.configure(
        command=lambda: delete(top_text, inner_frame, name_entry.get()))

"""Function that deletes account"""
def delete(top_text,inner_frame,name):
    with engine.begin() as con:
        con.execute(m.text(f"DELETE FROM tracking_new WHERE Name='{name}' AND id = {m.user_id}"))
    tracking(top_text,inner_frame)

"""Function to reset account selecting screen"""
def cancel(top_text,inner_frame,name_entry,total_entry,add_account_button,delete_account_button):
    name_entry.grid_forget()
    total_entry.grid_forget()
    add_account_button.configure(command=lambda: add_new(top_text, inner_frame,add_account_button,name_entry,total_entry))
    delete_account_button.configure(command=lambda: delete_account(top_text, inner_frame, delete_account_button,name_entry))

"""Function that displays all the user's accounts"""
def create_accounts(top_text,inner_frame,accounts_frame):
    data=m.pd.read_sql(F"SELECT DISTINCT Name FROM tracking_new WHERE id = {m.user_id}", engine).to_numpy()
    for d in data:
        name=d[0]
        account_button=m.ctk.CTkButton(accounts_frame, text=name,font=("Trebuchet MS",35),height=60,
                                       width=250,command=lambda: tracking_table(top_text,inner_frame, name))
        account_button.pack(pady=10)

"""
Function that displays the tracking of an account
@:param account_name the account displayed
"""
def tracking_table(top_text,inner_frame,account_name):
    m.delete_contents(inner_frame)
    data = m.pd.read_sql_query(f"SELECT Name,Date,Category,Payee,Amount,Total FROM tracking_new WHERE id = {m.user_id}",
                               engine).to_numpy()
    account_text=m.ctk.CTkLabel(inner_frame,text=account_name,font=("Trebuchet MS", 35,'bold'),text_color="black")
    account_text.grid(row=0,column=0,columnspan=3,padx=100,pady=(20,5))
    tracking_frame=m.ctk.CTkScrollableFrame(inner_frame, width=1000, height=500)
    tracking_frame.grid(row=1,column=0,columnspan=3,padx=50,pady=10)
    #inputs to enter the information for the tracked changes
    tracking_input_frame=m.ctk.CTkFrame(inner_frame, width=1000, height=70)
    tracking_input_frame.grid(row=2,column=0,columnspan=3,padx=50,pady=10)
    tracking_input_frame.grid_propagate(False)
    date_track=m.ctk.CTkEntry(tracking_input_frame,placeholder_text=m.datetime.date.today().strftime("%m/%d/%Y"),height=40,)
    date_track.grid(row=0,column=1,pady=10,padx=10)
    cat_track=m.ctk.CTkOptionMenu(tracking_input_frame,height=40,values=['Enter Category',"Income","Housing","Transportation","Bills",
                                                                         "Education","Health and Wellness","Food","Savings","Kids",
                                                                         "Entertainment","Shopping","Pets","Travel","Gifts","Misc"])
    cat_track.grid(row=0,column=2,pady=10,padx=10)
    payee_track=m.ctk.CTkEntry(tracking_input_frame,placeholder_text="Enter Payee:",height=40,)
    payee_track.grid(row=0,column=3,pady=10,padx=10)
    deposit_track=m.ctk.CTkEntry(tracking_input_frame,placeholder_text="Enter Deposit:",height=40,)
    deposit_track.grid(row=0,column=4,pady=10,padx=10)
    withdrawal_track=m.ctk.CTkEntry(tracking_input_frame,placeholder_text="Enter Withdrawal:",height=40,)
    withdrawal_track.grid(row=0,column=5,pady=10,padx=10)
    entries=[date_track,cat_track,payee_track,deposit_track,withdrawal_track]
    #buttons to add or delete based on the inputs, also allows user to return to accounts page
    submit_button=m.ctk.CTkButton(inner_frame,text="Submit",font=("Trebuchet MS", 35),width=250,
                                  command=lambda: add_track(top_text,inner_frame,account_name,entries,data))
    submit_button.grid(row=3,column=0)
    delete_button=m.ctk.CTkButton(inner_frame,text="Delete",font=("Trebuchet MS", 35),width=250,
                                  command=lambda: del_track(top_text,inner_frame,account_name,entries))
    delete_button.grid(row=3,column=1)
    back_button=m.ctk.CTkButton(inner_frame,text="Back to Accounts",font=("Trebuchet MS", 35),
                                width=250,command=lambda: tracking(top_text,inner_frame))
    back_button.grid(row=3,column=2)
    show_table(tracking_frame,data)

"""Function that adds a tracked change to the table"""
def add_track(top_text,inner_frame,account_name,entries,data):
    #sets the date if left empty
    if entries[0].get() == "":
        date = m.datetime.date.today().strftime("%m/%d/%Y")
    else:
        date = entries[0].get()
    #checks to see that no important info is left out
    if entries[2].get()=="" or entries[1].get()=="Enter Category":
        tracking_table(top_text, inner_frame, account_name)
    #checks to see if neither deposit or withdrawal was used
    elif entries[3].get() == "" and entries[4].get() == "":
        tracking_table(top_text, inner_frame, account_name)
    else:
        #otherwise checks if the change is a deposit or a withdrawal
        if entries[3].get()=="":
            #withdrawal
            df=m.pd.DataFrame({"id":[m.user_id],"Name":[account_name],"Date":[date],"Category":[entries[1].get()],
                               "Payee":[entries[2].get()],"Amount":[-int(entries[4].get())],"Total":[data[-1][5]-int(entries[4].get())]})
            df.to_sql("tracking_new",con=engine,if_exists="append",index=False)
            tracking_table(top_text,inner_frame,account_name)
        elif entries[4].get()=="":
            #deposit
            df = m.pd.DataFrame({"id": [m.user_id], "Name": [account_name], "Date": [date],"Category": [entries[1].get()],
                                 "Payee": [entries[2].get()], "Amount": [int(entries[3].get())],"Total":[data[-1][5]+int(entries[3].get())]})
            df.to_sql("tracking_new", con=engine, if_exists="append", index=False)
            tracking_table(top_text,inner_frame,account_name)

"""Function that deletes a tracked change from the table"""
def del_track(top_text,inner_frame,account_name,entries):
    # sets the date if left empty
    if entries[0].get() == "":
        date = m.datetime.date.today().strftime("%m/%d/%Y")
    else:
        date = entries[0].get()
    #deletes the inputted change
    with engine.begin() as con:
        con.execute(m.text(f"DELETE FROM tracking_new WHERE id = {m.user_id} AND Name='{account_name}' AND Date = '{date}' AND Category='{entries[1].get()}' AND Payee='{entries[2].get()}'",))
    tracking_table(top_text,inner_frame,account_name)

"""Function that displays all tracked changes for an account"""
def show_table(tracking_frame,data):
    tracking_label = m.ctk.CTkLabel(tracking_frame,text='',font=("Consolas", 25),text_color="white")
    string=''
    cats={  "Income": "       Income      ",
    "Housing": "      Housing     ",
    "Transportation": " Transportation",
    "Bills": "       Bills       ",
    "Education": "     Education    ",
    "Health and Wellness": "Health and Wellness",
    "Food": "        Food       ",
    "Savings": "      Savings     ",
    "Kids": "        Kids       ",
    "Entertainment": "  Entertainment  ",
    "Shopping": "     Shopping     ",
    "Pets": "        Pets       ",
    "Travel": "       Travel      ",
    "Gifts": "       Gifts       ",
    "Misc": "        Misc       "}
    for d in data:
        if d[4]==0:
            pass
        elif d[4]>0:
            #deposit
            string += d[1] +" | " + cats[d[2]] + " | " + str(d[3]) + " | " + str(d[4]) + " |    | " + str(d[5]) + "\n"
        else:
            #withdrawal
            string += d[1]+" | "+cats[d[2]]+" | "+str(d[3])+" |    | "+str(abs(d[4]))+" | "+str(d[5])+"\n"
    tracking_label.configure(text=string)
    tracking_label.pack(anchor='w')
