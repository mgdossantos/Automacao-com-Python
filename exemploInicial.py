import requests

def printCurrentPrice():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    print(data)

if __name__ == "__main__":
    printCurrentPrice()
