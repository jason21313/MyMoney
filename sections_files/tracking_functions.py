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
    guide_text = m.ctk.CTkLabel(inner_frame, text="Please Select an Account", font=("Trebuchet MS", 35),
                                text_color='black')
    add_account_button = m.ctk.CTkButton(inner_frame, text='Add')
    if data[0][0]=="E":
        guide_text.configure(text="Please Create an Account")
        guide_text.grid(row=0, column=0, padx=400, pady=10)
        add_account_button.configure(command=lambda: add_first(top_text, inner_frame, guide_text, add_account_button))
        add_account_button.grid(row=2, column=0, padx=400, pady=10)
    else:
        guide_text.grid(row=0, column=0, columnspan=2, padx=400, pady=10)
        accounts_frame = m.ctk.CTkScrollableFrame(inner_frame, width=800, height=400)
        accounts_frame.grid(row=1, column=0, columnspan=2)
        create_accounts(accounts_frame)
        add_account_button.configure(command=lambda: add_new(top_text, inner_frame))
        add_account_button.grid(row=2, column=0)
        delete_account_button = m.ctk.CTkButton(inner_frame, text='Delete')
        delete_account_button.grid(row=2, column=1)

def add_first(top_text,inner_frame,guide_text,add_account_button):
    guide_text.configure(text="Please Enter a Name and Total\n To create an Account")
    name_entry=m.ctk.CTkEntry(inner_frame,placeholder_text="Enter Name:")
    name_entry.grid(row=1,column=0,padx=400,pady=10)
    total_entry=m.ctk.CTkEntry(inner_frame,placeholder_text="Enter Total:")
    total_entry.grid(row=2,column=0,padx=400,pady=10)
    add_account_button.grid(row=3,column=0,padx=400,pady=10)
    add_account_button.configure(command=lambda:add_account(top_text,inner_frame,name_entry.get(),total_entry.get()))

def add_new(top_text,inner_frame):
    pass

def add_account(top_text,inner_frame,name,total):
    df = m.pd.DataFrame({"id":[m.user_id],"Name":[name],"Amount":[0],"Total":[total]})
    df.to_sql("tracking_new",con=engine,if_exists='append',index=False)
    tracking(top_text,inner_frame)

def create_accounts(accounts_frame):
    pass
