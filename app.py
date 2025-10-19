import customtkinter
import requests
from numpy import random

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

app = customtkinter.CTk()  # create CTk window like you do with the Tk window
app.geometry("400x240")



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


def button_function():
    inputted_wca_id = wca_id_entry.get()
    new_player = gennedPlayer(inputted_wca_id)
    if new_player.validPlayer() is False:
        wca_id_entry_feedback_label.configure(text = "WCA ID invalid", text_color = "red")
        return
    wca_id_entry_feedback_label.configure(text = "Input successful", text_color = "green")
    wca_id_entry_feedback_label.place(relx = 0.5, rely = 0.19, anchor = customtkinter.CENTER)

    wca_id_entry.delete(0, len(inputted_wca_id))
    new_player.generateNewResults('333')
    print(new_player.times)
    print(new_player.avg)

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
wca_id_entry.place(relx = 0.5, rely = 0.225, anchor = customtkinter.CENTER)

wca_id_entry_feedback_label = customtkinter.CTkLabel(app, text = "WCA ID invalid",
                                                     text_color = "red",
                                                     font = ("TkDefaultFont", 15))
wca_id_entry_feedback_label.place_forget()
app.mainloop()
