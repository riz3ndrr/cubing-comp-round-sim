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

from constants import GAME, START, DNF, MO3_EVENTS
from helper_functions import convertToReadableTime, convertTimeStringToSec
from popup import popupFrame

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

GREY = "#c3c7c4"

class PlayerGameRow():
    def __init__(self, root, x, y, player, num_solves, is_player, game_frame, toggleDisableFunc):
        self.player = player
        self.y = y
        self.frame = root
        self.game_frame = game_frame

        NAME_DISPLAY_LENGTH = 16
        display_name = player.name
        if len(display_name) > NAME_DISPLAY_LENGTH:
            display_name = display_name[:NAME_DISPLAY_LENGTH - 3] + "..."
        elif len(display_name) < NAME_DISPLAY_LENGTH:
            display_name += " " * (NAME_DISPLAY_LENGTH - len(display_name))


        self.toggleDisableFunc = toggleDisableFunc
        self.player_name_label = customtkinter.CTkLabel(root, text = display_name, width = 150, font = ("TkDefaultFont", 20))
        self.player_name_label.grid(row = self.y, column = 1, sticky = "ew", padx = 10, pady = 10)

        self.player_avg_label = customtkinter.CTkLabel(root, text = "N/A", font = ("TkDefaultFont", 20))
        self.player_time_labels = [customtkinter.CTkButton(root, text = "#####", text_color = "black", width = 50, fg_color = GREY, hover_color = GREY, font = ("TkDefaultFont", 20)) for x in range(num_solves)]
       # self.player_time_labels = [customtkinter.CTkButton(root, text = "#####", font = ("TkDefaultFont", 20),
       #                                                    command = self.changeTime, fg_color = "transparent")
       #                                                    for x in range(num_solves)]


        for col_num, time_label in enumerate(self.player_time_labels):
            if is_player:
                time_label.configure(command = lambda c = col_num : self.changeTime(c))
            time_label.bind("<Enter>", lambda event, tl = time_label: tl.configure(text_color = "red"))
            time_label.bind("<Leave>", lambda event, tl = time_label: tl.configure(text_color = "black"))
            time_label.grid(row = self.y, column = col_num + 2, sticky = "", padx = 10)
            # STOP FOR MO3 EVENTS
            

        #self.frame.grid_columnconfigure(0, weight = 0)
    def changeTime(self, i):
        if i < len(self.player.times):
            self.toggleDisableFunc()
            popup = ChangeTimePopup(self.game_frame, self.player, self.player.times[i])
            print(self.player.times)
            print("CHANGING TIME," + str(i))

    def repositionLabels(self, new_row_num, solve_num, num_solves_in_round):
        self.player_name_label.grid(row = new_row_num, column = 1, sticky = "", padx = 10)
        for col_num, time_label in enumerate(self.player_time_labels):
            time_label.grid(row = new_row_num, column = col_num + 2, sticky = "", padx = 10)
        if solve_num >= num_solves_in_round - 2:
            self.player_avg_label.grid(row = new_row_num, column = 7, sticky = "", padx = 10)
    
    def resetLabels(self):
        self.player_avg_label.grid_forget()
        for time_label in self.player_time_labels:
            time_label.configure(text = "#####")
    
    def displayNextResult(self, solve_num, num_solves_in_round):
        label_to_configure = self.player_time_labels[solve_num]
    
        time_to_display = self.player.times[solve_num]
        if time_to_display == DNF:
            label_to_configure.configure(text = "DNF")
        else:
            label_to_configure.configure(text = convertToReadableTime(time_to_display))

        if (solve_num == num_solves_in_round - 2):
            if num_solves_in_round == 5:
                #self.player_avg_label.grid(row = self.y, column = 7, sticky = "", padx = 10)
                wpa = "DNF" if self.player.wpa == DNF else convertToReadableTime(self.player.wpa)
                self.player_avg_label.configure(text = f"{convertToReadableTime(self.player.bpa)}/{wpa}", text_color = "grey")
            else:
                # Show provisional mean 
                print("RAHHH")
                self.player_avg_label.configure(text = convertToReadableTime(self.player.provisionalMean), text_color = "grey")
        elif (solve_num == num_solves_in_round - 1):
            avg = "DNF" if self.player.avg == DNF else convertToReadableTime(self.player.avg)
            self.player_avg_label.configure(text = avg, text_color = "black")

class ChangeTimePopup():
    def __init__(self, root, player, current_time):
        self.frame = customtkinter.CTkFrame(master = root, width = 600, height = 200)
        self.frame.place(relx = 0.25, rely = 0.2)
        self.entry = customtkinter.CTkEntry(master = self.frame, state = "normal")
        self.entry.place(relx = 0.25, rely = 0.5)
        self.entry.insert(0, current_time)





class GameFrame():
    def __init__(self, root, cpu_players, switchFrameFunc, event):
        self.frame = customtkinter.CTkFrame(master = root, width = 1000, height = 1000, fg_color = "white")
        #self.label = customtkinter.CTkLabel(self.frame, text = "WADSHASDHSAJD")
        #self.label.place(relx = 0.5, rely = 0.1, anchor = customtkinter.CENTER)
        self.solve_num = 0
        self.event = event
        self.disabled = False
        if self.event in MO3_EVENTS:
            self.num_solves = 3 
        else:
            self.num_solves = 5

        self.scramble_func = EVENT_INFO[self.event][0]


        ## PLAYER CONTAINER
        self.players_container = customtkinter.CTkScrollableFrame(master = self.frame, width = 850, height = 700, fg_color = GREY)
        self.players_container.place(relx = 0.5, rely = 0.65, anchor = customtkinter.CENTER)

        ## DISPLAY PLAYER STATS 
        
        self.players = {}
        
        self.player_name_header = customtkinter.CTkLabel(master = self.players_container, width = 150, text = "Player:", font = ("TkDefaultFont", 20))
        self.player_name_header.grid(row = 0, column = 1, sticky = "", padx = 10)

        self.player_rank_header = customtkinter.CTkLabel(master = self.players_container, text = "Rank:", font = ("TkDefaultFont", 20))
        self.player_rank_header.grid(row = 0, column = 0, sticky = "", padx = 10)
        
        ## SOLVE COLUMNS
        for col_num in range(1, self.num_solves + 1):
            self.time_label = customtkinter.CTkLabel(master = self.players_container, text = f"Solve {col_num}:", font = ("TkDefaultFont", 20))
            self.time_label.grid(row = 0, column = col_num + 1, sticky = "", padx = 10)

        self.avg_header = customtkinter.CTkLabel(master = self.players_container, text = "Average:", font = ("TkDefaultFont", 20))
        self.avg_header.grid(row = 0, column = 7, sticky = "", padx = 10)

         
        for row_num, player in enumerate(cpu_players):
            pos_label = customtkinter.CTkLabel(master = self.players_container, text = f"{row_num + 1}", font = ("TkDefaultFont", 20))
            pos_label.grid(row = row_num + 1, column = 0)
            self.players[player] = PlayerGameRow(self.players_container, row_num + 1, row_num + 1, player, self.num_solves, False)

        ## GENERATE USER ROW
        pos_label = customtkinter.CTkLabel(master = self.players_container, text = f"{len(cpu_players) + 1}", font = ("TkDefaultFont", 20))
        pos_label.grid(row = len(cpu_players) + 1, column = 0)

        self.user = UserPlayer("You", event)
        self.players[self.user] = PlayerGameRow(self.players_container, len(cpu_players) + 1, len(cpu_players) + 1 , self.user, self.num_solves, True, self.frame, self.toggleDisable)

        ## DISPLAY SCRAMBLE 
        self.scramble_list = []
        scramble_font_size = EVENT_INFO[self.event][1]
        self.scramble_label = customtkinter.CTkLabel(master = self.frame, text = "", font = ("TkDefaultFont", scramble_font_size),
                                                     wraplength = 800, justify = customtkinter.CENTER, width = 700)
        self.generateScramble()
        self.scramble_label.place(relx = 0.5, rely = 0.1, anchor = customtkinter.CENTER)


        # GET USER INPUT
        
        
        user_input_y = 0.2
        self.time_input_label = customtkinter.CTkEntry(master = self.frame, placeholder_text = "E.G., 6.53", width = 400, state = "normal")
        self.time_input_label.place(relx = 0.4, rely = user_input_y, anchor = customtkinter.CENTER)

        self.enter_time_button = customtkinter.CTkButton(master = self.frame, text = "Enter Time", command = self.processUserTimeInput,
                                                         height = 30, state = "normal")
        self.enter_time_button.place(relx = 0.7, rely = user_input_y, anchor = customtkinter.CENTER)

        self.rematch_button = customtkinter.CTkButton(master = self.frame, text = "Rematch (R)", command = self.resetRound, width = 200, height = 40)
        self.rematch_button.place(relx = 0.35, rely = user_input_y + 0.05, anchor = customtkinter.CENTER)

            ## SWITCH FRAMES 
        self.switchFrameFunc = switchFrameFunc
        self.switch_frame_button = customtkinter.CTkButton(master = self.frame, text = "Change Competitors (C)", 
                                                           command = lambda: self.switchFrame(), width = 200, 
                                                           height = 40)
        self.switch_frame_button.place(relx = 0.6, rely = user_input_y + 0.05, anchor = customtkinter.CENTER)

        # USER FEEDBACK 
        
        self.error_popup = popupFrame(self.frame, "Please correctly input a time", "red", 500, 200)
       # self.error_label = customtkinter.CTkLabel(master = self.frame, text = "Please correctly input a time", text_color = "red",
       #                                           font = ("TkDefaultFont", 20))
        #root.bind('<Key>', self.enterUserTime)
        #TODO DISABLE FUNCTION

    def toggleDisable(self):
        self.disabled = not self.disabled
        if self.disabled:
            self.time_input_label.configure(state = "disabled")
        else:
            self.time_input_label.configure(state = "normal")

    def switchFrame(self):
        if self.disabled:
            return 

        if len(self.user.times) == self.num_solves:
            self.user.updateCSV(self.getPlacing() ,len(self.players))
        self.switchFrameFunc(START)

    def resetRound(self):
        if self.disabled:
            return 

        if len(self.user.times) == self.num_solves:
            self.user.updateCSV(self.getPlacing() ,len(self.players))

        self.time_input_label.delete(0, len(self.time_input_label.get()))
        self.time_input_label.configure(state = "normal")
        self.enter_time_button.configure(state = "normal")
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
        if key.keysym == "Return" and (self.solve_num < self.num_solves):
            self.processUserTimeInput()
        elif key.keysym == "R":
            self.resetRound()
        elif key.keysym == "C":
            self.switchFrame()

    def getPlacing(self):
        for i, player in enumerate(self.players):
            if isinstance(player, UserPlayer):
                return i + 1
        return None
    
    def processUserTimeInput(self):
        if self.disabled:
            return

        time = self.time_input_label.get()

        if time == 'DNF':
            self.user.addTime(DNF)
        else:
            time = convertTimeStringToSec(time)
            if time is None:
                #self.error_label.place(relx = 0.5, rely = 0.15, anchor = customtkinter.CENTER)
                self.error_popup.place()
                return

            self.user.addTime(time)

        if self.solve_num == (self.num_solves - 1):
            self.user.generateAvg()
        elif self.solve_num == (self.num_solves - 2):
            if self.num_solves == 5:
                self.user.calcBPAandWPA()
            else:
                self.user.calcProvisionalMean()

        self.showNextTime()
        self.error_popup.forget()
        self.time_input_label.delete(0, len(str(time)))
            


             
            
    def generateScramble(self):
        self.scramble_label.configure(text="Generating scrambles...")
        self.scramble_list = []
        def showFirstScramble():
            first_scramble = self.scramble_func()
            self.scramble_label.configure(text = first_scramble)
            self.scramble_list.append(first_scramble)

            def generateRest():
                for _ in range(self.num_solves - 1):
                    self.scramble_list.append(self.scramble_func())
                pprint(self.scramble_list)

            self.scramble_label.after(100, generateRest)

        self.scramble_label.after(500, showFirstScramble)
        pprint(self.scramble_list)
        
    def showNextTime(self):
              
        self.rerankPlayers()
        for player_game_row in self.players.values():
            player_game_row.displayNextResult(self.solve_num, self.num_solves)
        self.solve_num += 1

        if self.solve_num < self.num_solves:
            self.scramble_label.configure(text = self.scramble_list[self.solve_num])
        else:
            self.time_input_label.configure(state = "disabled")
            self.enter_time_button.configure(state = "disabled")


    def rerankPlayers(self):
        #pprint(self.players.items())
        if self.solve_num < (self.num_solves - 1):
            self.players = dict(sorted(self.players.items(), key = lambda player_info : min(player_info[0].times[:(self.solve_num + 1)])))
        else:
            self.players = dict(sorted(self.players.items(), key = lambda player_info : player_info[0].avg))

        #pprint(self.players.items())
        for new_row_num, player_row in enumerate(self.players.values()):
            player_row.repositionLabels(new_row_num + 1, self.solve_num, self.num_solves)

        


