import customtkinter
from PIL import Image
import csv
import pandas as pd
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from constants import GAME, START, STAT, MO3_EVENTS, DNF
from helper_functions import convertToReadableTime

DIR1 = '../data/'
DIR2 = '.csv'

GREY = "#a7a7a8"
LIGHT_BLUE = "#e3faff"
LIGHT_GREY = "#e6edf0"
RED = "#e64040"

EVENT_NAMES = [
    "3x3x3 Cube",
    "2x2x2 Cube",
    "4x4x4 Cube",
    "5x5x5 Cube",
    "6x6x6 Cube",
    "7x7x7 Cube",
    "3x3x3 Blindfolded",
    "3x3x3 Fewest Moves",
    "3x3x3 One-Handed",
    "Clock",
    "Megaminx",
    "Pyraminx",
    "Skewb",
    "Square-1",
    "4x4x4 Blindfolded",
    "5x5x5 Blindfolded",
]


class StatFrame():
    def __init__(self, root, switch_frame_func, event):
        self.frame = customtkinter.CTkFrame(root, width = 1000, height = 1000, fg_color = "white")
        self.header = customtkinter.CTkLabel(self.frame, text = f"Player stats",
                                             font = ("TkDefaultFont", 40))
        self.header.place(relx = 0.35, rely = 0.05)
       
        self.event = event
        self.num_solves = 3 if self.event in MO3_EVENTS else 5

        # CHANGE EVENT DROPDOWN
        self.change_event_label = customtkinter.CTkLabel(master = self.frame, text = "Change Event",
                                                         font = ("TkDefaultFont", 23))
        self.change_event_label.place(relx = 0.3, rely = 0.125)
        self.event_dropdown = customtkinter.CTkOptionMenu(self.frame, values = EVENT_NAMES,
                                                          command = self.event_dropdown_callback,
                                                          width = 140, height = 30)
        self.event_dropdown.set(event)
        self.event_dropdown.place(relx = 0.5, rely = 0.13)
        
        # SWITCH FRAME WIDGET
        self.switch_frame_func = switch_frame_func
        self.switch_frame_button = customtkinter.CTkButton(master = self.frame, text = "Main Menu (-)",
                                                           command = lambda: self.switch_frame_func(START),
                                                           width = 220, height = 50,
                                                           font = ("TkDefaultFont", 20))
        self.switch_frame_button.place(relx = 0.39, rely = 0.75)
        
        # CLEAR DATA WIDGET 
        self.clear_data_button = customtkinter.CTkButton(master = self.frame, text = "Clear Data (D)",
                                                         command = self.clear_data,
                                                         fg_color = RED,
                                                         width = 220, height = 50,
                                                         font = ("TkDefaultFont", 20))
        self.clear_data_button.place(relx = 0.39, rely = 0.82)
        
        # STATS
        self.initDataFrame()
        self.showGraph()
        


        self.showSummaryStats() 

        ## DRAWING LINE 
        self.line = customtkinter.CTkFrame(self.frame, width = 900, height = 3, fg_color = "black")
        self.line.place(relx=0.05, rely= 0.175)
        ## DISPLAY TIMES 
        self.displayTopResults()
        print(self.data_frame)

    def clear_data(self):
        filename = f"../data/{self.event}.csv"
        with open(filename, 'w') as players_csv:
            num_times = 3 if self.event in MO3_EVENTS else 5 
            headers = [[f"t{x + 1}" for x in range(num_times)] + ["average", "placing", "num_ppl"]]
            csvwriter = csv.writer(players_csv)
            csvwriter.writerows(headers)
            
        self.forgetStatWidgets()
        self.initDataFrame()
        self.refreshStatWidgets()


    def initDataFrame(self):
        filename = DIR1 + self.event + DIR2
        try:
            self.data_frame = pd.read_csv(filename)
        except FileNotFoundError:
            default_data = [
                [f"t{x + 1}" for x in range(self.num_solves)] + ["average", "placing", "num_ppl"]
            ]

            with open(filename, 'w', newline='') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerows(default_data)
            self.data_frame = pd.read_csv(filename)


    def event_dropdown_callback(self, new_event):
        self.event = new_event
        self.num_solves = 3 if self.event in MO3_EVENTS else 5
        self.forgetStatWidgets()
        
        self.initDataFrame()
        self.refreshStatWidgets()


    def forgetStatWidgets(self):
        stat_widgets = [self.placing_header, self.placing_label,
                       self.mean_time_header, self.mean_time_label,
                       self.mean_avg_header, self.mean_avg_label,
                       self.canvas.get_tk_widget()]
        for w in stat_widgets:
            w.place_forget()


        for child in self.top_means_container.winfo_children():
            child.destroy()
        for child in self.top_singles_container.winfo_children():
            child.destroy()
    def refreshStatWidgets(self):
        self.showGraph()
        self.showSummaryStats()
        self.displayTopResults()


                

    def genSuffix(self, number):
        conversion = {0 : "th",
                      1 : "st",
                      2 : "nd",
                      3 : "rd",
                      4 : "th",
                      5 : "th",
                      6 : "th",
                      7 : "th",
                      8 : "th",
                      9 : "th"}
        if number in conversion:
            return conversion[number]
        if (number % 100) >= 11 and (number % 100) <= 19:
            return "th"
        else:
            return conversion[number % 10]


    def showSummaryStats(self):
        results = self.data_frame

        LABEL_Y = 0.20

        # PLACING RESULTS
        placing_results = results[["placing", "num_ppl"]].mean()
        if np.isnan(placing_results["placing"]):
            placing_text = "N/A"
        else:
            avg_placing = round(placing_results["placing"])
            avg_num_ppl = round(placing_results["num_ppl"]) 
            placing_text = f"{avg_placing}{self.genSuffix(avg_placing)} out of {avg_num_ppl} people" 
    
        self.placing_container = customtkinter.CTkFrame(self.frame, width = 280, height = 100, fg_color = "transparent", border_color = GREY, border_width = 2)
        self.placing_container.place(relx=0.05, rely = LABEL_Y)

        self.placing_header = customtkinter.CTkLabel(self.placing_container, text = "Average Placing", font = ("TkDefaultFont", 20), fg_color="transparent")
        self.placing_label = customtkinter.CTkLabel(self.placing_container, text = placing_text, font = ("TkDefaultFont", 15), fg_color="transparent")
        self.placing_header.place(relx = 0.22, rely = 0.1)
        self.placing_label.place(relx = 0.22, rely = 0.4)
        #self.placing_header.place(relx = 0.1, rely = LABEL_Y) 
        #self.placing_label.place(relx = 0.125, rely = LABEL_Y + 0.05)

        # MEAN RESULTS
        time_cols = [f"t{x + 1}" for x in range(self.num_solves)]
        times = (results[time_cols].melt())
        times = times[times.value != DNF]
        mean_time = times["value"].mean()
        if np.isnan(mean_time):
            mean_sin_text = "N/A"
        else:
            mean_sin_text = convertToReadableTime(mean_time)


        self.mean_time_container = customtkinter.CTkFrame(self.frame, width = 280, height = 100, fg_color = "transparent", border_color = GREY, border_width = 2)
        self.mean_time_container.place(relx=0.36, rely = LABEL_Y)
        self.mean_time_header = customtkinter.CTkLabel(self.mean_time_container, text = "Average Time", font = ("TkDefaultFont", 20))
        self.mean_time_label = customtkinter.CTkLabel(self.mean_time_container, text = mean_sin_text, font = ("TkDefaultFont", 17))
        self.mean_time_header.place(relx = 0.26, rely = 0.1)
        self.mean_time_label.place(relx = 0.4, rely = 0.4)
        
    
        mean_avg = results["average"].tail(10).mean()
        if np.isnan(mean_avg):
            mean_avg_text = "N/A"
        else:
            mean_avg_text= convertToReadableTime(mean_avg)
        # DISPLAY AT MOST, THE RECENT 10 AVERAGES
        average_type_text = "Mo3" if self.event in MO3_EVENTS else "Ao5"
        self.mean_avg_container = customtkinter.CTkFrame(self.frame, width = 280, height = 100, fg_color = "transparent", border_color = GREY, border_width = 2)
        self.mean_avg_container.place(relx=0.67, rely = LABEL_Y)
        self.mean_avg_header = customtkinter.CTkLabel(self.mean_avg_container, text = f"Mo{min(10, len(results))}{average_type_text}", font = ("TkDefaultFont", 20))
        self.mean_avg_label = customtkinter.CTkLabel(self.mean_avg_container, text = mean_avg_text, font = ("TkDefaultFont", 17))
        self.mean_avg_header.place(relx = 0.30, rely = 0.1)
        self.mean_avg_label.place(relx = 0.4, rely = 0.4)

            
    def showGraph(self):
        # GET ONLY 50 MOST RECENT SOLVES
        self.graph_container = customtkinter.CTkFrame(self.frame, width = 900, height = 300, fg_color = "transparent", border_color = GREY, border_width = 2)
        self.graph_container.place(relx=0.05, rely = 0.325)
        results = self.data_frame
        time_cols = [f"t{x + 1}" for x in range(self.num_solves)]
        times = results[time_cols].melt()
        NUM_TIMES_TO_DISPLAY = 50
        times = times[times.value != DNF].tail(NUM_TIMES_TO_DISPLAY)


        fig = Figure(figsize = (8.5, 2.5), dpi = 100)
        
        ax = fig.add_subplot(111)
        ax.set_ylabel("Time(s)")
        # turn off tick labels 
        ax.set_xticks([])

        if len(times) != 0:
            times.plot(ax = ax, legend=False)
            #times.plot.line()
        else:
            ax.text(s = "Data not available", fontsize = 15,
                    ha = "center", va = "center", x = 0.5, y = 0.5)
        self.canvas = FigureCanvasTkAgg(fig, master = self.graph_container)
        self.canvas.draw() 
        self.canvas.get_tk_widget().place(relx = 0.01, rely = 0.1)

        

        
        

        num_times = min(NUM_TIMES_TO_DISPLAY, len(times))
        self.results_header = customtkinter.CTkLabel(self.graph_container, text = f"Recent {num_times} Times:",
                                                     font = ("TkDefaultFont", 20))
        self.results_header.place(relx = 0.05, rely = 0.05)



    def displayTopResults(self): 
        results = self.data_frame
        #print(times)
        time_cols = [f"t{x + 1}" for x in range(self.num_solves)]
        times = results[time_cols].melt()
        
        LABEL_X = 0.3
        LABEL_Y = 0.2
        ICON_Y = 0.14 
        ICON_X = 0.05
        TIME_X = 0.73
        TIME_Y = 0.18
        HEADER_X = 0.05 
        HEADER_Y = 0.05
        SIN_CONTAINER_X = 0.05 
        AVG_CONTAINER_X = 0.62
        CONTAINER_Y = 0.65
        ROW_X = 0.075 
        ROW_Y_SHIFT = 0.15
        ICON_SIZE = 25
        CONTAINER_WIDTH = 330 
        CONTAINER_HEIGHT = 300 
        ROW_WIDTH = 275 
        ROW_HEIGHT = 40

        self.top_singles_container = customtkinter.CTkFrame(self.frame, width = CONTAINER_WIDTH, height = CONTAINER_HEIGHT,
                                                            fg_color = "transparent", border_color = GREY, border_width = 2)
        self.top_singles_container.place(relx=SIN_CONTAINER_X, rely=CONTAINER_Y)

        # DISPLAY SINGLES
        self.singles_header = customtkinter.CTkLabel(self.top_singles_container, text = f"Fastest Singles", font = ("TkDefaultFont", 20), anchor = "w")
        self.singles_header.place(relx=HEADER_X, rely=HEADER_Y)
        
        icon_filenames = ["first", "second", "third", "fourth", "fifth"]

        if len(times) == 0:
            label = customtkinter.CTkLabel(self.top_singles_container, text = f"N/A",  font = ("TkDefaultFont", 20),
                                           anchor = "w", justify = "left", width = 130) 
            label.place(relx=LABEL_X, rely = LABEL_Y) 
        else:
            fastest = times["value"].nsmallest(5)
            for i, time in enumerate(fastest):
                row = customtkinter.CTkFrame(self.top_singles_container, width = ROW_WIDTH, height = ROW_HEIGHT, fg_color=LIGHT_GREY)
                row.place(relx = ROW_X, rely = LABEL_Y + ROW_Y_SHIFT * i)
                icon = customtkinter.CTkImage(Image.open(f"icons/{icon_filenames[i]}.png"), size = (ICON_SIZE, ICON_SIZE))
                icon_label = customtkinter.CTkLabel(row, image = icon, text = "")
                icon_label.place(relx=ICON_X, rely=ICON_Y)

                label = customtkinter.CTkLabel(row, text = f"{convertToReadableTime(time)}",  font = ("TkDefaultFont", 20), anchor = "w") 
                label.place(relx=TIME_X, rely = TIME_Y)

        # DISPLAY MEANS
        self.top_means_container = customtkinter.CTkFrame(self.frame, width = CONTAINER_WIDTH, height = CONTAINER_HEIGHT,
                                                           fg_color = "transparent", border_color = GREY, border_width = 2)
        self.top_means_container.place(relx = AVG_CONTAINER_X, rely = CONTAINER_Y)

       
        self.mean_header = customtkinter.CTkLabel(self.top_means_container, text = f"Fastest Averages", font = ("TkDefaultFont", 20), anchor = "w")
        self.mean_header.place(relx=HEADER_X, rely=HEADER_Y)
        
        if len(times) == 0:
            label = customtkinter.CTkLabel(self.top_means_container, text = f"N/A",  font = ("TkDefaultFont", 20),
                                           anchor = "w", justify = "left", width = 130) 
            label.place(relx=LABEL_X, rely = LABEL_Y) 
        else:
            avgs = results["average"]
            fastest = avgs.nsmallest(5)
            for i, time in enumerate(fastest):
                row = customtkinter.CTkFrame(self.top_means_container, width = ROW_WIDTH, height = ROW_HEIGHT, fg_color=LIGHT_GREY)
                row.place(relx = ROW_X, rely = LABEL_Y + ROW_Y_SHIFT * i)
                icon = customtkinter.CTkImage(Image.open(f"icons/{icon_filenames[i]}.png"), size = (ICON_SIZE, ICON_SIZE))
                icon_label = customtkinter.CTkLabel(row, image = icon, text = "")
                icon_label.place(relx=ICON_X, rely=ICON_Y)

                label = customtkinter.CTkLabel(row, text = f"{convertToReadableTime(time)}",  font = ("TkDefaultFont", 20), anchor = "w") 
                label.place(relx=TIME_X, rely = TIME_Y)
        
        
    def changeEventChoice(self, shift):
        curr_event_index = EVENT_NAMES.index(self.event)
        num_events = len(EVENT_NAMES)
        self.event = EVENT_NAMES[(curr_event_index + shift) % num_events]
        self.event_dropdown.set(self.event)


    def toggleSinAvg(self):
        pass
    def processUserKeyInput(self, key):
        if key.keysym == "minus":
            self.switch_frame_func(START)
        elif key.keysym == "Up":
            self.changeEventChoice(-1)
            self.event_dropdown_callback(self.event)
        elif key.keysym == "Down":
            self.changeEventChoice(1)
            self.event_dropdown_callback(self.event)
        elif key.keysym == "D":
            self.clear_data()
