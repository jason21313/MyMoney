import sections_files.misc_functions as m

#setup for sql queries throughout this file
engine = m.create_engine('sqlite:///user_database.db')
connection = m.sqlite3.connect('user_database.db')
cursor = connection.cursor()
#creates the budget table
cursor.execute("""CREATE TABLE IF NOT EXISTS budget (id INTEGER, Housing INTEGER, Transportation INTEGER, Bills INTEGER, Education INTEGER, Health INTEGER,
Food INTEGER, Savings INTEGER, Kids INTEGER, Entertainment INTEGER, Shopping INTEGER, Pets INTEGER, Travel INTEGER, Gifts INTEGER, Misc INTEGER)""")
connection.commit()
connection.close()

in_table = False
#Dictionary of all the budget categories with a description of each
categories={"Housing":"Rent/Mortgage payment, renter's/homeowner's insurance, furniture, repairs and improvements",
            "Transportation":"Gas, public transport, car maintenance, payments and insurance", "Bills":"Utilities, card payments and other monthly payments",
            "Education":"Tuition/Student Loans, books and supplies as well as room and board","Health and Wellness":"Medical insurances, co-pays, medications and gym membership",
            "Food":"Groceries and Dining Out","Savings":"Savings goals, retirement contributions and investments","Kids":"Childcare, toys, clothes and child support",
            "Entertainment":"Subscriptions and recreational activities","Shopping":"Clothes and personal wants","Pets":"Vet bills, grooming, food and toys",
            "Travel":"Tickets, hotels, taxis and food","Gifts":"Presents or Charity/Donations","Misc":"Any non-categorized expense"}

"""Function that creates the contents of the budget page"""
def budget(top_text,inner_frame):
    m.delete_contents(inner_frame)
    top_text.configure(text="MyBudget")
    # query sql to check if user is in budget table, if not prompts them to create budget
    data = m.pd.read_sql_query(f"SELECT * FROM budget WHERE id = {m.user_id}", engine).to_string()
    if data[0][0]=="E":
        guide_text = m.ctk.CTkLabel(inner_frame, text="not in table", text_color="black", font=("Trebuchet MS", 35))
        guide_text.grid(row=0, column=0, columnspan=2, sticky='n')
        survey_button = m.ctk.CTkButton(inner_frame, text="Click here to take our Budget Survey",
                                        font=("Trebuchet MS", 35),
                                        command=lambda: survey(top_text, inner_frame))
        survey_button.grid(row=1, column=0)
        create_own_button = m.ctk.CTkButton(inner_frame, text="Click here to Create your Own Budget",
                                            font=("Trebuchet MS", 35),
                                            command=lambda: create_own(top_text, inner_frame))
        create_own_button.grid(row=1, column=1)
    else:
        temp_text = m.ctk.CTkLabel(inner_frame, text="in table", text_color="black", font=("Trebuchet MS", 35))
        temp_text.pack(pady=(0, 10))

def survey(top_text,inner_frame):
    m.delete_contents(inner_frame)
    top_text.configure(text="MyBudgetSurvey")

def create_own(top_text,inner_frame):
    m.delete_contents(inner_frame)
    top_text.configure(text="MyCreateBudget")
    w=inner_frame.winfo_width()
    h=inner_frame.winfo_height()
    guide_text=m.ctk.CTkLabel(inner_frame,text="For each Category, Enter a Percentage you would like to Dedicate to that Category",text_color="black",font=("Trebuchet MS", 35))
    guide_text.pack(pady=5,anchor='n')
    scroll_frame=m.ctk.CTkScrollableFrame(inner_frame,width=w-10,height=h-50,fg_color="#bebebe")
    scroll_frame.pack(pady=5,padx=5)
    for category in categories:
        category_name=m.ctk.CTkLabel(scroll_frame,text=category,text_color="black",font=("Trebuchet MS", 35))
        category_name.pack(pady=(25,5),anchor='w')
        category_explanation=m.ctk.CTkLabel(scroll_frame,text=categories[category],text_color="black",font=("Trebuchet MS", 25))
        category_explanation.pack(pady=5,anchor='w')
        category_entry=m.ctk.CTkEntry(scroll_frame,placeholder_text="Enter Percent Here:",font=("Trebuchet MS", 20))
        category_entry.pack(pady=(5,25),anchor='w')
    create_budget_button=m.ctk.CTkButton(scroll_frame,text="Save and Create Budget",font=("Trebuchet MS", 35),
                                         command=lambda: create_budget(top_text,inner_frame))
    create_budget_button.pack(pady=10)

def create_budget(top_text,inner_frame):
    budget(top_text,inner_frame)

