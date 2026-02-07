import sections_files.misc_functions as m
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#setup for sql queries throughout this file
engine = m.create_engine('sqlite:///user_database.db')
connection = m.sqlite3.connect('user_database.db')
cursor = connection.cursor()
#creates the budget table
cursor.execute("""CREATE TABLE IF NOT EXISTS budget_new (id INTEGER, Income INTEGER, Housing INTEGER, Transportation INTEGER, Bills INTEGER, Education INTEGER, Health INTEGER,
Food INTEGER, Savings INTEGER, Kids INTEGER, Entertainment INTEGER, Shopping INTEGER, Pets INTEGER, Travel INTEGER, Gifts INTEGER, Misc INTEGER)""")
connection.commit()
connection.close()

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
    data = m.pd.read_sql_query(f"SELECT * FROM budget_new WHERE id = {m.user_id}", engine).to_string()
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
        in_table(top_text, inner_frame)

def in_table(top_text,inner_frame):
    temp_text = m.ctk.CTkLabel(inner_frame, text="in table", text_color="black", font=("Trebuchet MS", 35))
    temp_text.pack(pady=(0, 10))
    sizes=m.np.array(m.pd.read_sql(f"SELECT * FROM budget_new WHERE id = {m.user_id}", engine).to_numpy())
    labels=["Housing",'Transportation','Bills','Education','Health and Wellness','Food', 'Savings',
            'Kids', 'Entertainment','Shopping', 'Pets','Travel','Gifts','Misc']
    pie_chart=m.plt.pie(sizes, labels=labels)
    pie_ctk=FigureCanvasTkAgg(pie_chart, master=inner_frame)
    pie_ctk.get_tk_widget().pack()


def survey(top_text,inner_frame):
    m.delete_contents(inner_frame)
    top_text.configure(text="MyBudgetSurvey")

def create_own(top_text,inner_frame):
    m.delete_contents(inner_frame)
    top_text.configure(text="MyCreateBudget")
    category_entries_dict = {}
    w=inner_frame.winfo_width()
    h=inner_frame.winfo_height()
    guide_text=m.ctk.CTkLabel(inner_frame,text="For each Category, Enter a Percentage you would like to Dedicate to that Category",text_color="black",font=("Trebuchet MS", 35))
    guide_text.pack(pady=5,anchor='n')
    scroll_frame=m.ctk.CTkScrollableFrame(inner_frame,width=w-10,height=h-50,fg_color="#bebebe")
    scroll_frame.pack(pady=5,padx=5)
    income_explanation = m.ctk.CTkLabel(scroll_frame, text="Please Enter a Rough Post Tax Income", text_color="black",
                                         font=("Trebuchet MS", 35))
    income_explanation.pack(pady=5, anchor='w')
    income_entry = m.ctk.CTkEntry(scroll_frame, placeholder_text="Enter Income Here:", font=("Trebuchet MS", 20),
                                  width=200)
    income_entry.pack(pady=(5, 25), anchor='w')
    for category in categories:
        category_name=m.ctk.CTkLabel(scroll_frame,text=category,text_color="black",font=("Trebuchet MS", 35))
        category_name.pack(pady=(25,5),anchor='w')
        category_explanation=m.ctk.CTkLabel(scroll_frame,text=categories[category],text_color="black",font=("Trebuchet MS", 25))
        category_explanation.pack(pady=5,anchor='w')
        category_entry=m.ctk.CTkEntry(scroll_frame,placeholder_text="Enter Percent Here:",font=("Trebuchet MS", 20),
                                      width=200)
        category_entry.pack(pady=(5,25),anchor='w')
        category_entries_dict[category]=category_entry
    create_budget_button=m.ctk.CTkButton(scroll_frame,text="Save and Create Budget",font=("Trebuchet MS", 35),
                                         command=lambda: create_budget(top_text,inner_frame,category_entries_dict,income_entry))
    create_budget_button.pack(pady=10)

def create_budget(top_text,inner_frame,category_entries_dict,income_entry):
    total_percent=0
    for cat in category_entries_dict:
        total_percent+=int(category_entries_dict[cat].get())
    if total_percent!=100:
        pass
    else:
        budget_df=m.pd.DataFrame({'id':[m.user_id], "Income":[income_entry.get()],
                                  'Housing':[category_entries_dict['Housing'].get()],
                                  'Transportation': [category_entries_dict['Transportation'].get()],
                                  'Bills': [category_entries_dict['Bills'].get()],'Education': [category_entries_dict['Education'].get()],
                                  'Health and Wellness': [category_entries_dict['Health and Wellness'].get()],
                                  'Food': [category_entries_dict['Food'].get()], 'Savings': [category_entries_dict['Savings'].get()],
                                  'Kids': [category_entries_dict['Kids'].get()], 'Entertainment': [category_entries_dict['Entertainment'].get()],
                                  'Shopping': [category_entries_dict['Shopping'].get()], 'Pets': [category_entries_dict['Pets'].get()],
                                  'Travel': [category_entries_dict['Travel'].get()],'Gifts': [category_entries_dict['Gifts'].get()],
                                  'Misc': [category_entries_dict['Misc'].get()]})
        budget_df.to_sql('budget_new', con=engine, if_exists='replace',index=False)
        budget(top_text,inner_frame)

