import customtkinter

class popupFrame():
    def __init__(self, root, msg, text_color, w, h):
        self.container = customtkinter.CTkFrame(master = root,fg_color = "white", width = w, height = h)
        self.container.pack_propagate(0)

        self.x_button = customtkinter.CTkButton(master = self.container, width = 40, height = 40, text = "X",
                                                font = ("TkDefaultFont", 20),
                                                command = self.forget)
        self.x_button.place(relx = 0.9, rely = 0.1)

        label = customtkinter.CTkLabel(self.container, text = msg, font = ("TkDefaultFont", 20), width = w, fg_color = "transparent")
        label.place(relx = 0, rely = 0.3)
    def place(self):
        self.container.place(relx = 0.25, rely = 0.5)
    def forget(self):
        self.container.place_forget()
