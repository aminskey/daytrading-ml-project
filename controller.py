import matplotlib.pyplot as plt
import tkinter as tk

from os import mkdir, listdir
from time import sleep

class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.swap = False
        self.wd = "."
        self.curr = "dkk"
        
    def main(self, coin="bitcoin", curr="dkk"):
        self.curr = curr
        for child in self.view.root.winfo_children():
            child.destroy()
        plt.clf()

        self.setup()

        data = self.model.get_data(coin, self.curr)
        print(data)

        if "id" in data.keys():
            self.model.drawPlot(data)
            self.view.drawUI(data)
        elif "error" in data.keys():
            self.view.bluescreen(data["error"], data["subtitle"])
            self.view.root.mainloop()
        exit(1)
    
    def setup(self, wd="."):
        self.wd = wd
        self.view.root.configure(bg=self.view.stdbg)
        self.view.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def on_closing(self):
        exit(1)
