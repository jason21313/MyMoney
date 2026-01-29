import customtkinter as ctk
import CTkGradient as ctg
import sqlite3
from PIL import Image
import pandas as pd
from sqlalchemy import create_engine
import datetime

"""deletes all the contents of the inputted ctk element"""
def delete_contents(element):
    for element in element.winfo_children():
        element.destroy()


"""Function that creates the contents of the home page"""
def home(top_text,inner_frame):
    delete_contents(inner_frame)
    top_text.configure(text="MyHome")


"""Function that creates the contents of the budget page"""
def budget(top_text,inner_frame):
    delete_contents(inner_frame)
    top_text.configure(text="MyBudget")


"""Function that creates the contents of the budget page"""
def savings(top_text,inner_frame):
    delete_contents(inner_frame)
    top_text.configure(text="MySavings")


"""Function that creates the contents of the tracking page"""
def tracking(top_text,inner_frame):
    delete_contents(inner_frame)
    top_text.configure(text="MyTracking")
