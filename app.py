# import urllib.request
# from PIL import Image
# import requests
# import json
import requests
from bs4 import BeautifulSoup

import re, os
# from gtts import gTTS
# from moviepy.editor import *
from flask import Flask , render_template , request, url_for , redirect , jsonify

app = Flask(__name__)


@app.route('/', methods=['GET','POST'])
def home():
     if request.method == "POST":
       Title = request.form.get("Title")
       story = request.form.get("story")

        # Split the text by , and .
       paragraphs = re.split(r"[,.]", story)

       url = f"https://www.google.com/search?q={paragraphs[0]}&tbm=isch&tbs=isz:lt,islt:qsvga"
       response = requests.get(url)
       soup = BeautifulSoup(response.text, "html.parser")
       image_tags = soup.find_all("img")
       urls = [img["src"] for img in image_tags][1:7]

        # Step 6: Download the images
       if not os.path.exists("static/teditImages"):
         os.makedirs("static/teditImages")

       for i, url in enumerate(urls):
            try:
                response = requests.get(url, stream=True)
                file = open(os.path.join("static/teditImages", f"{i}.jpg"), "wb")
                for chunk in response.iter_content(1024):
                    file.write(chunk)
                file.close()
            except:
                print(f"Failed to download {url}")

       return render_template('editImage.html', index=0, paragraph=paragraphs[0])
       
     return render_template("index.html")

# @app.route('/getImage/<int:index>', methods=['GET', 'POST'])
# def getImage(story, index):
#     return render_template("temp.html", result=story[index], index=index, data=story)


@app.route('/screen', methods=['POST'])
def screen():
    index = int(request.form['index'])
    story = request.form['story']
    paragraphs = re.split(r'[,.  ]', story)

    if index >= len(paragraphs) - 1:
        # We've reached the end of the story, so redirect to the index page
        return redirect('/')

    # Render the next screen
    next_index = index + 1
    next_paragraph = paragraphs[next_index] 

    #Webcreaping of images
    url = f"https://www.google.com/search?q={next_paragraph}&tbm=isch&tbs=isz:lt,islt:qsvga"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    image_tags = soup.find_all("img")
    urls = [img["src"] for img in image_tags][1:7]

    # Step 6: Download the images
    if not os.path.exists("static/teditImages"):
        os.makedirs("static/teditImages")

    for i, url in enumerate(urls):
        try:
            response = requests.get(url, stream=True)
            file = open(os.path.join("tImage", f"{i}.jpg"), "wb")
            for chunk in response.iter_content(1024):
                file.write(chunk)
            file.close()
        except:
            print(f"Failed to download {url}")



    return render_template('editImage.html', index=next_index, paragraph=next_paragraph)

 
if __name__ == '__main__':
    app.run()