import random

from sections_files.profile_functions import *
from sections_files.payments_functions import *
from sections_files.budget_functions import *
from sections_files.savings_functions import *
from sections_files.misc_functions import *
from sections_files.tracking_functions import *

engine = m.create_engine('sqlite:///user_database.db')

"""Function that creates the initial section of the main page of the app"""
def create_main(root):
    #baseline pieces of the app
    root.title("MyMoney Main Page")
    root.update_idletasks()
    h = root.winfo_screenheight()
    w = root.winfo_screenwidth()
    outer_frame=ctk.CTkFrame(root,width=w-50,height=h-100, fg_color="#6C3BAA")
    outer_frame.pack(pady=(25,20))
    outer_frame.grid_propagate(False)

    #non-button pieces inside the outer_frame
    top_frame=ctk.CTkFrame(outer_frame,fg_color="#d7d7d7", width=w-170, height=50)
    top_frame.pack_propagate(False)
    top_frame.grid(row=0,column=0,columnspan=2,padx=60,pady=20)
    top_text=ctk.CTkLabel(top_frame,text="",text_color='black',font=("Trebuchet MS",25,"bold"))
    top_text.pack(pady=10,anchor='n')
    top_frame.pack_propagate(False)
    img=Image.open("transparent.png")
    image= ctk.CTkImage(light_image=img,dark_image=img,size=(150,150))
    image_label=ctk.CTkLabel(outer_frame,image=image,text="")
    image_label.grid(row=1,column=0,padx=10,pady=(15,0),sticky='n')

    #buttons for each section of the website
    home_b=ctk.CTkButton(outer_frame,text='Home',height=75,fg_color="#6C3BAA",hover_color="#7851A9",
                         font=("Trebuchet MS",25,"bold"),text_color='#d7d7d7', command=lambda: home(root,top_text,inner_frame,False))
    budget_b = ctk.CTkButton(outer_frame, text='Budget',height=75,fg_color="#6C3BAA",hover_color="#7851A9",
                             font=("Trebuchet MS",25,"bold"),text_color='#d7d7d7',command=lambda: budget(top_text,inner_frame,root))
    savings_b = ctk.CTkButton(outer_frame, text='Savings',height=75,fg_color="#6C3BAA",hover_color="#7851A9",
                              font=("Trebuchet MS",25,"bold"),text_color='#d7d7d7',command=lambda: savings(top_text,inner_frame,root))
    tracking_b = ctk.CTkButton(outer_frame, text='Tracking',height=75,fg_color="#6C3BAA",hover_color="#7851A9",
                               font=("Trebuchet MS",25,"bold"),text_color='#d7d7d7',command=lambda: tracking(top_text,inner_frame))
    payments_b = ctk.CTkButton(outer_frame, text='Payments',height=75,fg_color="#6C3BAA",hover_color="#7851A9",
                               font=("Trebuchet MS",25,"bold"),text_color='#d7d7d7',command=lambda: payments(top_text,inner_frame))
    profile_b = ctk.CTkButton(outer_frame, text='Profile',height=75,fg_color="#6C3BAA",hover_color="#7851A9",
                              font=("Trebuchet MS",25,"bold"),text_color='#d7d7d7',command=lambda: profile(top_text,inner_frame,root))
    home_b.grid(row=2,column=0,padx=(10,10),pady=(10,0),sticky='n')
    budget_b.grid(row=3,column=0,padx=(10,10),pady=(10,0),sticky='n')
    savings_b.grid(row=4,column=0,padx=(10,10),pady=(10,0),sticky='n')
    tracking_b.grid(row=5,column=0,padx=(10,10),pady=(10,0),sticky='n')
    payments_b.grid(row=6,column=0,padx=(10,10),pady=(10,0),sticky='n')
    profile_b.grid(row=7,column=0,padx=(10,10),pady=(10,0),sticky='n')

    #inner frame that will change depending on the current section of the website
    inner_frame=ctk.CTkFrame(outer_frame,width=w-350,height=770, fg_color="#d7d7d7")
    inner_frame.grid(row=1,rowspan=7,column=1,sticky='nw',pady=20)
    inner_frame.pack_propagate(False)
    inner_frame.grid_propagate(False)
    home(root,top_text,inner_frame,True)

"""Function that creates the contents of the home page"""
def home(root,top_text,inner_frame,starting):
    delete_contents(inner_frame)
    top_text.configure(text="MyHome")
    if not starting:
        now = m.datetime.datetime.now().strftime("%H")
        if 0 <= int(now) <= 12:
            greeting=f"Good Morning {first[0].upper()}{first[1:]}"
        elif 12 <= int(now) <= 18:
            greeting=f"Good Afternoon {first[0].upper()}{first[1:]}"
        else:
            greeting=f"Good Evening {first[0].upper()}{first[1:]}"
    else:
        greeting=f"Welcome Back {first[0].upper()}{first[1:]}"
    greeting_label=m.ctk.CTkLabel(inner_frame,text=greeting,text_color='black',font=("Trebuchet MS",25,"bold"))
    greeting_label.grid(row=0,column=0,columnspan=2,padx=550)

    payment=m.pd.read_sql(f"SELECT Name, Date FROM payments WHERE id='{m.user_id}'",engine).to_numpy()
    p_frame=m.ctk.CTkFrame(inner_frame,width=550,height=300)
    p_frame.grid(row=1,column=0,pady=10,padx=(100,0))
    p_frame.pack_propagate(False)
    p_guide=m.ctk.CTkLabel(p_frame,text="Upcoming Payments:",font=("Trebuchet MS",30,"bold"))
    p_guide.pack(pady=(30,0))
    p_dict={}
    p_list=[]
    p_string=""
    for p in payment:
        p_dict[p[1]]=p[0]
    i=int(datetime.datetime.now().strftime("%d"))
    while len(p_list)<3 and len(p_list)<len(p_dict.keys()):
        try:
            p_list.append(p_dict[str(i)])
            p_string+=f"{p_dict[str(i)]} is due on the {i}"
            if i==1 or i==11 or i==21 or i==31:
                p_string+="st\n"
            elif i==2 or i==12 or i==22:
                p_string+="nd\n"
            elif i==3 or i==13 or i==23:
                p_string+="rd\n"
            else:
                p_string+="th\n"
        except KeyError:
            pass
        finally:
            if i<31:
                i+=1
            else:
                i=1
    p_text=m.ctk.CTkLabel(p_frame,text=f"{p_string}",font=("Trebuchet MS",30,"bold"))
    p_text.pack(pady=30)


    m_frame = m.ctk.CTkFrame(inner_frame, width=550, height=300)
    m_frame.grid(row=1, column=1,pady=10,padx=(0,100))
    m_frame.pack_propagate(False)
    motivational_messages = {
        1: "💰  Every dollar you save today\n     is a gift to your future self.",
        2: "📈  Small steps add up.\n     Keep going—you’re building\n     something meaningful.",
        3: "🎯  You're closer to your\n     financial goals than you\n     were yesterday.",
        4: "🌱  Consistency beats perfection.\n     Keep growing your wealth\n     one habit at a time.",
        5: "🚀  Great progress starts with\n     small actions.\n     You're on the right track.",
        6: "🏆  Nice work!\n     Your financial discipline\n     is paying off.",
        7: "🎉  Another milestone reached.\n     Celebrate the progress\n     you've made.",
        8: "📊  Your smart decisions are\n     creating long-term results.",
        9: "💪  You've stayed committed—\n     your future self will\n     thank you.",
        10: "⭐  Progress isn't always dramatic.\n     Today's win still counts.",
        11: "🐷  Every dollar saved is\n     another dollar working\n     for you.",
        12: "🌟  Your savings are growing—\n     keep the momentum alive.",
        13: "🔒  Financial security is built\n     one deposit at a time.",
        14: "💎  Small savings today can\n     become big opportunities\n     tomorrow.",
        15: "📈  Your future goals are\n     getting funded,\n     one contribution at a time.",
        16: "🌳  Wealth grows like a tree:\n     steadily, patiently,\n     and over time.",
        17: "📈  Time in the market can be\n     more powerful than timing\n     the market.",
        18: "🚀  Your investments are part\n     of a bigger journey toward\n     financial freedom.",
        19: "🔍  Stay focused on the long term—\n     today's choices shape\n     tomorrow's outcomes.",
        20: "💡  Smart investing isn't about\n     perfection;\n     it's about consistency.",
        21: "☕  Skip one impulse purchase,\n     fund one future goal.",
        22: "📱  Your money is making moves—\n     even when you're not.",
        23: "🔥  Momentum is building.\n     Keep the streak alive.",
        24: "🎯  Future You just gave\n     Present You a high five.",
        25: "💸  You're telling your money\n     where to go instead of\n     wondering where it went.",
        26: "🌅  Financial freedom isn't\n     a dream—it's a series\n     of decisions.",
        27: "🏔️  Big goals are reached\n     through steady progress.",
        28: "🔑  Every smart financial choice\n     unlocks more possibilities.",
        29: "🌍  Wealth creates options.\n     You're building yours.",
        30: "⭐  The habits you build today\n     become the freedom you\n     enjoy tomorrow.",
        31: "✨  One smart decision today\n     can change your future.",
        32: "🎯  Goal progress updated—\n     keep it moving!",
        33: "💪  You're building wealth,\n     one step at a time.",
        34: "📈  Consistency is your\n     superpower.",
        35: "🚀  Keep going.\n     Financial freedom\n     is built daily."
    }
    message = motivational_messages[random.randint(1, len(motivational_messages))]
    m_label=m.ctk.CTkLabel(m_frame,text=message,font=("Trebuchet MS",35,"bold"))
    m_label.pack(pady=50)


    accounts = m.pd.read_sql(f"SELECT Name, Total FROM tracking_new WHERE id='{m.user_id}'", engine).to_numpy()
    a_frame=m.ctk.CTkFrame(inner_frame,width=550,height=300)
    a_frame.grid(row=2,column=0,pady=(0,20),padx=(100,0))
    a_frame.grid_propagate(False)
    a_text = m.ctk.CTkLabel(a_frame,font=("Trebuchet MS", 35, "bold"))
    a_button = m.ctk.CTkButton(a_frame,font=("Trebuchet MS", 30, "bold"),width=200,height=50)
    if accounts.size==0:
        a_text.configure(text="Seems like you haven't created any accounts yet\nClick below to go create one")
        a_text.grid(row=0,column=0)
        a_button.configure(text="create",command=lambda:tracking(top_text,inner_frame))
        a_button.grid(row=1,column=0)
    else:
        a_guide=m.ctk.CTkLabel(a_frame,text="Account Totals:",font=("Trebuchet MS", 30, "bold"))
        a_guide.grid(row=0,column=0,pady=(20,10),padx=150,columnspan=2)
        a_text.configure(text=f"{accounts[(accounts.size//2)-1][0]}:")
        a_text.grid(row=1,column=0,pady=(30,20),padx=(90,10))
        a_num=m.ctk.CTkLabel(a_frame,text=f"{accounts[(accounts.size//2)-1][1]}",font=("Trebuchet MS",35,"bold"))
        a_num.grid(row=1,column=1,padx=(0,100),pady=(30,20))
        a_button.configure(text=f"Update {accounts[(accounts.size//2)-1][0]}",command=lambda:tracking_table(top_text,inner_frame,accounts[(accounts.size//2)-1][0]))
        a_button.grid(row=2,column=0,columnspan=2,padx=100)


    goals = m.pd.read_sql(f"SELECT Name, Total, Current FROM savings_goals WHERE id='{m.user_id}' LIMIT 2",
                          engine).to_numpy()
    s_frame = m.ctk.CTkFrame(inner_frame, width=550, height=300)
    s_frame.grid(row=2, column=1,pady=(0,20),padx=(0,100))
    s_frame.pack_propagate(False)
    s_guide=m.ctk.CTkLabel(s_frame,font=("Trebuchet MS", 30, "bold"),text="Saving Goals:")
    s_guide.pack(pady=(20,10))
    s_button = m.ctk.CTkButton(s_frame, font=("Trebuchet MS", 30, "bold"), width=150, height=50)
    s1_text = m.ctk.CTkLabel(s_frame, font=("Trebuchet MS", 30, "bold"))
    s2_text = m.ctk.CTkLabel(s_frame, font=("Trebuchet MS", 30, "bold"))
    if goals.size == 0:
        s1_text.configure(text="Seems like you haven't created any savings goals")
        s1_text.pack()
        s_button.configure(text="Go to Savings", command=lambda: savings(top_text, inner_frame, root))
        s_button.pack()
    else:
        s1_text.configure(text=f"{goals[0][0]}\n{goals[0][2]} out of {goals[0][1]} Saved!")
        s1_text.pack()
        s1_bar = m.ctk.CTkProgressBar(s_frame, height=20)
        s1_bar.set(goals[0][2] / goals[0][1])
        s1_bar.pack()
        if goals.size // 3 > 2:
            s2_text.configure(text=f"{goals[1]}")
            s2_text.pack()
            s2_bar = m.ctk.CTkProgressBar(s_frame, height=20)
            s2_bar.set(goals[1][2] / goals[1][1])

    logout_button = m.ctk.CTkButton(inner_frame,text="Logout",font=("Trebuchet MS",25),command=lambda: logout(root))
    logout_button.grid(row=3,column=0,columnspan=2)




#temp stuff to skip login process for developmental purposes
# r= ctk.CTk()
# r.bind("<Escape>", lambda e: r.destroy())
# create_main(r)
# r.after(1,r.state,'zoomed')
# r.mainloop()