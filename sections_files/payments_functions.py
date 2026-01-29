from sections_files.misc_functions import *

today=datetime.date.today().strftime("%B %d, %Y")

"""Function that creates the contents of the payments page"""
def payments(top_text,inner_frame):
    delete_contents(inner_frame)
    top_text.configure(text="MyPayments")
    date=ctk.CTkLabel(inner_frame,text=today,text_color="black")
    date.pack()
