import sections_files.misc_functions as m
from sections_files.budget_functions import budget
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

#setup for sql queries throughout this file
engine=m.create_engine('sqlite:///user_database.db')
connection = m.sqlite3.connect('user_database.db')
cursor = connection.cursor()
#two sql tables for savings, one for the savings budget
# aspect and the other for the savings goals aspect
#creates the savings budget table
cursor.execute("""CREATE TABLE IF NOT EXISTS savings_budget (id INTEGER, Income INTEGER, TotalSavings INTEGER, 
                  Investments INTEGER, Retirement INTEGER, SavingsGoals INTEGER)""")
#creates the savings goals table

connection.commit()
connection.close()


"""Function that creates the contents of the budget page"""
def savings(top_text,inner_frame,root):
    m.delete_contents(inner_frame)
    w=inner_frame.winfo_width()
    h=inner_frame.winfo_height()
    top_text.configure(text="MySavings")
    #queries tables to check if user has made a budget and or a savings budget
    has_budget=m.pd.read_sql(f"SELECT * FROM budget_new WHERE id = {m.user_id}",engine).to_string()
    has_savings=m.pd.read_sql(f"SELECT * FROM savings_budget WHERE id = {m.user_id}",engine).to_string()
    #if the user has no budget they are directed to create one
    if has_budget[0][0]=="E":
        guide_text=m.ctk.CTkLabel(inner_frame,text='It seems you have not made a Budget yet\nPlease Click the button Below to Create one',
                                  font=("Trebuchet MS",45,'bold'),text_color='black')
        guide_text.pack(pady=(100,20))
        budget_button=m.ctk.CTkButton(inner_frame,text='Create Budget',font=("Trebuchet MS",45),height=60,
                                      width=250,command=lambda:budget(top_text,inner_frame,root))
        budget_button.pack(pady=20)
    #the user has a budget but no savings plan and is directed to create one
    elif has_savings[0][0]=="E":
        income = int(m.pd.read_sql(f"SELECT Income FROM budget_new WHERE id = {m.user_id}",engine).iloc[0,0])
        total_savings=round(income/int(m.pd.read_sql(f"SELECT Savings FROM budget_new WHERE id = {m.user_id}",engine).iloc[0,0]),2)
        guide_text = m.ctk.CTkLabel(inner_frame,font=("Trebuchet MS", 45, 'bold'), text_color='black',
                                    text=f"It seems you don't have a Savings Plan\n "
                                         f"Based on how you are setting aside {total_savings}\n"
                                         f"Enter how you would like to Plan your Savings",)
        guide_text.pack(pady=(30,20))
        #Entries for the information for the savings plan table
        retirement_text=m.ctk.CTkLabel(inner_frame,font=("Trebuchet MS", 35),text_color='black',
                                       text="Enter an Amount for Retirement Savings")
        retirement_text.pack(pady=(20,0))
        retirement_entry=m.ctk.CTkEntry(inner_frame,placeholder_text="Enter Here:",font=("Trebuchet MS", 30),
                                        height=60,width=350)
        retirement_entry.pack(pady=(5,20))
        investments_text=m.ctk.CTkLabel(inner_frame,font=("Trebuchet MS", 35),text_color='black',
                                       text="Enter an Amount for Investments Savings")
        investments_text.pack(pady=(20,0))
        investments_entry=m.ctk.CTkEntry(inner_frame,placeholder_text="Enter Here:",font=("Trebuchet MS", 30),
                                         height=60,width=350)
        investments_entry.pack(pady=(5, 20))
        goals_text=m.ctk.CTkLabel(inner_frame,font=("Trebuchet MS", 35),text_color='black',
                                       text="Enter an Amount for Savings Goals")
        goals_text.pack(pady=(20,0))
        goals_entry=m.ctk.CTkEntry(inner_frame,placeholder_text="Enter Here:",font=("Trebuchet MS", 30),
                                   height=60,width=350)
        goals_entry.pack(pady=(5, 20))
        #list to condense the information
        values=[income,total_savings,retirement_entry,investments_entry,goals_entry]
        create_savings_button=m.ctk.CTkButton(inner_frame,text='Create Savings',font=("Trebuchet MS", 35),height=60,
                                              width=350,command=lambda:create_savings(top_text,inner_frame,root,values))
        create_savings_button.pack(pady=20)
    #the user has a budget and savings plan so they are given their info
    else:
        #Savings Plan aspect of the savings page
        savings_label=m.ctk.CTkLabel(inner_frame,text="MyPlan",text_color="black",font=("Trebuchet MS",35,'bold'))
        savings_label.grid(row=0,column=0,columnspan=5)
        pie_chart=m.ctk.CTkButton(inner_frame,text="pretend this is a pie chart")
        pie_chart.grid(row=1,column=0,rowspan=3)
        # buttons to display number amounts of savings per time periods
        explanation_text = m.ctk.CTkLabel(inner_frame, text="For Different Budget Breakdowns\nClick the Following"
                                          , text_color="black", font=("Trebuchet MS", 35, 'bold'))
        explanation_text.grid(row=1, column=1,columnspan=3)
        show_yearly = m.ctk.CTkButton(inner_frame, text="Show Yearly Budget", font=("Trebuchet MS", 35))
        show_yearly.grid(row=2, column=1, pady=(0, 5))
        show_monthly = m.ctk.CTkButton(inner_frame, text="Show Monthly Budget", font=("Trebuchet MS", 35))
        show_monthly.grid(row=2, column=2)
        show_weekly = m.ctk.CTkButton(inner_frame, text="Show Weekly Budget", font=("Trebuchet MS", 35))
        show_weekly.grid(row=2, column=3)
        chart_info=m.ctk.CTkLabel(inner_frame,text="Pie chart info",font=("Trebuchet MS", 35, 'bold'),
                                  text_color='black')
        chart_info.grid(row=3,column=1,columnspan=3)

        #Savings Goals aspect of savings page
        # goals_label=m.ctk.CTkLabel(inner_frame,text="MySavingsGoals",font=("Trebuchet MS", 35, 'bold'),
        #                            text_color='black')
        # goals_label.grid(row=4,column=0,columnspan=4)
        # scroll_frame=m.ctk.CTkScrollableFrame(inner_frame,width=1200,height=400)
        # scroll_frame.grid(row=5,column=0,columnspan=5)
        # add_goal_button=m.ctk.CTkButton(inner_frame,text='add goal')
        # add_goal_button.grid(row=6,column=0,columnspan=4)

"""
Function that creates a new savings plan in the table

@:param values list of information to be uploaded to sql table
"""
def create_savings(top_text,inner_frame,root,values):
    #checks to see if any entry was empty
    total=0
    for value in values[2:]:
        if value.get()=='':
            pass
        else:
            total+=int(value.get())
    #checks to see if amounts user entered adds up to the total savings
    # #if not nothing happens
    if total!=values[1]:
        pass
    #if so then the information is put into a DataFrame and uploaded to the table
    else:
        savings_df=m.pd.DataFrame({'id':[m.user_id],'Income':[values[0]],'TotalSavings':[values[1]],
                                   'Investments':[values[2].get()],'Retirement':[values[3].get()],
                                   'SavingsGoals':[values[4].get()]})
        savings_df.to_sql('savings_budget',engine,if_exists='replace',index=False)
        savings(top_text,inner_frame,root)