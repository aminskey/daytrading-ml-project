import tkinter as tk
import asyncio

from PIL import ImageTk
from form import Form

class View:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.curr_price = 0
        self.form_lbl = ""
        self.conv_lbl = ""

    def update(self, conv1, conv2, curr_price, *args):
        """
        if conv1.id:
            conv1.trace_remove("write", conv1.id)
        if self.controller.swap:
            conv1.trace_add("write",
                            lambda *args: self.update_conversion(conv2.entry, conv1.entry, 1 / curr_price, *args))
        self.switchSwap([conv1, conv2])
        """

        inp = conv1.get()
        if inp.isdigit():
            conv2.config(text=f"{self.conv_lbl}: {int(inp) * curr_price}")
        else:
            conv2.config(text=f"{self.conv_lbl}: 0")


    def switchSwap(self, form, label):  # added self
        self.curr_price = 1/self.curr_price
        self.form_lbl, self.conv_lbl = self.conv_lbl, self.form_lbl
        form.label.config(text=self.form_lbl)
        label.config(text=self.conv_lbl)


    def drawUI(self, data, root, w=-1, h=-1):
        if w > 0 and h > 0:
            img = ImageTk.PhotoImage(self.controller.model.load_from_buffer().resize((w, h)))
        else:
            img = ImageTk.PhotoImage(self.controller.model.load_from_buffer())
            w, h = img.width(), img.height()

        date, time = data["last_updated"].split("T")

        title = tk.Label(root, text=f"{data['id'].capitalize()}", pady=7, padx=10, font=("Aptos", 25))
        lb = tk.Label(root, image=img, width=w, height=h, borderwidth=7, relief="sunken")
        mark = tk.Label(root, text=f"Last Updated: {time[:8]}")

        convFrame = tk.Frame(root)
        formFrame = tk.Frame(root)

        self.curr_price = data["current_price"]
        swapBtn = tk.Button(convFrame, text="Swap", command=lambda: self.switchSwap(conv_form, conv_label))  # command=lambda: self.update(conv1, conv2, curr_price)

        self.conv_lbl = f"{self.controller.curr.upper()}"
        self.form_lbl = f"{data['symbol'].upper()}"

        conv_form = Form(convFrame, f"{data['symbol'].upper()}", default=0, labelpad=(5, 0), formpad=(5, 0))
        conv_label = tk.Label(convFrame, text=f"{self.controller.curr.upper()}: 0", font=("Aptos", 15))
        conv_form.trace_add("write", lambda *args: self.update(conv_form, conv_label, self.curr_price, self.controller.curr, *args))


        cryp_form = Form(formFrame, "Enter Cryptocurrency", default=data['id'], labelpad=(5, 0), formpad=(5, 0))
        curr_form = Form(formFrame, "Enter Target Currency", default=self.controller.curr, labelpad=(5, 0), formpad=(5, 0))

        btn = tk.Button(root, text="Update", pady=10, padx=10, font=("Aptos", 15), command=lambda: self.controller.main(cryp_form.get().lower(), curr_form.get().lower()))

        cryp_form.grid(row=0, column=1)
        curr_form.grid(row=1, column=1)

        lb.grid(row=1, column=1)
        title.grid(row=0, column=1)
        mark.grid(row=2, column=1, sticky="nw")
        btn.grid(row=3, column=1, sticky="nw", pady=10)
        formFrame.grid(row=3, column=1, sticky="n", padx=10, pady=10)

        conv_form.grid(row=1, column=0, pady=(0, 5), sticky="nw")
        conv_label.grid(row=2, column=0, padx=(5, 0), pady=(5, 0), sticky="nw")
        swapBtn.grid(row=3, column=0, padx=10, pady=10)
        convFrame.grid(row=1, column=0, padx=(0, 10))

        root.mainloop()