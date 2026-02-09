import sections_files.misc_functions as m
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

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
def budget(top_text,inner_frame,root):
    m.delete_contents(inner_frame)
    top_text.configure(text="MyBudget")
    # query sql to check if user is in budget table, if not prompts them to create budget
    data = m.pd.read_sql_query(f"SELECT * FROM budget_new WHERE id = {m.user_id}", engine).to_string()
    if data[0][0]=="E":
        #basic GUI for any user who does not have a budget
        guide_text = m.ctk.CTkLabel(inner_frame, text="It looks like you haven't Created a Budget yet\nTo do so you can Either:",
                                    text_color="black", font=("Trebuchet MS", 45))
        guide_text.grid(row=0, column=0, padx=225,pady=(20,40))
        survey_text = m.ctk.CTkLabel(inner_frame,text="Click Below to take our Budget Survey",
                                    text_color="black", font=("Trebuchet MS", 40))
        survey_text.grid(row=1, column=0,pady=(10,5))
        survey_button = m.ctk.CTkButton(inner_frame, text="Click Here!",font=("Trebuchet MS", 35),height=60,
                                        width=250,command=lambda: survey(top_text, inner_frame,root))
        survey_button.grid(row=2, column=0,pady=(0,20))
        own_text = m.ctk.CTkLabel(inner_frame,text="OR\n\nClick Below to Create your Own Budget",
                                  text_color="black", font=("Trebuchet MS", 40))
        own_text.grid(row=3, column=0,pady=(10,5))
        create_own_button = m.ctk.CTkButton(inner_frame, text="Click Here!",font=("Trebuchet MS", 35),height=60,
                                            width=250,command=lambda: create_own(top_text, inner_frame,root,False))
        create_own_button.grid(row=4, column=0)
    else:
        #if the user has a budget it takes them to that screen
        in_table(top_text, inner_frame,root)

"""Function that creates the contents of the page where a user has a budget"""
def in_table(top_text,inner_frame,root):
    m.delete_contents(inner_frame)
    #list of percentages for each category in the user's budget
    budget_percents = []
    #list of categories in the user's budget
    labels = ["Housing", 'Transportation', 'Bills', 'Education', 'Health and Wellness', 'Food', 'Savings',
              'Kids', 'Entertainment', 'Shopping', 'Pets', 'Travel', 'Gifts', 'Misc']
    #places the percentages into the list, removes the ones that are 0
    df = m.pd.read_sql(f"SELECT * FROM budget_new WHERE id = {m.user_id}", engine).to_numpy()
    for i in range(2, df.size):
        budget_percents.append(int(df[0][i]))
    i = 0
    for percent in budget_percents:
        if percent == 0:
            budget_percents.pop(i)
            labels.pop(i)
        i += 1
    i = 0
    for percent in budget_percents:
        if percent == 0:
            budget_percents.pop(i)
            labels.pop(i)
        i += 1
    #sets the user's income as a variable
    income=int(df[0][1])
    #creates pie chart
    create_chart(inner_frame,root,labels,budget_percents,8)
    #buttons to display number amounts of categories per time periods
    explanation_text=m.ctk.CTkLabel(inner_frame,text="For Different Budget Breakdowns\nClick the Following"
                                    ,text_color="black", font=("Trebuchet MS", 35,'bold'))
    explanation_text.grid(row=0,column=1,pady=(40,0))
    show_yearly=m.ctk.CTkButton(inner_frame,text="Show Yearly Budget",font=("Trebuchet MS", 35),height=60,width=350,
                                command=lambda:show(top_text, inner_frame,root,1,income,labels,budget_percents))
    show_yearly.grid(row=1,column=1,pady=(0,5))
    show_monthly=m.ctk.CTkButton(inner_frame,text="Show Monthly Budget",font=("Trebuchet MS", 35),height=60,width=350,
                                 command=lambda:show(top_text, inner_frame,root,12,income,labels,budget_percents))
    show_monthly.grid(row=2,column=1)
    show_daily=m.ctk.CTkButton(inner_frame,text="Show Weekly Budget",font=("Trebuchet MS", 35),height=60,width=350,
                               command=lambda:show(top_text, inner_frame,root,52,income,labels,budget_percents))
    show_daily.grid(row=3,column=1)
    #button to edit your budget
    edit_text=m.ctk.CTkLabel(inner_frame,text='To Edit your Current Budget\nClick the Below',
                             text_color='black',font=("Trebuchet MS", 35,'bold'))
    edit_text.grid(row=4,column=1)
    edit_button=m.ctk.CTkButton(inner_frame,text="Edit Budget",font=("Trebuchet MS", 35),height=60,width=350,
                                command=lambda: create_own(top_text,inner_frame,root,True))
    edit_button.grid(row=5,column=1)

"""
Function used to easily display the budget as a pie chart

@:param labels list of all categories the user has in budget
@:param budget_percents list of all percentages for user's categories
@:param rows what the rowspan of the widget will be
"""
def create_chart(inner_frame,root,labels,budget_percents,rows):
    #converts the list of %s to a numpy array
    sizes = m.np.array(budget_percents)
    #list of colors to be used in the pie chart
    colors=["#82B2C0","#8dcc7e","#FFA5C5","#FF746C","#B399DD",
            "#BCD8EC","#EECE9D","#D6E5BD","#DCCCEC","#FFEE8C",
            "#FFCBE1","#B3D1E7","#ACC791","#BFC1CE","#D28A8C"]
    #creation of the pie chart with matplotlib
    fig, ax = plt.subplots(figsize=(12, 12))
    fig.patch.set_facecolor('#d7d7d7')
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90,
           textprops={'size':18},colors=colors)
    ax.axis('equal')
    #puts the pie chart into ctk and the frame
    pie_ctk = FigureCanvasTkAgg(fig, master=inner_frame)
    pie_ctk.draw()
    pie_ctk.get_tk_widget().grid(row=0, column=0, rowspan=rows)
    #prevents a matplot bug on program close
    root.protocol("WM_DELETE_WINDOW", plt.close("all"))

"""
Function that shows the amount per percentage in each
category for an inputted time period

@:param amount time period for calculate, year/month/week
@:param income the user's income
@:param labels list of all categories the user has in budget
@:param budget_percents list of all percentages for user's categories
"""
def show(top_text,inner_frame,root,amount,income,labels,budget_percents):
    m.delete_contents(inner_frame)
    # creates pie chart
    create_chart(inner_frame, root, labels, budget_percents, 5)
    #changes the top text/guide text to the format that is being displayed
    guide_text = m.ctk.CTkLabel(inner_frame, text='',font=("Trebuchet MS", 35, 'bold'), text_color="black")
    guide_text.grid(row=1, column=1, padx=(50, 10), sticky='s')
    if amount==1:
        top_text.configure(text="MyShowYearlyBudget")
        guide_text.configure(text="Displaying Yearly Budget")
    elif amount==12:
        top_text.configure(text="MyShowMonthlyBudget")
        guide_text.configure(text="Displaying Monthly Budget")
    else:
        top_text.configure(text="MyShowWeeklyBudget")
        guide_text.configure(text="Displaying Weekly Budget")
    #loops through all the percentages and puts in into a string form
    amount_text=''
    for i in range(0,len(labels)-1):
        if budget_percents[i]==0:
            pass
        elif i==len(labels)-1:
            amount_text += f"{labels[i]}: ${round(((budget_percents[i] / 100) * income) / amount, 2)}"
        else:
            amount_text+=f"{labels[i]}: ${round(((budget_percents[i]/100)*income)/amount,2)}\n"
    spending_amounts = m.ctk.CTkLabel(inner_frame, text=amount_text, font=("Trebuchet MS", 30,'bold'), text_color="black")
    spending_amounts.grid(row=2,column=1,padx=(20,10))
    #button for returning back to the in_table screen
    go_back=m.ctk.CTkButton(inner_frame,text="Return to Budget Page",font=("Trebuchet MS", 35),height=60,
                            width=350,command=lambda:budget(top_text,inner_frame,root))
    go_back.grid(row=3,column=1,sticky='n')

"""Function that allows the user to take a survey to create their budget"""
def survey(top_text,inner_frame,root):
    """this is not implemented yet"""
    m.delete_contents(inner_frame)
    top_text.configure(text="MyBudgetSurvey")
    #button to go back to hope page
    go_back = m.ctk.CTkButton(inner_frame, text="Return to Budget Page", font=("Trebuchet MS", 35),height=60,
                              width=350,command=lambda:budget(top_text,inner_frame,root))
    go_back.pack(pady=20)


"""
Function that will create a scroll frame where the user will enter all percentages they
would like for the categories in the budget

@:param editing boolean value to show if the user is editing(true) or creating(false),
                used for returning user to proper spot
"""
def create_own(top_text,inner_frame,root,editing):
    m.delete_contents(inner_frame)
    top_text.configure(text="MyCreateBudget")
    w = inner_frame.winfo_width()
    h = inner_frame.winfo_height()
    #dictionary that will be used to more easily track all the inputs of the entries
    category_entries_dict = {}
    #scroll frame where all the entries will be
    scroll_frame=m.ctk.CTkScrollableFrame(inner_frame,width=w-10,height=h-10,fg_color="#bebebe",label_text_color="black",
                                          label_fg_color="#bebebe",label_font=("Trebuchet MS", 35,"underline"),
                                          label_text="For each Category, Enter a Percentage you would like to Dedicate to that Category")
    scroll_frame.pack(pady=5,padx=5)
    #income entry
    income_explanation = m.ctk.CTkLabel(scroll_frame, text="Please Enter a Rough Post Tax Income", text_color="black",
                                         font=("Trebuchet MS", 35))
    income_explanation.pack(pady=5, anchor='w')
    income_entry = m.ctk.CTkEntry(scroll_frame, placeholder_text="Enter Income Here:", font=("Trebuchet MS", 20),
                                  width=200)
    income_entry.pack(pady=(5, 25), anchor='w')
    #for loop that creates the entries for all the budget categories
    for category in categories:
        category_name=m.ctk.CTkLabel(scroll_frame,text=category,text_color="black",font=("Trebuchet MS", 35))
        category_name.pack(pady=(25,5),anchor='w')
        category_explanation=m.ctk.CTkLabel(scroll_frame,text=categories[category],text_color="black",font=("Trebuchet MS", 25))
        category_explanation.pack(pady=5,anchor='w')
        category_entry=m.ctk.CTkEntry(scroll_frame,placeholder_text="Enter Percent Here:",font=("Trebuchet MS", 20),
                                      width=200)
        category_entry.pack(pady=(5,25),anchor='w')
        category_entries_dict[category]=category_entry
    create_budget_button=m.ctk.CTkButton(scroll_frame,text="Save and Create Budget",font=("Trebuchet MS", 35),height=60,width=350,
                                         command=lambda: create_budget(top_text,inner_frame,root,category_entries_dict,income_entry))
    create_budget_button.pack(pady=10)
    #check to see if the user is creating a budget or editing an existing one
    go_back = m.ctk.CTkButton(scroll_frame, text="Return to Budget Page", font=("Trebuchet MS", 35),
                              height=60,width=350)
    if editing:
        go_back.configure(command=lambda: in_table(top_text,inner_frame,root))
    else:
        go_back.configure(command=lambda: budget(top_text,inner_frame,root))
    go_back.pack(pady=10)

"""
Function that queries to the SQL table to create/edit a budget

@:param category_entries_dict dictionary containing all the entries and
        the user's percentages for the various categories in the budget
@:param income_entry where the user's income will be drawn from
"""
def create_budget(top_text,inner_frame,root,category_entries_dict,income_entry):
    #check to see if all the numbers the user entered adds up to 100
    #also checks to see if user left anything blank
    total_percent=0
    for cat in category_entries_dict:
        if category_entries_dict[cat].get()=='':
            pass
        else:
            total_percent+=int(category_entries_dict[cat].get())
    if total_percent!=100:
        pass
    else:
        #pandas DataFrame that represents the categories and the user's information
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
        #queries the sql table to create/edit a budget
        budget_df.to_sql('budget_new', con=engine, if_exists='replace',index=False)
        #sends the user to the view of a user in with a budget
        budget(top_text,inner_frame,root)

