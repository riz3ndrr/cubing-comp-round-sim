import customtkinter
from player import Player, UserPlayer, GennedPlayer
from pprint import pprint
from cubescrambler import (
    scrambler222,
    scrambler333,
    scrambler444,
    scrambler555,
    scrambler666,
    scrambler777,
    pyraminxScrambler,
    megaminxScrambler,
    squareOneScrambler,
    skewbScrambler,
    clockScrambler
)

# Tuple of the form (scramble function, font size)
EVENT_INFO = {
    "2x2x2 Cube": (scrambler222.get_WCA_scramble, 25),
    "3x3x3 Cube": (scrambler333.get_WCA_scramble, 25),
    "4x4x4 Cube": (scrambler444.get_WCA_scramble, 20),
    "5x5x5 Cube": (scrambler555.get_WCA_scramble, 20),
    "6x6x6 Cube": (scrambler666.get_WCA_scramble, 20),
    "7x7x7 Cube": (scrambler777.get_WCA_scramble, 20),
    "3x3x3 Blindfolded": (scrambler333.get_WCA_scramble, 25),
    "3x3x3 Fewest Moves": (scrambler333.get_WCA_scramble, 25),
    "3x3x3 One-Handed": (scrambler333.get_WCA_scramble, 25),
    "3x3x3 Multi-Blind": (scrambler333.get_3BLD_scramble, 25),
    "Pyraminx": (pyraminxScrambler.get_WCA_scramble, 25),
    "Megaminx": (megaminxScrambler.get_WCA_scramble, 20),
    "Skewb": (skewbScrambler.get_WCA_scramble, 25),
    "Square-1": (squareOneScrambler.get_WCA_scramble, 25),
    "Clock": (clockScrambler.get_WCA_scramble, 25),
    "4x4x4 Blindfolded": (scrambler444.get_WCA_scramble, 20),
    "5x5x5 Blindfolded": (scrambler555.get_WCA_scramble, 20)
}

DNF = 999

class PlayerGameRow():
    def __init__(self, root, x, y, player):
        self.player = player
        self.y = y
        self.frame = root

        NAME_DISPLAY_LENGTH = 16
        display_name = player.name
        if len(display_name) > NAME_DISPLAY_LENGTH:
            display_name = display_name[:NAME_DISPLAY_LENGTH - 3] + "..."
        elif len(display_name) < NAME_DISPLAY_LENGTH:
            display_name += " " * (NAME_DISPLAY_LENGTH - len(display_name))



        self.player_name_label = customtkinter.CTkLabel(root, text = display_name, width = 150, font = ("TkDefaultFont", 20))
        self.player_name_label.grid(row = self.y, column = 1, sticky = "ew", padx = 10, pady = 10)
        
        self.player_time_label_0 = customtkinter.CTkLabel(root, text = "#####", font = ("TkDefaultFont", 20))
        self.player_time_label_1 = customtkinter.CTkLabel(root, text = "#####", font = ("TkDefaultFont", 20))
        self.player_time_label_2 = customtkinter.CTkLabel(root, text = "#####", font = ("TkDefaultFont", 20))
        self.player_time_label_3 = customtkinter.CTkLabel(root, text = "#####", font = ("TkDefaultFont", 20))
        self.player_time_label_4 = customtkinter.CTkLabel(root, text = "#####", font = ("TkDefaultFont", 20))

        self.player_avg_label = customtkinter.CTkLabel(root, text = "N/A", font = ("TkDefaultFont", 20))

        self.player_time_labels = [self.player_time_label_0,
                                   self.player_time_label_1,
                                   self.player_time_label_2,
                                   self.player_time_label_3,
                                   self.player_time_label_4]
        for col_num, time_label in enumerate(self.player_time_labels):
            time_label.grid(row = self.y, column = col_num + 2, sticky = "", padx = 10)

        #self.frame.grid_columnconfigure(0, weight = 0)

    def repositionLabels(self, new_row_num, solve_num):
        self.player_name_label.grid(row = new_row_num, column = 1, sticky = "", padx = 10)
        for col_num, time_label in enumerate(self.player_time_labels):
            time_label.grid(row = new_row_num, column = col_num + 2, sticky = "", padx = 10)
        if solve_num >= 3:
            self.player_avg_label.grid(row = new_row_num, column = 7, sticky = "", padx = 10)
    
    def resetLabels(self):
        self.player_avg_label.grid_forget()
        for time_label in self.player_time_labels:
            time_label.configure(text = "#####")
    
    def displayNextResult(self, solve_num):
        label_to_configure = self.player_time_labels[solve_num]
    
        time_to_display = self.player.times[solve_num]
        if time_to_display == DNF:
            label_to_configure.configure(text = "DNF")
        else:
            label_to_configure.configure(text = f"{time_to_display:.2f}")

        if (solve_num == 3):
            #self.player_avg_label.grid(row = self.y, column = 7, sticky = "", padx = 10)
            wpa = "DNF" if self.player.wpa == DNF else f"{self.player.wpa:.2f}"
            self.player_avg_label.configure(text = f"{self.player.bpa:.2f}/{wpa}", text_color = "grey")

        elif (solve_num == 4):
            avg = "DNF" if self.player.avg == DNF else f"{self.player.avg:.2f}"
            self.player_avg_label.configure(text = avg, text_color = "black")




class GameFrame():
    def __init__(self, root, cpu_players, switchFrameFunc, event):
        self.frame = customtkinter.CTkFrame(master = root, width = 1000, height = 1000, fg_color = "white")
        #self.label = customtkinter.CTkLabel(self.frame, text = "WADSHASDHSAJD")
        #self.label.place(relx = 0.5, rely = 0.1, anchor = customtkinter.CENTER)
        self.solve_num = 0
        self.scramble_func = EVENT_INFO[event][0]

        ## PLAYER CONTAINER
        self.players_container = customtkinter.CTkScrollableFrame(master = self.frame, width = 850, height = 700, fg_color = "#f0f0f0")
        self.players_container.place(relx = 0.5, rely = 0.65, anchor = customtkinter.CENTER)

        ## DISPLAY PLAYER STATS 
        
        self.players = {}
        
        self.player_name_header = customtkinter.CTkLabel(master = self.players_container, width = 150, text = "Player:", font = ("TkDefaultFont", 20))
        self.player_name_header.grid(row = 0, column = 1, sticky = "", padx = 10)

        self.player_rank_header = customtkinter.CTkLabel(master = self.players_container, text = "Rank:", font = ("TkDefaultFont", 20))
        self.player_rank_header.grid(row = 0, column = 0, sticky = "", padx = 10)
        
        ## SOLVE COLUMNS
        for col_num in range(1, 6):
            self.time_label = customtkinter.CTkLabel(master = self.players_container, text = f"Solve {col_num}:", font = ("TkDefaultFont", 20))
            self.time_label.grid(row = 0, column = col_num + 1, sticky = "", padx = 10)

        self.avg_header = customtkinter.CTkLabel(master = self.players_container, text = "Average:", font = ("TkDefaultFont", 20))
        self.avg_header.grid(row = 0, column = 7, sticky = "", padx = 10)

         
        for row_num, player in enumerate(cpu_players):
            pos_label = customtkinter.CTkLabel(master = self.players_container, text = f"{row_num + 1}", font = ("TkDefaultFont", 20))
            pos_label.grid(row = row_num + 1, column = 0)
            self.players[player] = PlayerGameRow(self.players_container, row_num + 1, row_num + 1, player)

        ## GENERATE USER ROW
        pos_label = customtkinter.CTkLabel(master = self.players_container, text = f"{len(cpu_players) + 1}", font = ("TkDefaultFont", 20))
        pos_label.grid(row = len(cpu_players) + 1, column = 0)

        self.user = UserPlayer("You")
        self.players[self.user] = PlayerGameRow(self.players_container, len(cpu_players) + 1, len(cpu_players) + 1 , self.user)

        ## DISPLAY SCRAMBLE 
        self.scramble_list = []
        scramble_font_size = EVENT_INFO[event][1]
        self.scramble_label = customtkinter.CTkLabel(master = self.frame, text = "", font = ("TkDefaultFont", scramble_font_size),
                                                     wraplength = 800, justify = customtkinter.CENTER, width = 700)
        self.generateScramble()
        self.scramble_label.place(relx = 0.5, rely = 0.1, anchor = customtkinter.CENTER)


        # GET USER INPUT
        
        
        user_input_y = 0.2
        self.time_input_label = customtkinter.CTkEntry(master = self.frame, placeholder_text = "E.G., 6.53", width = 400)
        self.time_input_label.place(relx = 0.4, rely = user_input_y, anchor = customtkinter.CENTER)

        self.enter_time_button = customtkinter.CTkButton(master = self.frame, text = "Enter Time", command = self.processUserTimeInput, height = 30)
        self.enter_time_button.place(relx = 0.7, rely = user_input_y, anchor = customtkinter.CENTER)

        self.rematch_button = customtkinter.CTkButton(master = self.frame, text = "Rematch (R)", command = self.resetRound, width = 200, height = 40)
        self.rematch_button.place(relx = 0.35, rely = user_input_y + 0.05, anchor = customtkinter.CENTER)

            ## SWITCH FRAMES 
        self.switchFrameFunc = switchFrameFunc
        self.switch_frame_button = customtkinter.CTkButton(master = self.frame, text = "Change Competitors (C)", command = self.switchFrameFunc, width = 200, 
                                                           height = 40)
        self.switch_frame_button.place(relx = 0.6, rely = user_input_y + 0.05, anchor = customtkinter.CENTER)

        # USER FEEDBACK 
        self.error_label = customtkinter.CTkLabel(master = self.frame, text = "Please correctly input a time", text_color = "red")
        #root.bind('<Key>', self.enterUserTime)


    def resetRound(self):
        for player, player_row in self.players.items():
            player_row.resetLabels()
            if (isinstance(player, UserPlayer)):
                player.times = []
            else:
                player.avg, player.times = player.generateNewResults()
                player.calcBPAandWPA()
        self.generateScramble()
        self.solve_num = 0

    def processUserKeyInput(self, key):
        ENTER_KEYSYM = 36
        R = 27
        C = 54
        print(key)
        if key.keycode == ENTER_KEYSYM:
            self.processUserTimeInput()
        elif key.keycode == R:
            self.resetRound()
            self.time_input_label.delete(0, len(self.time_input_label.get()))

        elif key.keycode == C:
            self.switchFrameFunc()
        
    
    def processUserTimeInput(self):
        try:
            time = self.time_input_label.get()

            if time == 'DNF':
                self.user.addTime(DNF)
            else:
                time = float(self.time_input_label.get())
                self.user.addTime(time)

            if self.solve_num == 4:
                self.user.generateAvg()
            elif self.solve_num == 3:
                self.user.calcBPAandWPA()

            self.showNextTime()
            self.error_label.place_forget()
            self.time_input_label.delete(0, len(str(time)))
        except ValueError:
            self.error_label.place(relx = 0.5, rely = 0.1, anchor = customtkinter.CENTER)


             
            
    def generateScramble(self):
        # TODO: DISPLAY SOME EVENTS CORRECTLY
        self.scramble_label.configure(text="Generating scrambles...")
        self.scramble_list = []
        def showFirstScramble():
            first_scramble = self.scramble_func()
            self.scramble_label.configure(text = first_scramble)
            self.scramble_list.append(first_scramble)

            def generateRest():
                for _ in range(4):
                    self.scramble_list.append(self.scramble_func())
                pprint(self.scramble_list)

            self.scramble_label.after(100, generateRest)

        self.scramble_label.after(500, showFirstScramble)
        pprint(self.scramble_list)
        
    def showNextTime(self):
              
        self.rerankPlayers()
        for player_game_row in self.players.values():
            player_game_row.displayNextResult(self.solve_num)
        self.solve_num += 1

        if self.solve_num <= 4:
            self.scramble_label.configure(text = self.scramble_list[self.solve_num])

    def rerankPlayers(self):
        #pprint(self.players.items())
        if self.solve_num < 4:
            self.players = dict(sorted(self.players.items(), key = lambda player_info : min(player_info[0].times[:(self.solve_num + 1)])))
        else:
            self.players = dict(sorted(self.players.items(), key = lambda player_info : player_info[0].avg))

        #pprint(self.players.items())
        for new_row_num, player_row in enumerate(self.players.values()):
            player_row.repositionLabels(new_row_num + 1, self.solve_num)

        


