from flask import Flask, render_template
import requests
import wikipedia

# Edit These Flags To Customize the software
PORT = 1991
HOST = "0.0.0.0"
KEY = "6ohcvqhs11a7"
LOCATION = "L3700344"
AMOUNT_OF_BIRDS=10

def get_bird_image_url(sci_name):
    manual_image_overrides = {
    "Milvus milvus": "https://images.stockcake.com/public/1/1/e/11e71e9c-d454-4102-9526-6011f1a92308_medium/majestic-soaring-eagle-stockcake.jpg",
    "Buteo buteo" : "https://cdn.openart.ai/published/gfDssGha4jNjVWozyeak/bizG1roP_Dtrc_256.webp",
    "Phasianus colchicus" : "https://cdn.neighbourly.co.nz/images/cache/message_image_thumbnail/message_images/626857575e9081.13864759.jpeg?170410"
    }

    
    print(sci_name)
    if sci_name in manual_image_overrides:
        print("Overide Engaged")
        return manual_image_overrides[sci_name]
    
    try:
        page = wikipedia.page(sci_name)
        for img in page.images:
            url = img.lower()
            if (
                any(url.endswith(ext) for ext in ['.jpg', '.jpeg', '.png']) and
                'map' not in url and
                'distribution' not in url and
                'range' not in url and
                'logo' not in url and
                'icon' not in url and
                'symbol' not in url and
                'flag' not in url and
                'coat_of_arms' not in url
            ):
                return img
    except Exception as e:
        print(f"Image lookup failed for {sci_name}: {e}")
    
    # fallback image if no valid photo found
    return "https://upload.wikimedia.org/wikipedia/commons/thumb/4/42/Question_mark_%28black%29.svg/1200px-Question_mark_%28black%29.svg.png"



# Function to fetch data
def fetchData():
    headers = {'X-eBirdApiToken': KEY}
    response = requests.get(f"https://api.ebird.org/v2/data/obs/{LOCATION}/recent", headers=headers)
    response.raise_for_status()
    data = response.json()
    
    # Add image URLs
    for obs in data[:AMOUNT_OF_BIRDS]:
        obs['image_url'] = get_bird_image_url(obs['sciName'])
    
    return data

# Initialize Flask app
print("Initializing Web Server")
app = Flask(__name__)


@app.route("/")
def main():
    observations = fetchData()
    return render_template('index.html', observations=observations[:AMOUNT_OF_BIRDS])

if __name__ == "__main__":
    app.run(port=PORT, host=HOST)
