import sections_files.misc_functions as m
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt



"""Function that creates the contents of the budget page"""
def savings(top_text,inner_frame):
    m.delete_contents(inner_frame)
    top_text.configure(text="MySavings")
    savings_label=m.ctk.CTkLabel(inner_frame,text="MyPlan",text_color="black",font=("Trebuchet MS",35,'bold'))
    savings_label.grid(row=0,column=0,columnspan=2)
    pie_chart=m.ctk.CTkButton(inner_frame,text="pretend this is a pie chart")
    pie_chart.grid(row=1,column=0)
    chart_info=m.ctk.CTkLabel(inner_frame,text="Pie chart info")
    chart_info.grid(row=1,column=1)
    goals_label=m.ctk.CTkLabel(inner_frame,text="MySavingsGoals")
    goals_label.grid(row=3,column=0,columnspan=2)
    scroll_frame=m.ctk.CTkScrollableFrame(inner_frame,width=800,height=400)
    scroll_frame.grid(row=4,column=0,columnspan=2)
    add_goal_button=m.ctk.CTkButton(inner_frame,text='add goal')
    add_goal_button.grid(row=5,column=0,columnspan=2)