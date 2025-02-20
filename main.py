import requests
import matplotlib.pyplot as plt

from tkinter import *
from os import mkdir, listdir

cwd = "./"
GIT_TRUE = True

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

def drawData(data, currency="dkk"):
    sparkline = data["sparkline_in_7d"]['price']

    plt.plot(range(0, len(sparkline)), sparkline, label=data["symbol"])

    plt.xlabel("Day")
    plt.ylabel(f"Value in {currency}")
    plt.title(f"7 Day sparkline of {data['id'].capitalize()}")
    plt.legend()
    plt.grid()

if __name__ == "__main__":
    setup()
    data = get_data(input("enter cryptocurrency> ").lower(), "dkk")
    if data:
        drawData(data)
        plt.savefig(f"assets/{data['symbol']}.png")

"""
Why it doesn't work :

>>> crypto_data = get_data(input("enter cryptocurrency> ").lower(), "dkk")[0]
[]
>>> if crypto_data:
        drawData(crypto_data)
List of index out of range
"""