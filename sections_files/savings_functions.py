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
        in_table(top_text,inner_frame,root)

        #Savings Goals aspect of savings page
        # goals_label=m.ctk.CTkLabel(inner_frame,text="MySavingsGoals",font=("Trebuchet MS", 35, 'bold'),
        #                            text_color='black')
        # goals_label.grid(row=4,column=0,columnspan=4)
        # scroll_frame=m.ctk.CTkScrollableFrame(inner_frame,width=1200,height=400)
        # scroll_frame.grid(row=5,column=0,columnspan=5)
        # add_goal_button=m.ctk.CTkButton(inner_frame,text='add goal')
        # add_goal_button.grid(row=6,column=0,columnspan=4)

""""""
def in_table(top_text,inner_frame,root):
    #list of categories in the savings plan
    labels=["Investments","Retirement","Savings Goals"]
    #queries the table to get the values for each category
    data = m.pd.read_sql(f"SELECT Investments, Retirement, SavingsGoals FROM savings_budget WHERE id={m.user_id}",
                         engine).to_numpy()
    # Savings Plan aspect of the savings page
    savings_label = m.ctk.CTkLabel(inner_frame, text="MyPlan", text_color="black",
                                   font=("Trebuchet MS", 35, 'bold'))
    savings_label.grid(row=0, column=0, columnspan=4)
    #creates the pie chart
    create_chart(inner_frame,root,data,labels)
    # buttons to display number amounts of savings per time periods
    explanation_text = m.ctk.CTkLabel(inner_frame, text_color="black", font=("Trebuchet MS", 35, 'bold'),
                                      text="For Different Budget Breakdowns\nClick the Following")
    explanation_text.grid(row=1, column=1, columnspan=3,padx=20)
    show_yearly = m.ctk.CTkButton(inner_frame, text="Year", font=("Trebuchet MS", 35),
                                  command=lambda:show(chart_info,data,labels,1))
    show_yearly.grid(row=2, column=1, pady=(0, 5),padx=(10,0))
    show_monthly = m.ctk.CTkButton(inner_frame, text="Month", font=("Trebuchet MS", 35),
                                   command=lambda: show(chart_info,data,labels,12))
    show_monthly.grid(row=2, column=2,padx=0)
    show_weekly = m.ctk.CTkButton(inner_frame, text="Week", font=("Trebuchet MS", 35),
                                  command=lambda: show(chart_info,data,labels, 52))
    show_weekly.grid(row=2, column=3,padx=(0,10))
    chart_info = m.ctk.CTkLabel(inner_frame,font=("Trebuchet MS", 35, 'bold'),text_color='black',
                                text=f"Displaying Yearly\n"
                                     f"{labels[0]}: {round(int(data[0][0])/1,2)}\n"
                                     f"{labels[1]}: {round(int(data[0][1])/1,2)}\n"
                                     f"{labels[2]}: {round(int(data[0][2])/1,2)}\n")
    chart_info.grid(row=3, column=1, columnspan=3)

"""
Function that creates the pie chart representation 
 of the user's savings plan

@:param data numpy array containing the user's information
             from the table
@:param labels the names of the three pieces of the
               savings plan
"""
def create_chart(inner_frame,root,data,labels):
    #turns the data into a list containing the values of each category
    sizes=[]
    for d in data[0]:
        sizes.append(int(d))
    #creates the pie chart in matplot
    fig, ax = plt.subplots(figsize=(7,7))
    fig.patch.set_facecolor('#d7d7d7')
    ax.pie(sizes,labels=labels,autopct='%1.1f%%',startangle=90,
           textprops={'size':15})
    ax.axis('equal')
    #turns the pie chart into a ctk widget and displays it
    pie_ctk=FigureCanvasTkAgg(fig, inner_frame)
    pie_ctk.draw()
    pie_ctk.get_tk_widget().grid(row=1,column=0,rowspan=4,padx=(30,40))
    # prevents a matplot bug on program close
    root.protocol("WM_DELETE_WINDOW", plt.close("all"))

"""
Function that changes the chart_info label to
 show data based on a given time span
 
@:param data numpy array containing the user's information
             from the table
@:param labels the names of the three pieces of the
               savings plan
@:param amount the time span
"""
def show(chart_info,data,labels,amount):
    #checks the amount to give a string that matches
    if amount==1:
        size="Yearly"
    elif amount==12:
        size="Monthly"
    else:
        size="Weekly"
    #changes the text to be for that time span
    chart_info.configure(text=f"Displaying {size}\n"
                              f"{labels[0]}: {round(int(data[0][0])/amount,2)}\n"
                              f"{labels[1]}: {round(int(data[0][1])/amount,2)}\n"
                              f"{labels[2]}: {round(int(data[0][2])/amount,2)}\n")


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