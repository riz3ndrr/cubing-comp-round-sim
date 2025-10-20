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


class gennedPlayer(Player):
    def __init__(self, wca_id):
        self.wca_id = wca_id
        url = f"https://raw.githubusercontent.com/robiningelbrecht/wca-rest-api/master/api/persons/{self.wca_id}.json"
        self.response = requests.get(url) 
        if self.validPlayer():
            self.player_data = self.response.json()
            self.name = self.player_data['name']
        else:
            self.name = None
    
    def __str__(self):
        return f"{self.name}, WCA ID: {self.wca_id}"
    
    def __repr__(self):
        return self.__str__()

    def validPlayer(self):
        return self.response.status_code == 200
    
    def getRecentResults(self, event):
        num_results = 0
        times = []
        if self.validPlayer():
            for comp, results in self.player_data[RESULTS].items():
                if event in results:
                    for result in results[event]:
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

    def generateNewResults(self, event):
        recent_results = self.getRecentResults(event)
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
        self.avg = (total - fastest - slowest) / (3)
        self.times = times



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
    def __init__(self, frame, x, y, wca_id, name, remove_player_func, player):
        #super().__init__(frame)
        self.player = player
        self.player_wca_label = customtkinter.CTkLabel(frame,
                                                   text = wca_id,
                                                    fg_color = "transparent",
                                                    font = ("TkDefaultFont", 17))

        self.player_name_label = customtkinter.CTkLabel(frame,
                                                        text = name,
                                                        fg_color = "transparent",
                                                        font = ("TkDefaultFont", 17))
        self.x = x
        self.player_wca_label.place(relx = self.x, rely = y, anchor = customtkinter.CENTER)
        self.player_name_label.place(relx = self.x + 0.25, rely = y, anchor = customtkinter.CENTER)

        self.x_button = customtkinter.CTkButton(master = frame, text = "X", fg_color = "#e01010", hover_color = "#c70e0e", command = self.remove_row, width = 50)
        self.x_button.place(relx = x + 0.4, rely = y, anchor = customtkinter.CENTER)
        self.remove_player_callback_func = remove_player_func

    def remove_row(self):
        self.remove_player_callback_func(self.player)
        self.player_wca_label.destroy()
        self.player_name_label.destroy()
        self.x_button.destroy()

    def change_pos(self, new_y):
        self.player_wca_label.place(relx = self.x, rely = new_y, anchor = customtkinter.CENTER)
        self.player_name_label.place(relx = self.x + 0.25, rely = new_y, anchor = customtkinter.CENTER)
        self.x_button.place(relx = self.x + 0.4, rely = new_y, anchor = customtkinter.CENTER)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("500x1000") 

        self.app_label = customtkinter.CTkLabel(self, 
                                        text = "WCA Competition Round Simulator",
                                        fg_color = "transparent",
                                        font = ("TkDefaultFont", 35))
        self.app_label.place(relx = 0.5, rely = 0.1, anchor=customtkinter.CENTER)


        self.subtitle1 = customtkinter.CTkLabel(self,
                                        text = "Add Competitor",
                                        fg_color = "transparent",
                                        font = ("TkDefaultFont", 20))
        self.subtitle1.place(relx = 0.5, rely = 0.175, anchor = customtkinter.CENTER)


        self.wca_id_entry = customtkinter.CTkEntry(self, width = 200, placeholder_text="Enter your opponent(s)' WCA ID")
        self.wca_id_entry.place(relx = 0.7, rely = 0.135, anchor = customtkinter.CENTER)


        self.input_wca_id_button = customtkinter.CTkButton(master=self, text="Enter", command=self.input_wca_id_button_function)
        self.input_wca_id_button.place(relx=0.9, rely=0.135, anchor=customtkinter.CENTER)

        self.wca_id_entry_feedback_label = customtkinter.CTkLabel(self, text = "WCA ID invalid",
                                                            text_color = "red",
                                                            font = ("TkDefaultFont", 20))
        self.wca_id_entry_feedback_label.place_forget()


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

    
        self.players_frame = customtkinter.CTkFrame(self, width=700, height=700, fg_color = "#ffffff", border_color = "black", border_width = 2)
        self.players_frame.place(relx=0.5, rely=0.6, anchor = customtkinter.CENTER)
        
        self.players_frame_header1_offsetx = 0.05
        self.players_frame_header2_offsetx = self.players_frame_header1_offsetx + 0.25
        self.player_frame_header1= customtkinter.CTkLabel(self.players_frame, text = "WCA ID", fg_color = "transparent", font = ("TkDefaultFont", 25))
        self.player_frame_header1.place(relx = self.players_frame_header1_offsetx, rely = 0.05)

        self.player_frame_header2= customtkinter.CTkLabel(self.players_frame, text = "Name", fg_color = "transparent", font = ("TkDefaultFont", 25))
        self.player_frame_header2.place(relx = self.players_frame_header2_offsetx, rely = 0.05)


        self.players = {}
        self.players_row_offsety = 0.15
        

    def event_dropdown_callback(self, choice):
        print("optionmenu dropdown clicked:", choice)

    
    def remove_player(self, player):
        if player in self.players:
            self.players.pop(player)  
        self.shift_player_rows()

    def shift_player_rows(self): 
        for i, row in enumerate(self.players.values()):
            row.change_pos(0.15 + 0.1 * i)
        self.players_row_offsety = 0.15 + 0.1 * len(self.players)

    
    def playerAlreadyExists(self, wca_id):
        for opp in self.players.keys():
            if opp.wca_id == wca_id:
                return True
        return False


    def input_wca_id_button_function(self):
        inputted_wca_id = self.wca_id_entry.get()
        

        self.wca_id_entry_feedback_label.place(relx = 0.5, rely = 0.20, anchor = customtkinter.CENTER)

        if self.playerAlreadyExists(inputted_wca_id):
            self.wca_id_entry_feedback_label.configure(text = "Player Already Exists", text_color = "red")
            return    

        new_player = gennedPlayer(inputted_wca_id)
        if new_player.validPlayer() is False:
            self.wca_id_entry_feedback_label.configure(text = "WCA ID invalid", text_color = "red")
            return

        self.wca_id_entry_feedback_label.configure(text = "Input successful", text_color = "green")
        self.wca_id_entry.delete(0, len(inputted_wca_id))
        
        new_row = PlayerRowLabel(self.players_frame,
                                 self.players_frame_header1_offsetx + 0.08,
                                 self.players_row_offsety,
                                 new_player.wca_id,
                                 new_player.name,
                                 self.remove_player,
                                 new_player)

        self.players[new_player] = new_row
        self.players_row_offsety = 0.15 + 0.1 * len(self.players)
        print(len(self.players))
        new_player.generateNewResults('333')
        print(new_player.times)
        print(new_player.avg)


app = App()
app.mainloop()
