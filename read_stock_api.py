import requests

# https://www.alphavantage.co/documentation/

def read_access_token(file_name):
    with open(file_name, 'r') as file:
        return file.read().strip()

# Read the access token from the text file
access_token = read_access_token('access_token.txt')

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey='+access_token
r = requests.get(url)
data = r.json()

print(data)