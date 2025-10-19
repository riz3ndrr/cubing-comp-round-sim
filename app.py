import customtkinter

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

app = customtkinter.CTk()  # create CTk window like you do with the Tk window
app.geometry("400x240")

def button_function():
    print(wca_id_entry.get())
    wca_id_entry.delete(0, len(wca_id_entry.get()))

# Use CTkButton instead of tkinter Button
input_wca_id_button = customtkinter.CTkButton(master=app, text="CTkButton", command=button_function)
input_wca_id_button.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)

app_label = customtkinter.CTkLabel(app, 
                                   text = "WCA Competition Round Simulator",
                                   fg_color = "transparent",
                                   font = ("TkDefaultFont", 35))
app_label.place(relx = 0.5, rely = 0.1, anchor=customtkinter.CENTER)


subtitle1 = customtkinter.CTkLabel(app,
                                   text = "Enter your opponent(s)' WCA ID",
                                   fg_color = "transparent",
                                   font = ("TkDefaultFont", 20))
subtitle1.place(relx = 0.5, rely = 0.15, anchor = customtkinter.CENTER)


wca_id_entry = customtkinter.CTkEntry(app, placeholder_text="WCA IDs go here")
wca_id_entry.place(relx = 0.5, rely = 0.2, anchor = customtkinter.CENTER)


app.mainloop()
