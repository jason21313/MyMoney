import customtkinter as ctk
import CTkGradient as ctg
import sqlite3
from PIL import Image
import pandas as pd
from sqlalchemy import create_engine, text
import datetime
import numpy as np
import matplotlib.pyplot as plt

user_id=0

"""deletes all the contents of the inputted ctk element"""
def delete_contents(element):
    for element in element.winfo_children():
        element.destroy()

"""
Function that creates a global variable of the user id for the given 
username and password to be used later in the program
"""
def create_user_id(username,password):
    global user_id
    engine = create_engine('sqlite:///user_database.db')
    result = pd.read_sql('SELECT * FROM users_new WHERE username = ? AND password = ? LIMIT 1',engine,params=(username,password))
    user_id = result.iloc[0]['id']
    print(user_id)




"""Function that creates the contents of the home page"""
def home(top_text,inner_frame):
    delete_contents(inner_frame)
    top_text.configure(text="MyHome")


"""Function that creates the contents of the budget page"""
def savings(top_text,inner_frame):
    delete_contents(inner_frame)
    top_text.configure(text="MySavings")


"""Function that creates the contents of the tracking page"""
def tracking(top_text,inner_frame):
    delete_contents(inner_frame)
    top_text.configure(text="MyTracking")
