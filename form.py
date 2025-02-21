import tkinter as tk

class Form(tk.Frame):
    def __init__(self, root, labelText, default="", labelpad=(0, 0), formpad=(0, 0), *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)

        self.default = tk.StringVar(self, default)
        self.label = tk.Label(self, text=labelText, font=("Aptos", 15))
        self.entry = tk.Entry(self, bd=3, textvariable=self.default)

        self.label.pack(side="left", padx=labelpad[0], pady=labelpad[1])
        self.entry.pack(side="right", padx=formpad[0], pady=formpad[1])
        self.id = None

    def trace_add(self, *args, **kwargs):
        self.id = self.default.trace_add(*args, **kwargs)

    def trace_remove(self, *args, **kwargs):
        self.default.trace_remove(*args, **kwargs)
        self.id = None

    def get(self):
        return self.entry.get()