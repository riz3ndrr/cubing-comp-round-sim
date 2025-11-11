import customtkinter
import csv
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
START = 'start'
DIR1 = '../data/'
DIR2 = '.csv'

class StatFrame():
    def __init__(self, root, switch_frame_func, event):
        self.frame = customtkinter.CTkFrame(root, width = 1000, height = 1000, fg_color = "white")
        self.header = customtkinter.CTkLabel(self.frame, text = f"Player stats for {event}",
                                             font = ("TkDefaultFont", 40))
        self.event = event
        self.header.place(relx = 0.2, rely = 0.05)
        self.switch_frame_button = customtkinter.CTkButton(master = self.frame, text = "Main Menu",
                                                           command = lambda: switch_frame_func(START),
                                                           width = 200, height = 50,
                                                           font = ("TkDefaultFont", 20))
        self.switch_frame_button.place(relx = 0.75, rely = 0.95)

        filename = DIR1 + event + DIR2
        try:
            self.data_frame = pd.read_csv(filename)
        except FileNotFoundError:
            default_data = [
                ["t1", "t2", "t3", "t4", "t5", "average", "placing", "num_ppl"],
                [1.1, 1.2, 1.3, 1.4, 1.5, None, 1, 5],
                [2, 2, 2, 2, 2, 2, 2, 2]
            ]
            with open(filename, 'w', newline='') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerows(default_data)
            self.data_frame = pd.read_csv(filename)

        self.showGraph()
        

        self.top_result_container = customtkinter.CTkFrame(self.frame, width = 300, height = 500,
                                                           fg_color = "transparent")
        self.top_result_container.place(relx = 0.6, rely = 0.4)

        self.showSummaryStats() 

        ## DISPLAY TIMES 
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
        results = self.data_frame.iloc[:-2]

        # PLACING RESULTS
        placing_results = results[["placing", "num_ppl"]].mean()
        avg_placing = round(placing_results["placing"])
        avg_num_ppl = round(placing_results["num_ppl"]) 
        
        self.placing_header = customtkinter.CTkLabel(self.frame, text = "Average Placing", font = ("TkDefaultFont", 30))
        self.placing_label = customtkinter.CTkLabel(self.frame, text = f"{avg_placing}{self.genSuffix(avg_placing)} out of {avg_num_ppl} people", font = ("TkDefaultFont", 25))
        self.placing_header.place(relx = 0.1, rely = 0.125)
        self.placing_label.place(relx = 0.125, rely = 0.175)

        # MEAN RESULTS
        time_cols = ["t1", "t2", "t3", "t4", "t5"]
        mean_time = results[time_cols].melt()["value"].mean() 
        self.mean_time_header = customtkinter.CTkLabel(self.frame, text = "Average Time", font = ("TkDefaultFont", 30))
        self.mean_time_label = customtkinter.CTkLabel(self.frame, text = f"{mean_time:.2f}s", font = ("TkDefaultFont", 25))
        self.mean_time_header.place(relx = 0.1 + 0.30, rely = 0.125)
        self.mean_time_label.place(relx = 0.125 + 0.30, rely = 0.175)
        

        mean_avg = results["average"].tail(10).mean()
        self.mean_avg_header = customtkinter.CTkLabel(self.frame, text = f"Mo{min(10, len(results))}Ao5", font = ("TkDefaultFont", 30))
        self.mean_avg_label = customtkinter.CTkLabel(self.frame, text = f"{mean_avg:.2f}s", font = ("TkDefaultFont", 25))
        self.mean_avg_header.place(relx = 0.1 + 0.55, rely = 0.125)
        self.mean_avg_label.place(relx = 0.125 + 0.55, rely = 0.175)

            
    def showGraph(self):
        # GET ONLY 50 MOST RECENT SOLVES
        results = self.data_frame.iloc[:-2]
        time_cols = ["t1", "t2", "t3", "t4", "t5"]
        times = results[time_cols].melt()
        NUM_TIMES_TO_DISPLAY = 50
        times = times.tail(NUM_TIMES_TO_DISPLAY)

        fig = Figure(figsize = (5,4), dpi = 100) 
        ax = fig.add_subplot(111)
        ax.set_ylabel("Times")
        # turn off tick labels 
        ax.set_xticks([])
        times.plot(ax = ax, legend=False)
        canvas = FigureCanvasTkAgg(fig, master = self.frame)
        canvas.draw() 
        canvas.get_tk_widget().place(relx = 0.1, rely = 0.4)

        times.plot.line()

        num_times = min(NUM_TIMES_TO_DISPLAY, len(times))
        self.results_header = customtkinter.CTkLabel(self.frame, text = f"Recent {num_times} Times:",
                                                     font = ("TkDefaultFont", 30))
        self.results_header.place(relx = 0.15, rely = 0.375)



    def displayTopResults(self): 
        # CLEAR CHILDREN 
        for child in self.top_result_container.winfo_children():
            child.destroy()
        summary1 =self.data_frame.iloc[-2]
        summary2 =self.data_frame.iloc[-1]
        results = self.data_frame.iloc[:-2]
        
        #print(times)
        time_cols =["t1", "t2", "t3", "t4", "t5"]
        times = results[time_cols].melt()
        fastest = times["value"].nsmallest(5)
        self.singles_header = customtkinter.CTkLabel(self.top_result_container, text = f"Fastest Singles", font = ("TkDefaultFont", 30),
                                                    width = 300)
        self.singles_header.pack()
        for i, time in enumerate(fastest):
            label = customtkinter.CTkLabel(self.top_result_container, text = f"{i + 1}: {time}",  font = ("TkDefaultFont", 25),
                                           anchor = "w", justify = "left", width = 130) 
            label.pack() 

        self.mean_header = customtkinter.CTkLabel(self.top_result_container, text = f"Fastest Averages", font = ("TkDefaultFont", 30),
                                                    width = 300)
        self.mean_header.pack()
        avgs = results["average"]
        fastest = avgs.nsmallest(5)
        for i, time in enumerate(fastest):
            label = customtkinter.CTkLabel(self.top_result_container, text = f"{i + 1}: {time}",  font = ("TkDefaultFont", 25),
                                           anchor = "w", justify = "left", width = 130) 
            label.pack() 

        
        
        
    def toggleSinAvg(self):
        pass
    def processUserKeyInput(self, key):
        pass
