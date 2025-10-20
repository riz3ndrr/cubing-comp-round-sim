import customtkinter
import requests
from numpy import random

from pprint import pprint

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

class userPlayer(Player):
    def __init__(self, name):
        self.name = name
        self.avg = None
        self.times = []

    def addTime(self):
        new_time = float(input("What did you get on this scramble? "))
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

EVENT_INDEX_MAP = {
    "222": 0,
    "333": 1,
    "444": 2,
    "555": 3,
    "666": 4,
    "777": 5,
    "333bf": 6,
    "333fm": 7,
    "333oh": 8,
    "clock": 9,
    "minx": 10,
    "pyram": 11,
    "skewb": 12,
    "sq1": 13,
    "444bf": 14,
    "555bf": 15,
    "333mbf": 16
}

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
            self.rank = self.player_data['rank']['averages'][EVENT_INDEX_MAP[event]]['rank']['world']
            self.pr_avg = self.player_data['rank']['averages'][EVENT_INDEX_MAP[event]]['best'] / 100
            self.pr_sin = self.player_data['rank']['singles'][EVENT_INDEX_MAP[event]]['best'] / 100
            self.avg, self.times = self.generateNewResults()
            #TODO MAKE THIS EFFICIENT
            self.mo50_recent = self.calculate_mean_of_50_recent_solves()

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



EVENT_NAMES = [
    "2x2x2 Cube",
    "3x3x3 Cube",
    "3x3x3 Blindfolded",
    "3x3x3 Fewest Moves",
    "3x3x3 One-Handed",
    "4x4x4 Cube",
    "4x4x4 Blindfolded",
    "5x5x5 Cube",
    "5x5x5 Blindfolded",
    "6x6x6 Cube",
    "7x7x7 Cube",
    "Clock",
    "Megaminx",
    "Pyraminx",
    "Skewb",
    "Square-1",
    "3x3x3 Multi-Blind"
]

class PlayerRowLabel():
    ## TODO MAKE THIS EFFFICIENT
    def __init__(self, root, x, y, remove_player_func, player):
        #super().__init__(frame)
        self.container = customtkinter.CTkFrame(root, width=400, height=150, fg_color = "#ffffff", border_color = "grey", border_width = 1)
        self.container.grid(row = y, column = 0, sticky = "ew", padx = 15, pady=15)
        #self.container.grid_propagate(False)
        self.player = player
        self.player_wca_label = customtkinter.CTkLabel(self.container,
                                                    text = player.wca_id,
                                                    text_color = "grey",
                                                    font = ("TkDefaultFont", 17))

        self.player_name_label = customtkinter.CTkLabel(self.container,
                                                        text = player.name,
                                                        font = ("TkDefaultFont", 20))
        self.x = x
        self.player_name_label.grid(row = 0, column = 0, sticky = 'W', pady = 2, padx = 4,)
        self.player_wca_label.grid(row = 5, column = 5, sticky = 'W', pady = 2, padx = 2)

        
        ## PR AVG LABELS
        self.pr_avg_header = customtkinter.CTkLabel(self.container,
                                                    text = "PR Average:",
                                                    text_color = "grey",
                                                    font = ("TkDefaultFont", 17))

        self.pr_avg_label = customtkinter.CTkLabel(self.container,
                                                    text = player.pr_avg,
                                                    text_color = "black",
                                                    font = ("TkDefaultFont", 19))

        self.pr_avg_header.grid(row = 1, column = 0, sticky = 'W', pady = 2, padx = 4)
        self.pr_avg_label.grid(row = 2, column = 0, sticky = 'W', pady = 2, padx = 4)

        ## PR SINGLE LABELS
        self.pr_sin_header = customtkinter.CTkLabel(self.container,
                                                    text = "PR Single:    ",
                                                    text_color = "grey",
                                                    font = ("TkDefaultFont", 17))

        self.pr_sin_label = customtkinter.CTkLabel(self.container,
                                                    text = player.pr_sin,
                                                    text_color = "black",
                                                    font = ("TkDefaultFont", 19))
            
        self.pr_sin_header.grid(row = 3, column = 0, sticky = 'W', pady = 2, padx = 4)
        self.pr_sin_label.grid(row = 4, column = 0, sticky = 'W', pady = 2, padx = 4)


        ## WORLD RANK LABELS
        self.wr_header = customtkinter.CTkLabel(self.container,
                                                    text = "World Ranking:    ",
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
     
        self.country_header.grid(row = 3, column = 1, sticky = 'W', pady = 2, padx = 2)
        self.country_label.grid(row = 4, column = 1, sticky = 'W', pady = 2, padx = 2)
   
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
        self.x_button.grid(row = 0, column = 5, sticky = 'E', pady = 5, padx = 5)
        self.remove_player_callback_func = remove_player_func

        self.container.grid_columnconfigure(0, weight=1)  # left content
        self.container.grid_columnconfigure(1, weight=1)
        self.container.grid_columnconfigure(2, weight=1)
        self.container.grid_columnconfigure(3, weight=1)
        self.container.grid_columnconfigure(4, weight=1)
        self.container.grid_columnconfigure(5, weight=0)  # X button column (fixed) 

    def remove_row(self):
        self.remove_player_callback_func(self.player)
        for widget in self.container.winfo_children():
            widget.destroy()
        self.container.destroy()

    def change_pos(self, new_y):
        self.container.grid(row = new_y, column = 0, padx = 15, pady=15 ) 

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("500x1000") 

        self.app_label = customtkinter.CTkLabel(self, 
                                        text = "WCA Competition Round Simulator",
                                        fg_color = "transparent",
                                        font = ("TkDefaultFont", 35))
        self.app_label.place(relx = 0.5, rely = 0.1, anchor=customtkinter.CENTER)

        # ADD COMPETITOR
        self.subtitle1 = customtkinter.CTkLabel(self,
                                        text = "Add Competitor",
                                        fg_color = "transparent",
                                        font = ("TkDefaultFont", 20))
        self.subtitle1.place(relx = 0.2, rely = 0.185, anchor = customtkinter.CENTER)


        self.wca_id_entry = customtkinter.CTkEntry(self, width = 250, placeholder_text="Enter your opponent(s)' WCA ID")
        self.wca_id_entry.place(relx = 0.275, rely = 0.225, anchor = customtkinter.CENTER)


        self.input_wca_id_button = customtkinter.CTkButton(master=self, text="Enter", command=self.input_wca_id_button_function)
        self.input_wca_id_button.place(relx = 0.5, rely = 0.225, anchor=customtkinter.CENTER)

        self.wca_id_entry_feedback_label = customtkinter.CTkLabel(self, text = "WCA ID invalid",
                                                            text_color = "red",
                                                            font = ("TkDefaultFont", 20))
        self.wca_id_entry_feedback_label.place_forget()

        
        ## CONFIGURE EVENT
        self.event_label = customtkinter.CTkLabel(self, 
                                        text = "Event: ",
                                        fg_color = "transparent",
                                        font = ("TkDefaultFont", 25))
        self.event_label.place(relx = 0.3, rely = 0.135, anchor=customtkinter.CENTER)

        self.event = customtkinter.StringVar(value=EVENT_NAMES[0])
        self.event_dropdown = customtkinter.CTkOptionMenu(self, values=EVENT_NAMES,
                                         command=self.event_dropdown_callback,
                                         variable=self.event)
        
        self.event_dropdown.place(relx=0.35, rely = 0.1215)

        
        ## FRAME / COMPETITORS CONTAINER ##
        self.players_frame = customtkinter.CTkScrollableFrame(self, width=700, height=600, fg_color = "#ffffff", border_color = "black", border_width = 2)
        self.players_frame.place(relx=0.5, rely=0.65, anchor = customtkinter.CENTER)
        self.players_frame_header = customtkinter.CTkLabel(self, text = "Competitors", fg_color = "transparent", font = ("TkDefaultFont", 30))
        self.players_frame_header.place(relx = 0.1, rely = 0.25)

        self.players = {}
        self.players_row_offsety = 0
        

    def event_dropdown_callback(self, choice):
        print("optionmenu dropdown clicked:", choice)

    
    def remove_player(self, player):
        if player in self.players:
            self.players.pop(player)  
        self.shift_player_rows()

    def shift_player_rows(self): 
        for i, row in enumerate(self.players.values()):
            row.change_pos(i)
        self.players_row_offsety = len(self.players)

    
    def playerAlreadyExists(self, wca_id):
        for opp in self.players.keys():
            if opp.wca_id == wca_id:
                return True
        return False


    def input_wca_id_button_function(self):
        inputted_wca_id = self.wca_id_entry.get()
        

        self.wca_id_entry_feedback_label.place(relx = 0.675, rely = 0.225, anchor = customtkinter.CENTER)

        if self.playerAlreadyExists(inputted_wca_id):
            self.wca_id_entry_feedback_label.configure(text = "Player Already Exists", text_color = "red")
            return    

        new_player = gennedPlayer(inputted_wca_id, '333')
        pprint(new_player.rank)
        if new_player.validPlayer() is False:
            self.wca_id_entry_feedback_label.configure(text = "WCA ID invalid", text_color = "red")
            return

        self.wca_id_entry_feedback_label.configure(text = "Input successful", text_color = "green")
        self.wca_id_entry.delete(0, len(inputted_wca_id))
        
        new_row = PlayerRowLabel(self.players_frame,
                                 3,
                                 self.players_row_offsety,
                                 self.remove_player,
                                 new_player)

        self.players[new_player] = new_row
        self.players_row_offsety = len(self.players)
        print(len(self.players))
        print(new_player.times)
        print(new_player.avg)


app = App()
app.mainloop()
