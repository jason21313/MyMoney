from numpy.ma.core import inner
from sqlalchemy.testing.plugin.plugin_base import start_test_class_outside_fixtures

import sections_files.misc_functions as m
import datetime

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
    if data[0][0]=="E":
        guide_text.configure(text="Please Create an Account")
        guide_text.grid(row=0, column=0, padx=400, pady=10)
        add_account_button.configure(text="Create Account",command=lambda: add_first(top_text, inner_frame, guide_text, add_account_button))
        add_account_button.grid(row=2, column=0, padx=400, pady=10)
    else:
        guide_text.grid(row=0, column=0, columnspan=2, padx=400, pady=10)
        accounts_frame = m.ctk.CTkScrollableFrame(inner_frame, width=800, height=400)
        accounts_frame.grid(row=1, column=0, columnspan=2,pady=5)
        create_accounts(top_text,inner_frame,accounts_frame)
        add_account_button.configure(command=lambda: add_new(top_text, inner_frame,add_account_button))
        add_account_button.grid(row=2, column=0,pady=10)
        delete_account_button = m.ctk.CTkButton(inner_frame, text='Delete',font=("Trebuchet MS", 35),width=250,height=60,
                                                command=lambda: delete_account(top_text, inner_frame, delete_account_button))
        delete_account_button.grid(row=2, column=1,pady=10)

def add_first(top_text,inner_frame,guide_text,add_account_button):
    guide_text.configure(text="Please Enter a Name and Total\n To create an Account")
    name_entry=m.ctk.CTkEntry(inner_frame,placeholder_text="Enter Name:",height=40,
                              width=250, font=("Trebuchet MS",25))
    name_entry.grid(row=1,column=0,padx=400,pady=10)
    total_entry=m.ctk.CTkEntry(inner_frame,placeholder_text="Enter Total:",height=40,
                               width=250, font=("Trebuchet MS",25))
    total_entry.grid(row=2,column=0,padx=400,pady=10)
    add_account_button.grid(row=3,column=0,padx=400,pady=10)
    add_account_button.configure(command=lambda:add_account(top_text,inner_frame,name_entry.get(),total_entry.get()))

def add_new(top_text,inner_frame,add_account_button):
    name_entry = m.ctk.CTkEntry(inner_frame, placeholder_text="Enter Name:",height=40,
                                width=250,font=("Trebuchet MS", 25))
    name_entry.grid(row=3, column=0)
    total_entry = m.ctk.CTkEntry(inner_frame, placeholder_text="Enter Total:",height=40,
                                 width=250,font=("Trebuchet MS", 25))
    total_entry.grid(row=3, column=1)
    add_account_button.configure(
        command=lambda: add_account(top_text, inner_frame, name_entry.get(), total_entry.get()))

def add_account(top_text,inner_frame,name,total):
    df = m.pd.DataFrame({"id":[m.user_id],"Name":[name],"Amount":[0],"Total":[total]})
    df.to_sql("tracking_new",con=engine,if_exists='append',index=False)
    tracking(top_text,inner_frame)

def delete_account(top_text,inner_frame,delete_account_button):
    name_entry = m.ctk.CTkEntry(inner_frame, placeholder_text="Enter Name:",height=40,width=250,font=("Trebuchet MS", 25))
    name_entry.grid(row=3, column=0,columnspan=2)
    delete_account_button.configure(
        command=lambda: delete(top_text, inner_frame, name_entry.get()))

def delete(top_text,inner_frame,name):
    with engine.begin() as con:
        con.execute(m.text(f"DELETE FROM tracking_new WHERE Name='{name}' AND id = {m.user_id}"))
    tracking(top_text,inner_frame)

def create_accounts(top_text,inner_frame,accounts_frame):
    data=m.pd.read_sql(F"SELECT DISTINCT Name FROM tracking_new WHERE id = {m.user_id}", engine).to_numpy()
    for d in data:
        name=d[0]
        account_button=m.ctk.CTkButton(accounts_frame, text=name,font=("Trebuchet MS",35),height=60,
                                       width=250,command=lambda: tracking_table(top_text,inner_frame, name))
        account_button.pack(pady=10)

def tracking_table(top_text,inner_frame,account_name):
    m.delete_contents(inner_frame)
    account_text=m.ctk.CTkLabel(inner_frame,text=account_name,font=("Trebuchet MS", 35,'bold'),text_color="black")
    account_text.grid(row=0,column=0,columnspan=3,padx=100,pady=(20,10))
    tracking_frame=m.ctk.CTkScrollableFrame(inner_frame, width=1000, height=550)
    tracking_frame.grid(row=1,column=0,columnspan=3,padx=50,pady=10)
    submit_button=m.ctk.CTkButton(inner_frame,text="Submit",font=("Trebuchet MS", 35))
    submit_button.grid(row=2,column=0)
    delete_button=m.ctk.CTkButton(inner_frame,text="Delete",font=("Trebuchet MS", 35))
    delete_button.grid(row=2,column=1)
    back_button=m.ctk.CTkButton(inner_frame,text="Back to Accounts",font=("Trebuchet MS", 35),
                                command=lambda: tracking(top_text,inner_frame))
    back_button.grid(row=2,column=2)
