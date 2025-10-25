import customtkinter

from player import Player, GennedPlayer


EVENT_CODES = {
    "2x2x2 Cube": "222",
    "3x3x3 Cube": "333",
    "3x3x3 Blindfolded": "333bf",
    "3x3x3 Fewest Moves": "333fm",
    "3x3x3 One-Handed": "333oh",
    "4x4x4 Cube": "444",
    "4x4x4 Blindfolded": "444bf",
    "5x5x5 Cube": "555",
    "5x5x5 Blindfolded": "555bf",
    "6x6x6 Cube": "666",
    "7x7x7 Cube": "777",
    "Clock": "clock",
    "Megaminx": "minx",
    "Pyraminx": "pyram",
    "Skewb": "skewb",
    "Square-1": "sq1",
    "3x3x3 Multi-Blind": "333mbf"
}


class PlayerRowLabel():
    ## TODO MAKE THIS EFFFICIENT
    def __init__(self, root, x, y, remove_player_func, player):
        self.container = customtkinter.CTkFrame(root, width=450, height=200, fg_color = "#ffffff", border_color = "grey", border_width = 1)
        self.container.grid(row = y, column = x, sticky = "", padx = 5, pady=10)
        #self.container.grid_propagate(False)
        self.player = player
        self.player_wca_label = customtkinter.CTkLabel(self.container,
                                                    text = player.wca_id,
                                                    text_color = "grey",
                                                    font = ("TkDefaultFont", 17))
        NAME_DISPLAY_LENGTH = 16
        display_name = player.name
        if len(display_name) > NAME_DISPLAY_LENGTH:
            display_name = display_name[:NAME_DISPLAY_LENGTH - 3] + "..."
        elif len(display_name) < NAME_DISPLAY_LENGTH:
            display_name += " " * (NAME_DISPLAY_LENGTH - len(display_name))

        self.player_name_label = customtkinter.CTkLabel(self.container,
                                                        text = display_name,

                                                        font = ("Courier New", 20))
        self.player_name_label.grid(row = 0, column = 0, sticky = 'W', pady = 2, padx = 4,)
        self.player_wca_label.grid(row = 5, column = 2, sticky = 'W', pady = 2, padx = 2)

        
        ## PR AVG LABELS
        self.pr_avg_header = customtkinter.CTkLabel(self.container,
                                                    text = "PR Average:",
                                                    text_color = "grey",
                                                    font = ("TkDefaultFont", 17))

        self.pr_avg_label = customtkinter.CTkLabel(self.container,
                                                    text = player.pr_avg,
                                                    text_color = "black",
                                                    font = ("TkDefaultFont", 19))

        self.pr_avg_header.grid(row = 1, column = 0, sticky = '', pady = 2, padx = 4)
        self.pr_avg_label.grid(row = 2, column = 0, sticky = '', pady = 2, padx = 4)

        ## PR SINGLE LABELS
        self.pr_sin_header = customtkinter.CTkLabel(self.container,
                                                    text = "PR Single:",
                                                    text_color = "grey",
                                                    font = ("TkDefaultFont", 17))

        self.pr_sin_label = customtkinter.CTkLabel(self.container,
                                                    text = player.pr_sin,
                                                    text_color = "black",
                                                    font = ("TkDefaultFont", 19))
            
        self.pr_sin_header.grid(row = 3, column = 0, sticky = '', pady = 2, padx = 4)
        self.pr_sin_label.grid(row = 4, column = 0, sticky = '', pady = 2, padx = 4)


        ## WORLD RANK LABELS
        self.wr_header = customtkinter.CTkLabel(self.container,
                                                    text = "World Ranking:",
                                                    text_color = "grey",
                                                    font = ("TkDefaultFont", 17),
                                                    width = 70)

        self.wr_label = customtkinter.CTkLabel(self.container,
                                                    text = player.rank,
                                                    text_color = "black",
                                                    font = ("TkDefaultFont", 19),
                                                    width = 70)
     
        self.wr_header.grid(row = 1, column = 1, sticky = 'W', pady = 2)
        self.wr_label.grid(row = 2, column = 1, sticky = 'W', pady = 2)
   
        ## COUNTRY LABELS
        self.country_header = customtkinter.CTkLabel(self.container,
                                                    text = "Representing:    ",
                                                    text_color = "grey",
                                                    font = ("TkDefaultFont", 17),
                                                    width = 70)

        self.country_label = customtkinter.CTkLabel(self.container,
                                                    text = player.country,
                                                    text_color = "black",
                                                    font = ("TkDefaultFont", 19),
                                                    width = 100)
     
        self.country_header.grid(row = 3, column = 1, sticky = 'W', pady = 2, padx = 0)
        self.country_label.grid(row = 4, column = 1, sticky = 'W', pady = 2, padx = 0)
   
        ## RECENT RESULTS LABELS
        self.recent_results_header = customtkinter.CTkLabel(self.container,
                                                            text = "Recent Mo50:",
                                                    text_color = "grey",
                                                    font = ("TkDefaultFont", 17),
                                                    width = 70)

        self.recent_results_label = customtkinter.CTkLabel(self.container,
                                                    text = f"{player.mo50_recent:.2f}",
                                                    text_color = "black",
                                                    font = ("TkDefaultFont", 19),
                                                    width = 100)
     
        self.recent_results_header.grid(row = 1, column = 2, sticky = 'W', pady = 2, padx = 2)
        self.recent_results_label.grid(row = 2, column = 2, sticky = 'W', pady = 2, padx = 2)

        ## X BUTTON
        self.x_button = customtkinter.CTkButton(master = self.container, text = "X", text_color = "black", bg_color = "transparent", 
                                                hover_color = "grey", command = self.remove_row, width = 20)
        self.x_button.grid(row = 0, column = 2, sticky = 'E', pady = 5, padx = 5)
        self.remove_player_callback_func = remove_player_func
        
    def remove_row(self):
        self.remove_player_callback_func(self.player)
        for widget in self.container.winfo_children():
            widget.destroy()
        self.container.destroy()

    def change_pos(self, new_x, new_y):
        self.container.grid(row = new_y, column = new_x, padx = 5, pady=10) 


class StartFrame():
    def __init__(self, root, swtich_frame_func):
        self.frame = customtkinter.CTkFrame(master = root, width = 1000, height = 1000, fg_color="white")
        #self.frame.pack(expand = True)
        self.app_label = customtkinter.CTkLabel(self.frame, 
                                        text = "WCA Competition Round Simulator",
                                        fg_color = "transparent",
                                        font = ("TkDefaultFont", 35))
        self.app_label.place(relx = 0.5, rely = 0.05, anchor=customtkinter.CENTER)

        # ADD COMPETITOR
        self.subtitle1 = customtkinter.CTkLabel(self.frame,
                                        text = "Add Competitor",
                                        fg_color = "transparent",
                                        font = ("TkDefaultFont", 25))
        self.subtitle1.place(relx = 0.2, rely = 0.185, anchor = customtkinter.CENTER)


        self.wca_id_entry = customtkinter.CTkEntry(self.frame, width = 225, placeholder_text="Enter your opponent(s)' WCA ID")
        self.wca_id_entry.place(relx = 0.25, rely = 0.225, anchor = customtkinter.CENTER)


        self.input_wca_id_button = customtkinter.CTkButton(master=self.frame, text="Enter", command=self.input_wca_id_button_function)
        self.input_wca_id_button.place(relx = 0.45, rely = 0.225, anchor=customtkinter.CENTER)

        self.wca_id_entry_feedback_label = customtkinter.CTkLabel(self.frame, text = "WCA ID invalid",
                                                            text_color = "red",
                                                            font = ("TkDefaultFont", 20))
        self.wca_id_entry_feedback_label.place_forget()

        
        ## CONFIGURE EVENT
        self.event_label = customtkinter.CTkLabel(self.frame, 
                                        text = "Event: ",
                                        fg_color = "transparent",
                                        font = ("TkDefaultFont", 25))
        self.event_label.place(relx = 0.6, rely = 0.185, anchor=customtkinter.CENTER)

        self.event_dropdown = customtkinter.CTkOptionMenu(self.frame, values=list(EVENT_CODES.keys()),
                                         command=self.event_dropdown_callback,
                                         )
        
        self.event_dropdown.place(relx=0.55, rely = 0.21)
        self.event = list(EVENT_CODES.keys())[0]

        
        ## FRAME / COMPETITORS CONTAINER ##
        self.players_frame = customtkinter.CTkScrollableFrame(self.frame, width=900, height=600)
        self.players_frame.grid_columnconfigure(0, weight = 0)
        self.players_frame.place(relx=0.5, rely=0.60, anchor = customtkinter.CENTER)
        self.players_frame_header = customtkinter.CTkLabel(self.frame, text = "Competitors", fg_color = "transparent", font = ("TkDefaultFont", 30))
        self.players_frame_header.place(relx = 0.1, rely = 0.25)

        self.players = {}
        self.players_row_offsety = 0
        self.players_col_num = 0


        self.swtich_frame_func = swtich_frame_func
        self.start_button = customtkinter.CTkButton(master = self.frame, text = "Start (+)", command = self.swtich_frame_func,
                                                    width = 300, height = 50, font = ("TkDefaultFont", 20))
        self.start_button.place(relx = 0.5, rely = 0.95, anchor = customtkinter.CENTER)

        #root.bind('<Key>', self.recvUserKeyInput)
    def clearEntryText(self):
        self.wca_id_entry.delete(0, len(self.wca_id_entry.get()))

    def startRound(self):
        print("STARTED")

    def event_dropdown_callback(self, choice):
        if self.event != choice:
            self.event = choice
            self.clear_players()

    def clear_players(self):
        for player, player_row in self.players.items():
            for widget in player_row.container.winfo_children():
                widget.destroy()
            player_row.container.destroy() 
        self.players.clear()
        self.players_col_num = 0 
        self.players_row_offsety = 0

    def remove_player(self, player):
        if player in self.players:
            self.players.pop(player)  
        self.shift_player_pos()

    def shift_player_pos(self):
        x = 0
        y = 0 

        for row in self.players.values():
            row.change_pos(x, y)
            x = (x + 1) % 2 
            if (x == 0):
                y += 1
        
        self.players_col_num = x
        self.players_row_offsety = y 
    
    def playerAlreadyExists(self, wca_id):
        for opp in self.players.keys():
            if opp.wca_id == wca_id:
                return True
        return False
    
    def processUserKeyInput(self, key):
        ENTER_KEYCODE = 36
        PLUS_KEYCODE = 21
        if key.keycode == ENTER_KEYCODE:
            self.input_wca_id_button_function()
        elif key.keycode == PLUS_KEYCODE:
            self.swtich_frame_func()


    def input_wca_id_button_function(self):
        inputted_wca_id = self.wca_id_entry.get()
        self.wca_id_entry_feedback_label.place(relx = 0.8, rely = 0.225, anchor = customtkinter.CENTER)

        if self.playerAlreadyExists(inputted_wca_id):
            self.wca_id_entry_feedback_label.configure(text = "Player Already Exists", text_color = "red")
            return    

        new_player = GennedPlayer(inputted_wca_id, EVENT_CODES[self.event_dropdown.get()])
        if new_player.validPlayer() is False:
            self.wca_id_entry_feedback_label.configure(text = "WCA ID invalid", text_color = "red")
            return

        self.wca_id_entry_feedback_label.configure(text = "Input successful", text_color = "green")
        self.wca_id_entry.delete(0, len(inputted_wca_id))
        
        new_row = PlayerRowLabel(self.players_frame,
                                 self.players_col_num,
                                 self.players_row_offsety,
                                 self.remove_player,
                                 new_player)

        self.players[new_player] = new_row
        self.players_col_num = (self.players_col_num + 1) % 2
        if self.players_col_num == 0:
            self.players_row_offsety += 1

        print(len(self.players))
        print(new_player.times)
        print(new_player.avg)


