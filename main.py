from flask import Flask, render_template
from dotenv import load_dotenv
import requests
import wikipedia
import time
import os

load_dotenv()

# Edit These Flags To Customize the software
PORT = 1991
HOST = "0.0.0.0"
<<<<<<< HEAD
KEY = get.env("API_KEY")
=======
KEY = "6ohcvqhs11a7"
>>>>>>> 251abbb6979da269d21e308ac4e11436643e7504
LOCATION = "L3700344"
AMOUNT_OF_BIRDS=10
print(">> Starting Software with The Following Argurments")
print(">> PORT: ", PORT)
print(">> HOST:", HOST)
print(">> KEY: ", KEY)
print(">> LOCATION: ", LOCATION)
print(">> Amount of Birds to Display: ", AMOUNT_OF_BIRDS)

def log_missing_img(sci_name):
    line = f"Missing image: {sci_name}" 
    with open("MISSING_IMAGE_LOG.txt", "a") as f:
        f.write(line)
        f.close()
    print("r")
def get_bird_image_url(sci_name):
    print(">> Checking For Manual Image Overide")
    manual_image_overrides = {
    "Milvus milvus": "https://www.natureplprints.com/p/729/red-kite-milvus-milvus-flight-15363331.jpg.webp",
    "Buteo buteo" : "https://cdn.openart.ai/published/gfDssGha4jNjVWozyeak/bizG1roP_Dtrc_256.webp",
    "Phasianus colchicus" : "https://cdn.neighbourly.co.nz/images/cache/message_image_thumbnail/message_images/626857575e9081.13864759.jpeg?170410",
    "Anthus pratensis": "https://th.bing.com/th/id/R.295b7daaa42792951d05a6b7da3a4573?rik=qzVHphcXNhp5OA&riu=http%3a%2f%2fwww.naturephoto-cz.com%2fphotos%2fbirds%2fanthus-pratensis-39724.jpg&ehk=SlJKj3z6grLHRdpznIDlz%2bI24%2fGfYvCybL3YCdhF93g%3d&risl=&pid=ImgRaw&r=0&sres=1&sresct=1",
    "Sylvia atricapilla": "https://media.istockphoto.com/id/174837709/photo/eurasian-blackcap.jpg?s=612x612&w=0&k=20&c=3kUxdWcOQ8Xj41Q4HEKzxhQPsrkxrAYWc8XupMm_O6g=",
    "Ardea cinerea" : "https://northkent.birdwise.org.uk/wp-content/uploads/2020/05/Grey-heron-800.jpg",
    "Pica pica" : "https://static.inaturalist.org/photos/256224620/large.jpg",
    "Chroicocephalus ridibundus" : "https://www.first-nature.com/algbirds/birdpics/chroicocephalus-ridibundus1.jpg",
    "Apus apus" : "https://upload.wikimedia.org/wikipedia/commons/thumb/b/be/Apus_apus_-Barcelona%2C_Spain-8_%281%29.jpg/960px-Apus_apus_-Barcelona%2C_Spain-8_%281%29.jpg",
    "Saxicola rubicola" : "https://cdn.download.ams.birds.cornell.edu/api/v2/asset/387157581/900",
    "Phylloscopus trochilus" : "https://base-prod.rspb-prod.magnolia-platform.com/.imaging/focalpoint/_WIDTH_x_HEIGHT_/dam/jcr:db52496b-b63e-46b0-8393-81ed6047bc7c/1924160333-Species-Willow-Warbler-stood-on-mossy-log.jpg",
    "Coloeus monedula" : "https://www.publicdomainpictures.net/pictures/510000/nahled/kauw-vogel-coloeus-monedula.jpg",
    "Columba palumbus" : "https://inaturalist-open-data.s3.amazonaws.com/photos/108521205/original.jpg",
    "Parus major" : "https://upload.wikimedia.org/wikipedia/commons/1/1b/Great_tit_%28Parus_major%29%2C_Parc_du_Rouge-Cloitre%2C_For%C3%AAt_de_Soignes%2C_Brussels_%2826194636951%29.jpg",
    "Cyanistes caeruleus" : "https://upload.wikimedia.org/wikipedia/commons/8/86/Eurasian_blue_tit_Lancashire.jpg",
    "Dendrocopos major" : "https://www.aejames.com/wp-content/uploads/2018/12/Great-Spotted-Woodpecker-bird-guide-%E2%80%93-Albert-E-James-and-Sons-900x628.jpg",
    "Erithacus rubecula" : "https://cdn.britannica.com/77/189277-050-C9C1CA8A/European-robin-redbreast-bird.jpg",
    "Turdus merula" : "https://upload.wikimedia.org/wikipedia/commons/a/a9/Common_Blackbird.jpg",
    "Chloris chloris" : "https://www.google.com/imgres?q=Chloris%20chloris&imgurl=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2F2%2F29%2FChloris_chloris_%2528profile%2529.jpg&imgrefurl=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FEuropean_greenfinch&docid=3TqE-51mFVXQ8M&tbnid=RAIgqx741Y6u3M&vet=12ahUKEwjDxZvTttuSAxW8WkEAHRj7JV0QM3oECBsQAA..i&w=3508&h=2732&hcb=2&ved=2ahUKEwjDxZvTttuSAxW8WkEAHRj7JV0QM3oECBsQAA",
    "Corvus corone" : "https://www.featherbase.info/static/images/speciesimages/c2736530-3897-4838-96e0-b85ad6438723_400px.jpg",
    "Linaria cannabina" : "https://observation.org/media/photo/4437480.jpg",
    "Anas platyrhynchos" : "https://cdn.download.ams.birds.cornell.edu/api/v2/asset/308743051/900",
    "Prunella modularis" : "https://observation.org/media/photo/15634944.jpg",
    "Vanellus vanellus" : "https://upload.wikimedia.org/wikipedia/commons/2/2f/Northern-Lapwing-Vanellus-vanellus.jpg",
    "Branta canadensis" : "https://base-prod.rspb-prod.magnolia-platform.com/.imaging/focalpoint/_WIDTH_x_HEIGHT_/dam/jcr:7d2047d9-2411-40ae-af94-5bb3233d1e70/2097541234-Species-Canada-Goose-Flying-to-left.jpg",
    "Anser anser" : "https://inaturalist-open-data.s3.amazonaws.com/photos/11134288/original.jpg",
    "Pluvialis apricaria" : "https://upload.wikimedia.org/wikipedia/commons/f/f7/Rohkunborri_Pluvialis_Apricaria.jpg",
    "Sturnus vulgaris" : "https://cdn.download.ams.birds.cornell.edu/api/v2/asset/317860951/1200",
    "Troglodytes troglodytes" : "https://www.aejames.com/wp-content/uploads/2018/12/Wren-bird-guide-%E2%80%93-Albert-E-James-and-Sons-900x600.jpg",
    "Turdus viscivorus" : "https://upload.wikimedia.org/wikipedia/commons/9/9e/Turdus_viscivorus.001_-_Cardiff.jpg",
    "Lullula arborea" : "https://static.inaturalist.org/photos/65541931/large.jpeg",
    "Corvus frugilegus" : "https://www.wildlifeinsight.com/wp-content/gallery/gb_birds/rook_6768.jpg",
    "Phalacrocorax carbo" : "https://upload.wikimedia.org/wikipedia/commons/c/c3/2021-05-05_Phalacrocorax_carbo_carbo%2C_Killingworth_Lake%2C_Northumberland_1-1.jpg"
    
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
    # Birds reported in the last 30 days at Greenham Common sorted by date and count
    data = sorted(data, key=lambda x: (x.get('obsDt', ''), x.get('howMany', 0)), reverse=True)
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
