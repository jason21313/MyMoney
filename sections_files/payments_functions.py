import sections_files.misc_functions as m

engine = m.create_engine('sqlite:///user_database.db')

today=m.datetime.date.today().strftime("%B %d, %Y")

"""Function that creates the contents of the payments page"""
def payments(top_text,inner_frame):
    m.delete_contents(inner_frame)
    print(m.user_id)
    top_text.configure(text="MyPayments")
    date=m.ctk.CTkLabel(inner_frame,text=today,text_color="black")
    date.pack()
