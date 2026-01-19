import customtkinter as ctk
import CTkGradient as ctg
import sqlite3


def create_main(root):
    root.title("MyMoney Main Page")
    root.update_idletasks()
    h = root.winfo_screenheight()
    w = root.winfo_screenwidth()