import io

import requests
import matplotlib.pyplot as plt
import tkinter as tk
import numpy as np

from os import mkdir, listdir
from PIL import Image, ImageTk
from form import Form

cwd = "./"
GIT_TRUE = False
root = tk.Tk()
swap = False

if GIT_TRUE:
    import git

def setup(wd="./", branch="main"):
    global cwd
    cwd = wd

    if GIT_TRUE:
        repo = git.Repo(cwd)

        curr_commit = repo.head.commit
        latest_commit = repo.branches[branch].commit

        if curr_commit != latest_commit:
            print("Getting latest updates")
            origin = repo.remote()
            origin.pull()
            print("Restart the program")
            exit(1)

    if not "assets" in listdir(cwd):
        mkdir("assets")

    root.protocol("WM_DELETE_WINDOW", on_closing)

def on_closing():
    exit(1)


def update_conversion(ent1, ent2, convval, *args):
    v = float(ent1.get())
    ent2.delete(0, tk.END)
    ent2.insert(0, f"{v * convval}")

def switchSwap(widgets: list):
    global swap
    swap = not swap

    l = len(widgets) - 1

    for w in widgets:
        r = w.grid_info()["row"]
        w.grid_forget()
        w.grid(row=l-r, column=0)

def update(conv1, conv2, curr_price):

    if conv1.id:
        conv1.trace_remove("write", conv1.id)
    if conv2.id:
        conv2.trace_remove("write", conv2.id)

    if swap:
        conv1.trace_add("write", lambda *args: update_conversion(conv2.entry, conv1.entry, 1/curr_price, *args))
    else:
        conv2.trace_add("write", lambda *args: update_conversion(conv1.entry, conv2.entry, curr_price, *args))

    switchSwap([conv1, conv2])

def get_data(coin, currency="dkk"):
    url = "https://api.coingecko.com/api/v3/coins/markets"

    params = {
        "vs_currency": currency,
        "ids": coin,
        "order": "market_cap_desc",
        "per_page": 1,
        "page": 1,
        "sparkline": "true"
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()[0]
    else:
        return None

def drawPlot(data, currency="dkk"):
    sparkline = data["sparkline_in_7d"]["price"]

    plt.plot(range(0, len(sparkline)), sparkline, label=data["symbol"].upper())

    ticks = np.linspace(0, len(sparkline) - 1, 7, dtype=int)
    tick_names = [str(i) for i in range(7)]


    plt.xlabel("Day")
    plt.xticks(ticks, tick_names)
    plt.ylabel(f"Value in {currency}")
    plt.title(f"7 Day sparkline of {data['id'].capitalize()}")
    plt.legend()
    plt.grid()

def drawGraph(data, root, curr="dkk", w=-1, h=-1):
    if w > 0 and h > 0:
        img = ImageTk.PhotoImage(load_from_buffer().resize((w, h)))
    else:
        img = ImageTk.PhotoImage(load_from_buffer())
        w, h = img.width(), img.height()

    date, time = data["last_updated"].split("T")

    lb = tk.Label(root, image=img, width=w, height=h, borderwidth=7, relief="sunken")
    mark = tk.Label(root, text=f"Last Updated: {time[:8]}")
    title = tk.Label(root, text=f"{data['id'].capitalize()}", pady=15, padx=10, font=("Aptos", 25))
    btn1 = tk.Button(root, text="Analyze!", pady=10, padx=10, font=("Aptos", 15))
    cryp_form = Form(root, "Enter Cryptocurrency", default=data['id'], labelpad=(5, 0), formpad=(5, 0))
    btn2 = tk.Button(root, text="Update", pady=10, padx=10, font=("Aptos", 15), command=lambda: main(cryp_form.get().lower()))

    convFrame = tk.Frame(root)

    curr_price = data["current_price"]

    conv1 = Form(convFrame, f"{data['symbol'].upper()}", default="0", labelpad=(5, 0), formpad=(5, 0))
    conv2 = Form(convFrame, f"{curr.upper()}", default="0", labelpad=(5, 0), formpad=(5, 0))
    swapBtn = tk.Button(convFrame, text="Swap", command=lambda: update(conv1, conv2, curr_price))


    lb.grid(row=1, column=1)
    title.grid(row=0, column=1)
    mark.grid(row=2, column=1, sticky="nw")
    btn1.grid(row=3, column=1, sticky="ne", pady=10)
    btn2.grid(row=3, column=1, sticky="nw", pady=10)
    cryp_form.grid(row=3, column=1, sticky="n", padx=10, pady=10)

    conv1.grid(row=1, column=0, padx=10, pady=(0, 5), sticky="nw")
    conv2.grid(row=0, column=0, padx=10, pady=(5, 0), sticky="nw")
    update(conv1, conv2, curr_price)

    swapBtn.grid(row=3, column=0, padx=10, pady=10)
    convFrame.grid(row=1, column=0, padx=(0, 10))

    root.mainloop()

def load_from_buffer():
    buf = io.BytesIO()
    plt.savefig(buf)
    buf.seek(0)
    return Image.open(buf)

def main(coin="bitcoin", curr="dkk"):
    for child in root.winfo_children():
        child.destroy()
    plt.clf()

    setup()
    data = get_data(coin, "dkk")
    if data:
        print(data)
        drawPlot(data)
        drawGraph(data, root)
    exit(1)

if __name__ == "__main__":
    main()

"""
Why it doesn't work :

>>> crypto_data = get_data(input("enter cryptocurrency> ").lower(), "dkk")[0]
[]
>>> if crypto_data:
        drawData(crypto_data)
List of index out of range
"""