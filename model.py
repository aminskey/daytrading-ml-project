import requests
import matplotlib.pyplot as plt
import numpy as np
import io
import json

from PIL import Image

class Model:
    def __init__(self):
        self.controller = None

        with open("codes.json", "r") as f:
            self.err_codes = json.load(f)
            f.close()

    def get_data(self, coin, currency="dkk"):
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
            data = response.json()
            return data[0] if len(data) > 0 else dict(error="Error Code: -1", subtitle="Couldn't retrieve any information...")

        return dict(error=f"Error Code: {response.status_code}, {self.err_codes[str(response.status_code)]['message']}", subtitle=self.err_codes[str(response.status_code)]['description'])
    def drawPlot(self, data, currency="dkk"):
        sparkline = data["sparkline_in_7d"]["price"]
        usd_val = sparkline[-1]
        cus_val = data["current_price"]

        coeff = cus_val/usd_val
        sparkline = [i*coeff for i in sparkline]

        plt.plot(range(0, len(sparkline)), sparkline, label=data["symbol"].upper())

        ticks = np.linspace(0, len(sparkline) - 1, 7, dtype=int)
        tick_names = [str(i) for i in range(7)]

        plt.xlabel("Day")
        plt.xticks(ticks, tick_names)
        plt.ylabel(f"Value in {currency}")
        plt.title(f"7 Day sparkline of {data['id'].capitalize()}")
        plt.legend()
        plt.grid()
        
    def load_from_buffer(self):
        buf = io.BytesIO()
        plt.savefig(buf)
        buf.seek(0)
        return Image.open(buf)