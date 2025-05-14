import requests
import json

# Edit These Flags To Customize the software
KEY="6ohcvqhs11a7"
LOCATION="L3700344"

#Begining of Function Definitions

headers = {'X-eBirdApiToken': KEY}
response = requests.get(f"https://api.ebird.org/v2/data/obs/{LOCATION}/recent", headers=headers)
data = response.text
print(data)