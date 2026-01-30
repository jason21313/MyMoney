from sections_files.profile_functions import *
from sections_files.payments_functions import *
from sections_files.misc_functions import *

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
    top_text=ctk.CTkLabel(top_frame,text=f"Welcome Back {first[0].upper()}{first[1:]}",text_color='black',font=("Trebuchet MS",25,"bold"))
    top_text.pack(pady=10,anchor='n')
    top_frame.pack_propagate(False)
    img=Image.open("transparent.png")
    image= ctk.CTkImage(light_image=img,dark_image=img,size=(150,150))
    image_label=ctk.CTkLabel(outer_frame,image=image,text="")
    image_label.grid(row=1,column=0,padx=10,pady=(15,0),sticky='n')

    #buttons for each section of the website
    home_b=ctk.CTkButton(outer_frame,text='Home',height=75,fg_color="#6C3BAA",hover_color="#7851A9",
                         font=("Trebuchet MS",25,"bold"),text_color='#d7d7d7', command=lambda: home(top_text,inner_frame))
    budget_b = ctk.CTkButton(outer_frame, text='Budget',height=75,fg_color="#6C3BAA",hover_color="#7851A9",
                             font=("Trebuchet MS",25,"bold"),text_color='#d7d7d7',command=lambda: budget(top_text,inner_frame))
    savings_b = ctk.CTkButton(outer_frame, text='Savings',height=75,fg_color="#6C3BAA",hover_color="#7851A9",
                              font=("Trebuchet MS",25,"bold"),text_color='#d7d7d7',command=lambda: savings(top_text,inner_frame))
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

#temp stuff to skip login process for developmental purposes
# r= ctk.CTk()
# r.bind("<Escape>", lambda e: r.destroy())
# create_main(r)
# r.after(1,r.state,'zoomed')
# r.mainloop()