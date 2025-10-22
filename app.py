import customtkinter
import requests
from numpy import random

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

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

RESULTS = 'results'
NUM_RESULTS_TO_COLLECT = 50
DNF = 999
DNF_AVG = 999

def clear():
    print(chr(27) + "[2J")

class Player:
    def printSinglesUpToSolveNum(self, solve_num):
        string = f"{self.name}: "
        for i in range(solve_num - 1):
            if self.times[i] == DNF:
                string += "DNF, "
            else:
                string += f"{self.times[i]:.2f}, "
        if self.times[solve_num - 1] == DNF:
            string += "DNF"
        else:
            string += f"{self.times[solve_num - 1]:.2f}"
        print(string)

    def findBPAandWPA(self):
        times = self.times[:4]

        bpa = (sum(times) - max(times)) / 3
        if DNF in times:
            wpa = DNF
        else:
            wpa = (sum(times) - min(times)) / 3
        return bpa, wpa

class userPlayer(Player):
    def __init__(self, name):
        self.name = name
        self.avg = None
        self.times = []
        self.wpa = 0 
        self.bpa = 0

    def addTime(self, new_time):
        self.times.append(new_time)
    
    def generateAvg(self):
        num_dnf = 0
        for num in self.times:
            if num == DNF:
                num_dnf += 1

        if num_dnf > 1:
            self.avg = DNF_AVG

        total = sum(self.times)
        fastest = min(self.times)
        slowest = max(self.times)
        self.avg = (total - fastest - slowest) / (3)



class gennedPlayer(Player):
    def __init__(self, wca_id, event):
        self.wca_id = wca_id
        url = f"https://raw.githubusercontent.com/robiningelbrecht/wca-rest-api/master/api/persons/{self.wca_id}.json"
        self.response = requests.get(url) 
        self.event = event
        if self.validPlayer():
            self.player_data = self.response.json()
            self.name = self.player_data['name']
            self.country = self.player_data['country']
            self.rank, self.pr_avg = self.findAvgStats()
            self.pr_sin = self.findSinStats()
            self.avg, self.times = self.generateNewResults()
            #TODO MAKE THIS EFFICIENT
            self.mo50_recent = self.calculate_mean_of_50_recent_solves()
            self.bpa, self.wpa = self.findBPAandWPA()


    
    
    def findAvgStats(self):
        for event_info in self.player_data['rank']['averages']:
            if self.event == event_info['eventId']:
                return event_info['rank']['world'], event_info['best'] / 100
        return None, None

    def findSinStats(self):
        for event_info in self.player_data['rank']['singles']:
            if self.event == event_info['eventId']:
                return event_info['best'] / 100

    def __str__(self):
        return f"{self.name}, WCA ID: {self.wca_id}"
    
    def __repr__(self):
        return self.__str__()

    def validPlayer(self):
        return self.response.status_code == 200

    def calculate_mean_of_50_recent_solves(self):
        recent_results = self.getRecentResults()
        result = []
        i = 0
        while i < 50 and len(recent_results) > 0:
            result.append( (recent_results.pop() / 100) )
            i += 1
        return sum(result) / len(result)
    
    def getRecentResults(self):
        num_results = 0
        times = []
        if self.validPlayer():
            for comp, results in self.player_data[RESULTS].items():
                if self.event in results:
                    for result in results[self.event]:
                        for solve in result['solves']:
                            if solve != DNF:
                                times.append(solve) 
                                num_results += 1
                            if num_results == NUM_RESULTS_TO_COLLECT:
                                return times
            return times
        else:
            print(f"Request failed with status code {self.response.status_code}")

    def calcNormalDistribution(self, times, nd_size):
        result = []
        if times is None:
            return result
        dist = random.normal(loc = sum(times) / len(times) / 100, scale = 1, size = nd_size)
        # Having 2 guaranteed DNFs is completely arbitrary
        dnf_indices = range(2)
        # Allows for scalability if I want more DNFs in the data set
        dist[dnf_indices] = DNF
        return dist

    def generateNewResults(self):
        recent_results = self.getRecentResults()
        data_nd = self.calcNormalDistribution(recent_results, 98)
        
        times = []
        
        num_dnf = 0
        for _ in range(5):
            new_time = random.choice(data_nd)
            if new_time == DNF:
                num_dnf += 1
            times.append(new_time)
        
        if num_dnf > 1:
            self.avg = DNF_AVG

        total = sum(times)
        fastest = min(times)
        slowest = max(times)
        avg = (total - fastest - slowest) / (3)
        return avg, times



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


class PlayerGameRow():
    def __init__(self, root, x, y, player):
        self.player = player
        self.y = y
        self.frame = root
        self.player_name_label = customtkinter.CTkLabel(root, text = player.name)
        self.player_name_label.grid(row = self.y, column = 1, sticky = "", padx = 10)
        
        self.player_time_label_0 = customtkinter.CTkLabel(root, text = "#####")
        self.player_time_label_1 = customtkinter.CTkLabel(root, text = "#####")
        self.player_time_label_2 = customtkinter.CTkLabel(root, text = "#####")
        self.player_time_label_3 = customtkinter.CTkLabel(root, text = "#####")
        self.player_time_label_4 = customtkinter.CTkLabel(root, text = "#####")

        wpa = "DNF" if self.player.wpa == DNF else f"{self.player.wpa:.2f}"
        self.player_avg_label = customtkinter.CTkLabel(root, text = f"{self.player.bpa:.2f}/{wpa}", text_color = "grey")

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
        #if solve_num >= 3:
        self.player_avg_label.grid(row = new_row_num, column = 7, sticky = "", padx = 10)
        
    
    def displayNextResult(self, solve_num):
        label_to_configure = self.player_time_labels[solve_num]
    
        time_to_display = self.player.times[solve_num]
        if time_to_display == DNF:
            label_to_configure.configure(text = "DNF")
        else:
            label_to_configure.configure(text = f"{time_to_display:.2f}")

        if (solve_num == 3):
            self.player_avg_label.grid(row = self.y, column = 7, sticky = "", padx = 10)
        elif (solve_num == 4):
            self.player_avg_label.configure(text = f"{self.player.avg:.2f}", text_color = "black")




class GameFrame():
    def __init__(self, root, cpu_players):
        self.frame = customtkinter.CTkFrame(master = root, width = 1000, height = 1000, fg_color = "white")
        self.label = customtkinter.CTkLabel(self.frame, text = "WADSHASDHSAJD")
        self.label.place(relx = 0.5, rely = 0.1, anchor = customtkinter.CENTER)
        self.solve_num = 0
        #print(self.players, "AAA") 

        ## DISPLAY PLAYER STATS 
        self.players_container = customtkinter.CTkFrame(master = self.frame, width = 800, height = 800, fg_color = "#f0f0f0")
        self.players_container.place(relx = 0.5, rely = 0.6, anchor = customtkinter.CENTER)

        self.button = customtkinter.CTkButton(master = self.frame, text = "proceed to next solve", command = self.showNextTime)
        self.button.place(relx = 0.8, rely = 0.8, anchor = customtkinter.CENTER)
        
        self.players = {}
        

        self.player_name_header = customtkinter.CTkLabel(master = self.players_container, text = "Player:")
        self.player_name_header.grid(row = 0, column = 1, sticky = "", padx = 10)

        self.player_rank_header = customtkinter.CTkLabel(master = self.players_container, text = "Rank:")
        self.player_rank_header.grid(row = 0, column = 0, sticky = "", padx = 10)
        
        ## SOLVE COLUMNS
        for col_num in range(1, 6):
            self.time_label = customtkinter.CTkLabel(master = self.players_container, text = f"Solve {col_num}:")
            self.time_label.grid(row = 0, column = col_num + 1, sticky = "", padx = 10)

        self.avg_header = customtkinter.CTkLabel(master = self.players_container, text = "Average:")
        self.avg_header.grid(row = 0, column = 7, sticky = "", padx = 10)

         
        for row_num, player in enumerate(cpu_players):
            pos_label = customtkinter.CTkLabel(master = self.players_container, text = f"{row_num + 1}")
            pos_label.grid(row = row_num + 1, column = 0)
            self.players[player] = PlayerGameRow(self.players_container, row_num + 1, row_num + 1, player)
        ## GENERATE USER ROW
        pos_label = customtkinter.CTkLabel(master = self.players_container, text = f"{len(cpu_players) + 1}")
        pos_label.grid(row = len(cpu_players) + 1, column = 0)

        self.user = userPlayer("MEE")
        self.players[self.user] = PlayerGameRow(self.players_container, len(cpu_players) + 1, len(cpu_players) + 1 , self.user)

        ## DISPLAY SCRAMBLE 
        self.scramble_label = customtkinter.CTkLabel(master = self.frame, text = "")
        self.generateScramble()
        self.scramble_label.place(relx = 0.5, rely = 0.2, anchor = customtkinter.CENTER)


        # GET USER INPUT 
        self.time_input_label = customtkinter.CTkEntry(master = self.frame, placeholder_text = "E.G., 6.53")
        self.time_input_label.place(relx = 0.5, rely = 0.8, anchor = customtkinter.CENTER)

        self.enter_time_button = customtkinter.CTkButton(master = self.frame, text = "Enter Time", command = self.processUserTimeInput)
        self.enter_time_button.place(relx = 0.5, rely = 0.9, anchor = customtkinter.CENTER)

    def processUserTimeInput(self):
        time = float(self.time_input_label.get())
        self.user.addTime(time) 
        if self.solve_num == 4:
            self.user.generateAvg()
        self.showNextTime()
        
    def generateScramble(self):
        self.scramble_label.configure(text = "Generating scramble...")
        self.scramble_label.after(100, lambda : self.scramble_label.configure(text = scrambler333.get_WCA_scramble()))

    
    def showNextTime(self):
              
        self.rerankPlayers()
        for player_game_row in self.players.values():
            player_game_row.displayNextResult(self.solve_num)
        self.solve_num += 1

        if self.solve_num <= 4:
            self.generateScramble()        

    def rerankPlayers(self):
        #pprint(self.players.items())
        self.players = dict(sorted(self.players.items(), key = lambda player_info : min(player_info[0].times[:(self.solve_num + 1)])))
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
        #self.startFrame.frame.pack_forget()
        #self.gameFrame.frame.pack(expand = True)
        
        
        self.frames = [self.gameFrame, self.startFrame]

    def switchFrame(self):
        self.startFrame.frame.pack_forget()
        self.players = self.startFrame.getPlayers() 
        
        self.gameFrame = GameFrame(self, self.players)
        self.gameFrame.frame.pack(expand = True)
        print(self.players)
        for p in self.players:
            pprint(p.times)
    


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

        #self.event = customtkinter.StringVar(value=list(EVENT_CODES.keys())[0])
        self.event_dropdown = customtkinter.CTkOptionMenu(self.frame, values=list(EVENT_CODES.keys()),
                                         command=self.event_dropdown_callback,
                                         )
        
        self.event_dropdown.place(relx=0.55, rely = 0.21)
        self.event = None

        
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

    def startRound(self):
        print("STARTED")
        
    def getPlayers(self):
        return list(self.players.keys())

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
