import customtkinter as ctk
app = ctk.CTk()

def hello():
    t.configure(text="no")


ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")
app.title("Custom Tkinter Learning")
h=app.winfo_screenheight()
w=app.winfo_screenwidth()
app.geometry(f"{h}x{w}")

t=ctk.CTkLabel(app,text="Hello World")
t.pack()
b=ctk.CTkButton(app,text="Click Me",command=hello, hover_color = "green")
b.pack()
app.mainloop()
b.pack()
app.mainloop()



if __name__ == '__main__':
    pass
