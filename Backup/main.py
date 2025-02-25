import tkinter as tk
from model import Model
from view import View
from controller import Controller

if __name__ == "__main__":
    root = tk.Tk()
    model = Model()
    view = View(root, None)
    controller = Controller(model, view)
    view.controller = controller
    controller.main()
    root.mainloop()

"""
Why it doesn't work :

>>> crypto_data = get_data(input("enter cryptocurrency> ").lower(), "dkk")[0]
[]
>>> if crypto_data:
        drawData(crypto_data)
List of index out of range
"""