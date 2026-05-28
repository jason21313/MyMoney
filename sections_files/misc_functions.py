import customtkinter as ctk
import CTkGradient as ctg
import sqlite3
from PIL import Image
import pandas as pd
from sqlalchemy import create_engine, text
import datetime
import numpy as np

user_id=0
first=""
last=""
email=""
doob=""
engine=create_engine('sqlite:///user_database.db')


"""deletes all the contents of the inputted ctk element"""
def delete_contents(element):
    for i in range(10):
        element.grid_columnconfigure(i, weight=0)
        element.grid_rowconfigure(i, weight=0)
    for element in element.winfo_children():
        element.destroy()

"""
Function that creates a global variable of the user id for the given 
username and password to be used later in the program
"""
def create_user_id(username,password):
    global user_id
    result = pd.read_sql('SELECT * FROM users_final WHERE username = ? AND password = ? LIMIT 1',engine,params=(username,password))
    user_id = result.iloc[0]['id']

def set_name():
    global first,last,email,doob
    profile_data = pd.read_sql(f"SELECT name, dob, username FROM users_final WHERE id='{user_id}'",
                                 engine).to_numpy()
    name = "" + profile_data[0][0]
    first = name.split(" ")[0]
    last = name.split(" ")[1]
    doob = profile_data[0][1]
    email = profile_data[0][2]

