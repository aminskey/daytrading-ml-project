import requests
import matplotlib.pyplot as plt

from tkinter import *

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
        return response.json()
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
    plt.show()

btc_data = get_data("bitcoin", "dkk")[0]
print(btc_data)
drawData(btc_data)