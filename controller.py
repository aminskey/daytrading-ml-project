import matplotlib.pyplot as plt
import tkinter as tk
import git
from os import mkdir, listdir
from variables import *

class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.swap = False
        self.wd = "."
        
    def main(self, coin="bitcoin", curr="dkk"):
        for child in self.view.root.winfo_children():
            child.destroy()
        plt.clf()

        self.setup()
        data = self.model.get_data(coin, curr)

        if data:
            self.model.drawPlot(data, curr)
            self.view.drawUI(data, self.view.root, curr)
        exit(1)
    
    def setup(self, wd="."):

        self.wd = wd

        if not "assets" in listdir(self.wd):
            mkdir("assets")

        self.view.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def on_closing(self):
        exit(1)
    
    def update_conversion(self, ent1, ent2, convval, *args):
        v = float(ent1.get())
        ent2.delete(0, tk.END)
        ent2.insert(0, f"{v * convval}")
        
    def update(self, conv1, conv2, curr_price):
        if conv1.id:
            conv1.trace_remove("write", conv1.id)
        if conv2.id:
            conv2.trace_remove("write", conv2.id)
        if self.swap:
            conv1.trace_add("write", lambda *args: self.update_conversion(conv2.entry, conv1.entry, 1/curr_price, *args))
        else:
            conv2.trace_add("write", lambda *args: self.update_conversion(conv1.entry, conv2.entry, curr_price, *args))
        self.switchSwap([conv1, conv2])
    
    def switchSwap(self, widgets: list): # added self
        self.swap = not self.swap
        l = len(widgets) - 1
        for w in widgets:
            r = w.grid_info()["row"]
            w.grid_forget()
            w.grid(row=l-r, column=0)