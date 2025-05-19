from flask import Flask, render_template
import requests
import wikipedia
import time

# Edit These Flags To Customize the software
PORT = 1991
HOST = "0.0.0.0"
KEY = "6ohcvqhs11a7"
LOCATION = "L3700344"
AMOUNT_OF_BIRDS=12
print(">> Starting Software with The Following Argurments")
print(">> PORT: ", PORT)
print(">> HOST:", HOST)
print(">> KEY: ", KEY)
print(">> LOCATION: ", LOCATION)
print(">> Amount of Birds to Display: ", AMOUNT_OF_BIRDS)

def log_missing_img(sci_name):
    line = f"[Missing image: {sci_name}\n" 
    with open("MISSING_IMAGE_LOG.txt", "a") as f:
        f.write(line)
        f.close()
    priint("r")
def get_bird_image_url(sci_name):
    print(">> Checking For Manual Image Overide")
    manual_image_overrides = {
    "Milvus milvus": "https://images.stockcake.com/public/1/1/e/11e71e9c-d454-4102-9526-6011f1a92308_medium/majestic-soaring-eagle-stockcake.jpg",
    "Buteo buteo" : "https://cdn.openart.ai/published/gfDssGha4jNjVWozyeak/bizG1roP_Dtrc_256.webp",
    "Phasianus colchicus" : "https://cdn.neighbourly.co.nz/images/cache/message_image_thumbnail/message_images/626857575e9081.13864759.jpeg?170410",
    "Anthus pratensis": "https://th.bing.com/th/id/R.295b7daaa42792951d05a6b7da3a4573?rik=qzVHphcXNhp5OA&riu=http%3a%2f%2fwww.naturephoto-cz.com%2fphotos%2fbirds%2fanthus-pratensis-39724.jpg&ehk=SlJKj3z6grLHRdpznIDlz%2bI24%2fGfYvCybL3YCdhF93g%3d&risl=&pid=ImgRaw&r=0&sres=1&sresct=1",
    "Sylvia atricapilla": "https://media.istockphoto.com/id/174837709/photo/eurasian-blackcap.jpg?s=612x612&w=0&k=20&c=3kUxdWcOQ8Xj41Q4HEKzxhQPsrkxrAYWc8XupMm_O6g=",
    "Ardea cinerea" : "https://northkent.birdwise.org.uk/wp-content/uploads/2020/05/Grey-heron-800.jpg",
    "Pica pica" : "https://static.inaturalist.org/photos/256224620/large.jpg",
    "Chroicocephalus ridibundus" : "https://www.first-nature.com/algbirds/birdpics/chroicocephalus-ridibundus1.jpg"
    }

    
    if sci_name in manual_image_overrides:
        print(">> Image Overide Engaged For: ",sci_name)
        return manual_image_overrides[sci_name]
    else:
        try:
            print(">> Trying Wikipediea Image Base")
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
                    print(">> Image Found on Wikipedia For ", sci_name)
                    return img
        except Exception as e:
            print(f">> Image lookup failed for {sci_name}: {e}")
            log_missing_img(sci_name)
            print(">> Missing Image Reported")
            return "https://upload.wikimedia.org/wikipedia/commons/thumb/4/42/Question_mark_%28black%29.svg/1200px-Question_mark_%28black%29.svg.png"

# Function to fetch data
def fetchData():
    print(">> Making API Request With Location: ", LOCATION)
    headers = {'X-eBirdApiToken': KEY}
    response = requests.get(f"https://api.ebird.org/v2/data/obs/{LOCATION}/recent", headers=headers)
    response.raise_for_status()
    data = response.json()
    
    print(">> Getting Images...")
    # Add image URLs
    for obs in data[:AMOUNT_OF_BIRDS]:
        try:
            obs['image_url'] = get_bird_image_url(obs['sciName'])
        except:
            print(">> A Bird Requires Manual Image Overide: ", obs['sciName'])
    print(">> Data Fetch Complete")   
    return data
def getTime():
    now = time.strftime("%H:%M:%S", time.localtime())
    print(">> Refresh Time: ", now)
    return now
# Initialize Flask app
print(">> Initializing Flask Web Server")
app = Flask(__name__)


@app.route("/")
def main():
    print(">> Page Requested")
    observations = fetchData()
    current_time = getTime()
    print(">> Rendering Page")
    return render_template('index.html', observations=observations[:AMOUNT_OF_BIRDS], time=current_time)

if __name__ == "__main__":
    app.run(port=PORT, host=HOST)
