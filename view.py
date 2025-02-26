import tkinter as tk
from PIL import ImageTk
from form import Form

class View:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller

    def drawUI(self, data, root, curr="dkk", w=-1, h=-1):
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

        curr_price = data["current_price"]

        conv1 = Form(convFrame, f"{data['symbol'].upper()}", default="0", labelpad=(5, 0), formpad=(5, 0))
        conv2 = Form(convFrame, f"{curr.upper()}", default="0", labelpad=(5, 0), formpad=(5, 0))
        swapBtn = tk.Button(convFrame, text="Swap", command=lambda: self.controller.update(conv1, conv2, curr_price))

        cryp_form = Form(formFrame, "Enter Cryptocurrency", default=data['id'], labelpad=(5, 0), formpad=(5, 0))
        curr_form = Form(formFrame, "Enter Target Currency", default=curr, labelpad=(5, 0), formpad=(5, 0))

        btn = tk.Button(root, text="Update", pady=10, padx=10, font=("Aptos", 15), command=lambda: self.controller.main(cryp_form.get().lower(), curr_form.get().lower()))

        cryp_form.grid(row=0, column=1)
        curr_form.grid(row=1, column=1)

        lb.grid(row=1, column=1)
        title.grid(row=0, column=1)
        mark.grid(row=2, column=1, sticky="nw")
        btn.grid(row=3, column=1, sticky="nw", pady=10)
        formFrame.grid(row=3, column=1, sticky="n", padx=10, pady=10)

        conv1.grid(row=1, column=0, padx=10, pady=(0, 5), sticky="nw")
        conv2.grid(row=0, column=0, padx=10, pady=(5, 0), sticky="nw")
        self.controller.update(conv1, conv2, curr_price)

        swapBtn.grid(row=3, column=0, padx=10, pady=10)
        convFrame.grid(row=1, column=0, padx=(0, 10))

        root.mainloop()