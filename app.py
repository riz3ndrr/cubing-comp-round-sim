import customtkinter
from numpy import random

from pprint import pprint

from player import Player, userPlayer, gennedPlayer

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

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

def clear():
    print(chr(27) + "[2J")

DNF = 999


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
EVENT_SCRAMBLES = {
    "2x2x2 Cube": scrambler222.get_WCA_scramble,
    "3x3x3 Cube": scrambler333.get_WCA_scramble,
    "4x4x4 Cube": scrambler444.get_WCA_scramble,
    "5x5x5 Cube": scrambler555.get_WCA_scramble,
    "6x6x6 Cube": scrambler666.get_WCA_scramble,
    "7x7x7 Cube": scrambler777.get_WCA_scramble,
    "3x3x3 Blindfolded": scrambler333.get_WCA_scramble,
    "3x3x3 Fewest Moves": scrambler333.get_WCA_scramble,
    "3x3x3 One-Handed": scrambler333.get_WCA_scramble,
    "3x3x3 Multi-Blind": scrambler333.get_3BLD_scramble,
    "Pyraminx": pyraminxScrambler.get_WCA_scramble,
    "Megaminx": megaminxScrambler.get_WCA_scramble,
    "Skewb": skewbScrambler.get_WCA_scramble,
    "Square-1": squareOneScrambler.get_WCA_scramble,
    "Clock": clockScrambler.get_WCA_scramble,
    "4x4x4 Blindfolded": scrambler444.get_WCA_scramble,
    "5x5x5 Blindfolded": scrambler555.get_WCA_scramble
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



        self.player_name_label = customtkinter.CTkLabel(root, text = display_name, font = ("TkDefaultFont", 20))
        self.player_name_label.grid(row = self.y, column = 1, sticky = "", padx = 10, pady = 10)
        
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
    def __init__(self, root, cpu_players, switchFrameFunc, scramble_func):
        self.frame = customtkinter.CTkFrame(master = root, width = 1000, height = 1000, fg_color = "white")
        self.label = customtkinter.CTkLabel(self.frame, text = "WADSHASDHSAJD")
        self.label.place(relx = 0.5, rely = 0.1, anchor = customtkinter.CENTER)
        self.solve_num = 0
        self.scramble_func = scramble_func

        ## PLAYER CONTAINER
        self.players_container = customtkinter.CTkScrollableFrame(master = self.frame, width = 800, height = 600, fg_color = "#f0f0f0")
        self.players_container.place(relx = 0.5, rely = 0.7, anchor = customtkinter.CENTER)

        ## DISPLAY PLAYER STATS 
        
        self.players = {}
        
        self.player_name_header = customtkinter.CTkLabel(master = self.players_container, text = "Player:", font = ("TkDefaultFont", 20))
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

        self.user = userPlayer("Player")
        self.players[self.user] = PlayerGameRow(self.players_container, len(cpu_players) + 1, len(cpu_players) + 1 , self.user)

        ## DISPLAY SCRAMBLE 
        self.scramble_list = []
        self.scramble_label = customtkinter.CTkLabel(master = self.frame, text = "", font = ("TkDefaultFont", 30))
        self.generateScramble()
        self.scramble_label.place(relx = 0.5, rely = 0.2, anchor = customtkinter.CENTER)


        # GET USER INPUT
        
        
        user_input_y = 0.3
        self.time_input_label = customtkinter.CTkEntry(master = self.frame, placeholder_text = "E.G., 6.53", width = 400)
        self.time_input_label.place(relx = 0.4, rely = user_input_y, anchor = customtkinter.CENTER)

        self.enter_time_button = customtkinter.CTkButton(master = self.frame, text = "Enter Time", command = self.processUserTimeInput, height = 30)
        self.enter_time_button.place(relx = 0.7, rely = user_input_y, anchor = customtkinter.CENTER)

        self.rematch_button = customtkinter.CTkButton(master = self.frame, text = "Rematch", command = self.resetRound, height = 30)
        self.rematch_button.place(relx = 0.4, rely = user_input_y + 0.05, anchor = customtkinter.CENTER)

            ## SWITCH FRAMES 
        self.switch_frame_button = customtkinter.CTkButton(master = self.frame, text = "Change Competitors", command = switchFrameFunc, height = 30)
        self.switch_frame_button.place(relx = 0.6, rely = user_input_y + 0.05, anchor = customtkinter.CENTER)

        # USER FEEDBACK 
        self.error_label = customtkinter.CTkLabel(master = self.frame, text = "Please correctly input a time", text_color = "red")
        #root.bind('<Key>', self.enterUserTime)




    def tester(self):
        pprint(self.scramble_list)

    def resetRound(self):
        for player, player_row in self.players.items():
            player_row.resetLabels()
            if (isinstance(player, userPlayer)):
                player.times = []
            else:
                player.avg, player.times = player.generateNewResults()
                player.calcBPAandWPA()
        self.generateScramble()
        self.solve_num = 0

    def processUserKeyInput(self, key):
        ENTER_KEY = 36 
        if key.keycode == ENTER_KEY:
            self.processUserTimeInput()
    
    def processUserTimeInput(self):
        print("WE HERE")
        try:
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
        self.scramble_label.configure(text="Generating scramble...")
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

        



class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1000x1000")

        self.startFrame = StartFrame(self, self.switchFrame)
        self.gameFrame = None 

        self.players = None
        self.startFrame.frame.pack(expand = True)
        self.currFrame = self.startFrame
        self.frames = [self.gameFrame, self.startFrame]
        self.bind('<Key>', self.currFrame.processUserKeyInput)


    def switchFrame(self):
        if isinstance(self.currFrame, StartFrame):
            self.startFrame.frame.pack_forget()
            self.players = list(self.startFrame.players.keys())
            self.scramble_func = EVENT_SCRAMBLES[self.startFrame.event]
            self.gameFrame = GameFrame(self, self.players, self.switchFrame, self.scramble_func)
            
            self.gameFrame.frame.pack(expand = True)
            self.currFrame = self.gameFrame
        elif isinstance(self.currFrame, GameFrame):
            #self.bind('<Key>', self.startFrame.recvUserKeyInput)
            self.gameFrame.frame.pack_forget()
            self.startFrame.frame.pack(expand = True)
            self.currFrame = self.startFrame
        self.bind('<Key>', self.currFrame.processUserKeyInput)

    def helper_func(self, key):
        self.currFrame.processUserKeyInput()

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

        self.start_button = customtkinter.CTkButton(master = self.frame, text = "Start", command = swtich_frame_func)
        self.start_button.place(relx = 0.8, rely = 0.95)

        #root.bind('<Key>', self.recvUserKeyInput)
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
        ENTER_KEY = 36 
        if key.keycode == ENTER_KEY:
            self.input_wca_id_button_function()

    def input_wca_id_button_function(self):
        inputted_wca_id = self.wca_id_entry.get()
        self.wca_id_entry_feedback_label.place(relx = 0.8, rely = 0.225, anchor = customtkinter.CENTER)

        if self.playerAlreadyExists(inputted_wca_id):
            self.wca_id_entry_feedback_label.configure(text = "Player Already Exists", text_color = "red")
            return    

        new_player = gennedPlayer(inputted_wca_id, EVENT_CODES[self.event_dropdown.get()])
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


app = App()
app.mainloop()
