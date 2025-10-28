import customtkinter


from pprint import pprint

from player import Player, UserPlayer, GennedPlayer
from game_frame import PlayerGameRow, GameFrame
from start_frame import StartFrame, PlayerRowLabel

import csv



customtkinter.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("themes/cherry.json")  # Modes: system (default), light, dark


DNF = 999



class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1000x1000")

        self.startFrame = StartFrame(self, self.switchFrame, '../players.csv')
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
            self.gameFrame = GameFrame(self, self.players, self.switchFrame, self.startFrame.event)
            self.gameFrame.frame.pack(expand = True)
            self.currFrame = self.gameFrame

        elif isinstance(self.currFrame, GameFrame):
            #self.bind('<Key>', self.startFrame.recvUserKeyInput)
            self.gameFrame.frame.pack_forget()
            self.startFrame.frame.pack(expand = True)
            self.currFrame = self.startFrame

        self.startFrame.clearEntryText()
        self.bind('<Key>', self.currFrame.processUserKeyInput)

    def helper_func(self, key):
        self.currFrame.processUserKeyInput()

if __name__ == "__main__":
    app = App()
    app.mainloop()
