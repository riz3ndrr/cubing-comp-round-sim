import customtkinter
import csv
import pandas as pd
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from constants import GAME, START, STAT

DIR1 = '../data/'
DIR2 = '.csv'
DNF = 999


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
        self.header = customtkinter.CTkLabel(self.frame, text = f"Player stats for {event}",
                                             font = ("TkDefaultFont", 40))
        self.event = event
        self.event_dropdown = customtkinter.CTkOptionMenu(self.frame, values = EVENT_NAMES,
                                                          command = self.event_dropdown_callback)
        self.event_dropdown.set(event)
        self.event_dropdown.place(relx = 0.8, rely = 0.1)

        self.header.place(relx = 0.2, rely = 0.05)
        self.switch_frame_button = customtkinter.CTkButton(master = self.frame, text = "Main Menu",
                                                           command = lambda: switch_frame_func(START),
                                                           width = 200, height = 50,
                                                           font = ("TkDefaultFont", 20))
        self.switch_frame_button.place(relx = 0.75, rely = 0.95)
        self.initDataFrame()
        self.showGraph()
        

        self.top_result_container = customtkinter.CTkFrame(self.frame, width = 300, height = 500,
                                                           fg_color = "transparent")
        self.top_result_container.place(relx = 0.6, rely = 0.4)

        self.showSummaryStats() 

        ## DISPLAY TIMES 
        self.displayTopResults()
        print(self.data_frame)
    def initDataFrame(self):
        filename = DIR1 + self.event + DIR2
        try:
            self.data_frame = pd.read_csv(filename)
        except FileNotFoundError:
            print("AHH")
            default_data = [
                ["t1", "t2", "t3", "t4", "t5", "average", "placing", "num_ppl"],
            ]
            with open(filename, 'w', newline='') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerows(default_data)
            self.data_frame = pd.read_csv(filename)


    def event_dropdown_callback(self, new_event):
        self.event = new_event
        self.resetStats()
        self.showGraph()
        self.showSummaryStats()
        self.displayTopResults()
        self.header.configure(text = f"Player stats for {self.event}")
    
    def resetStats(self):
        self.initDataFrame()
        stat_widgets = [self.placing_header, self.placing_label,
                       self.mean_time_header, self.mean_time_label,
                       self.mean_avg_header, self.mean_avg_label,
                       self.canvas.get_tk_widget()]
        for w in stat_widgets:
            w.place_forget()

        
        for child in self.top_result_container.winfo_children():
            child.destroy()
                

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

        # PLACING RESULTS
        placing_results = results[["placing", "num_ppl"]].mean()
        if np.isnan(placing_results["placing"]):
            placing_text = "N/A"
        else:
            avg_placing = round(placing_results["placing"])
            avg_num_ppl = round(placing_results["num_ppl"]) 
            placing_text = f"{avg_placing}{self.genSuffix(avg_placing)} out of {avg_num_ppl} people" 
        LABEL_Y = 0.20
        self.placing_header = customtkinter.CTkLabel(self.frame, text = "Average Placing", font = ("TkDefaultFont", 30))
        self.placing_label = customtkinter.CTkLabel(self.frame, text = placing_text, font = ("TkDefaultFont", 25))
        self.placing_header.place(relx = 0.1, rely = LABEL_Y) 
        self.placing_label.place(relx = 0.125, rely = LABEL_Y + 0.05)

        # MEAN RESULTS
        time_cols = ["t1", "t2", "t3", "t4", "t5"]
        times = (results[time_cols].melt())
        times = times[times.value != DNF]
        mean_time = times["value"].mean()
        if np.isnan(mean_time):
            mean_sin_text = "N/A"
        else:
            mean_sin_text = f"{mean_time:.2f}"
        self.mean_time_header = customtkinter.CTkLabel(self.frame, text = "Average Time", font = ("TkDefaultFont", 30))
        self.mean_time_label = customtkinter.CTkLabel(self.frame, text = mean_sin_text, font = ("TkDefaultFont", 25))
        self.mean_time_header.place(relx = 0.1 + 0.30, rely = LABEL_Y)
        self.mean_time_label.place(relx = 0.125 + 0.30, rely = LABEL_Y + 0.05)
        
    
        mean_avg = results["average"].tail(10).mean()
        if np.isnan(mean_avg):
            mean_avg_text = "N/A"
        else:
            mean_avg_text= f"{mean_avg:.2f}"
        # DISPLAY AT MOST, THE RECENT 10 AVERAGES
        self.mean_avg_header = customtkinter.CTkLabel(self.frame, text = f"Mo{min(10, len(results))}Ao5", font = ("TkDefaultFont", 30))
        self.mean_avg_label = customtkinter.CTkLabel(self.frame, text = mean_avg_text, font = ("TkDefaultFont", 25))
        self.mean_avg_header.place(relx = 0.1 + 0.55, rely = LABEL_Y)
        self.mean_avg_label.place(relx = 0.125 + 0.55, rely = LABEL_Y + 0.05)

            
    def showGraph(self):
        # GET ONLY 50 MOST RECENT SOLVES
        results = self.data_frame
        time_cols = ["t1", "t2", "t3", "t4", "t5"]
        times = results[time_cols].melt()
        NUM_TIMES_TO_DISPLAY = 50
        times = times[times.value != DNF].tail(NUM_TIMES_TO_DISPLAY)

        fig = Figure(figsize = (5,4), dpi = 100) 
        ax = fig.add_subplot(111)
        ax.set_ylabel("Times")
        # turn off tick labels 
        ax.set_xticks([])

        if len(times) != 0:
            times.plot(ax = ax, legend=False)
            #times.plot.line()
        else:
            ax.text(s = "Data not available", fontsize = 15,
                    ha = "center", va = "center", x = 0.5, y = 0.5)
        self.canvas = FigureCanvasTkAgg(fig, master = self.frame)
        self.canvas.draw() 
        self.canvas.get_tk_widget().place(relx = 0.1, rely = 0.4)

        

        num_times = min(NUM_TIMES_TO_DISPLAY, len(times))
        self.results_header = customtkinter.CTkLabel(self.frame, text = f"Recent {num_times} Times:",
                                                     font = ("TkDefaultFont", 30))
        self.results_header.place(relx = 0.15, rely = 0.40)



    def displayTopResults(self): 
        # CLEAR CHILDREN 
        results = self.data_frame
        
        #print(times)
        time_cols =["t1", "t2", "t3", "t4", "t5"]
        times = results[time_cols].melt()

        self.singles_header = customtkinter.CTkLabel(self.top_result_container, text = f"Fastest Singles", font = ("TkDefaultFont", 30),
                                                    width = 300)
        self.singles_header.pack()

        if len(times) == 0:
            label = customtkinter.CTkLabel(self.top_result_container, text = f"N/A",  font = ("TkDefaultFont", 25),
                                           anchor = "w", justify = "left", width = 130) 
            label.pack() 
        else:
            fastest = times["value"].nsmallest(5)
            for i, time in enumerate(fastest):
                label = customtkinter.CTkLabel(self.top_result_container, text = f"{i + 1}: {time:.2f}",  font = ("TkDefaultFont", 25),
                                            anchor = "w", justify = "left", width = 130) 
                label.pack() 

        self.mean_header = customtkinter.CTkLabel(self.top_result_container, text = f"Fastest Averages", font = ("TkDefaultFont", 30),
                                                    width = 300)
        self.mean_header.pack()
        if len(times) == 0:
            label = customtkinter.CTkLabel(self.top_result_container, text = f"N/A",  font = ("TkDefaultFont", 25),
                                           anchor = "w", justify = "left", width = 130) 
            label.pack() 
        else:
            avgs = results["average"]
            fastest = avgs.nsmallest(5)
            for i, time in enumerate(fastest):
                label = customtkinter.CTkLabel(self.top_result_container, text = f"{i + 1}: {time:.2f}",  font = ("TkDefaultFont", 25),
                                            anchor = "w", justify = "left", width = 130) 
                label.pack() 
        
        
        
        
    def toggleSinAvg(self):
        pass
    def processUserKeyInput(self, key):
        pass
