import matplotlib.pyplot as plt
import tkinter as tk

from os import mkdir, listdir

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

        if data:
            self.model.drawPlot(data)
            self.view.drawUI(data, self.view.root)
        exit(1)
    
    def setup(self, wd="."):

        self.wd = wd

        if not "assets" in listdir(self.wd):
            mkdir("assets")

        self.view.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def on_closing(self):
        exit(1)
