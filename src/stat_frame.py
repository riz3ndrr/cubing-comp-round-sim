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
        self.frame = customtkinter.CTkFrame(root, width = 1000, height = 1000)
        self.header = customtkinter.CTkLabel(self.frame, text = f"Player stats for {event}",
                                             font = ("TkDefaultFont", 40))
        self.event = event
        self.header.place(relx = 0.2, rely = 0.05)
        self.switch_frame_button = customtkinter.CTkButton(master = self.frame, text = "Main Menu",
                                                           command = lambda: switch_frame_func(START))
        self.switch_frame_button.place(relx = 0.8, rely = 0.9)

        filename = DIR1 + event + DIR2
        self.data_frame = pd.read_csv(filename)
                

        ## SWITCH BETWEEN SHOWING SINGLE AND AVERAGE         
        self.showing_sin_avg = customtkinter.StringVar(value = "sin")
        self.switch_sin_avg_widget = customtkinter.CTkSwitch(self.frame, text = "Showing Best Singles",
                                                        command = self.toggleTopResults,
                                                        variable = self.showing_sin_avg, onvalue = "sin", offvalue ="avg",
                                                        switch_width = 60, switch_height = 30)
        
        self.switch_sin_avg_widget.place(relx = 0.65, rely = 0.8)
        self.results_header = customtkinter.CTkLabel(self.frame, text = "Recent 50 Times:",
                                                     font = ("TkDefaultFont", 25))
        self.results_header.place(relx = 0.1, rely = 0.425)
        self.top_result_container = customtkinter.CTkFrame(self.frame, width = 300, height = 500)

       

        ## DISPLAY TIMES 
        self.displayTopResults()
        self.showGraph()

    def toggleTopResults(self):
        if self.showing_sin_avg.get() == "sin":
            self.switch_sin_avg_widget.configure(text = "Showing Best Singles")
        else:
            self.switch_sin_avg_widget.configure(text = "Showing Best Averages")
        self.displayTopResults()
        
            
    def showGraph(self):
        # GET ONLY 50 MOST RECENT SOLVES
        results = self.data_frame.iloc[:-2]
        time_cols = [c for c in self.data_frame.columns if c.startswith("t")]
        times = results[time_cols].melt()
        times = times.tail(50)

        fig = Figure(figsize = (5,4), dpi = 100) 
        ax = fig.add_subplot(111)
        ax.set_ylabel("Times")
        # turn off tick labels 
        ax.set_xticks([])
        times.plot(ax = ax, legend=False)
        canvas = FigureCanvasTkAgg(fig, master = self.frame)
        canvas.draw() 
        canvas.get_tk_widget().place(relx = 0.1, rely = 0.5)

        times.plot.line()



    def displayTopResults(self): 
        # CLEAR CHILDREN 
        for child in self.top_result_container.winfo_children():
            child.destroy()
        summary1 =self.data_frame.iloc[-2]
        summary2 =self.data_frame.iloc[-1]
        results = self.data_frame.iloc[:-2]
        
        #print(times)
        if self.showing_sin_avg.get() == "sin":
            time_cols = [c for c in self.data_frame.columns if c.startswith("t")]
            times = results[time_cols].melt()
            fastest = times["value"].nsmallest(5)
            header_txt = "Singles"
        else: 
            avgs = results["average"]
            fastest = avgs.nsmallest(5)
            header_txt = "Averages"

        self.result_header = customtkinter.CTkLabel(self.top_result_container, text = f"Fastest {header_txt}", font = ("TkDefaultFont", 30),
                                                    width = 300)
        self.result_header.pack()
        for i, time in enumerate(fastest):
            label = customtkinter.CTkLabel(self.top_result_container, text = f"{i + 1}: {time}",  font = ("TkDefaultFont", 25),
                                           anchor = "w", justify = "left", width = 130) 
            label.pack() 
        self.top_result_container.place(relx = 0.65, rely = 0.5)
        
        
    def toggleSinAvg(self):
        pass
    def processUserKeyInput(self, key):
        pass
