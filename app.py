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

pathTImg = "static/teditImages"


@app.route('/', methods=['GET','POST'])
def home():
     if request.method == "POST":
       Title = request.form.get("Title")
       story = request.form.get("story")

        # Split the text by , and .
       paragraphs = re.split(r"[.,]", story)

       #Create Necessary Folders
       if not os.path.exists("static/audio"):
         os.makedirs("static/audio")
       if not os.path.exists("static/images"):
         os.makedirs("static/images")
       if not os.path.exists("static/videos"):
         os.makedirs("static/videos")
       
      #  print(paragraphs[0], paragraphs[1], paragraphs[2])
       url = f"https://www.google.com/search?q={paragraphs[0]}&tbm=isch&tbs=isz:l"
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
            filename = f"{i}.jpg"
            filepath = os.path.join(pathTImg, filename)
            
            if os.path.exists(filepath):
                os.remove(filepath)
            
            file = open(filepath, "wb")
            for chunk in response.iter_content(1024):
                file.write(chunk)
            file.close()
            
            print(f"File {filename} downloaded successfully.")
            
        except:
            print(f"Failed to download {url}")

      #  print(paragraphs[0])
       return render_template('imageselect.html', index=0, paragraph=paragraphs[0], img0=pathTImg+"/0.jpg", img1=pathTImg+"/1.jpg", img2=pathTImg+"/2.jpg", img3=pathTImg+"/3.jpg", img4=pathTImg+"/4.jpg", img5=pathTImg+"/5.jpg")
       
     return render_template("index.html")

# @app.route('/getImage/<int:index>', methods=['GET', 'POST'])
# def getImage(story, index):
#     return render_template("temp.html", result=story[index], index=index, data=story)


@app.route('/screen', methods=['POST'])
def screen():
    index = int(request.form['index'])
    story = request.form['story']
    paragraphs = re.split(r'[,.]', story)

    if index >= len(paragraphs) - 1:
        # We've reached the end of the story, so redirect to the index page
        return redirect('/')

    # Render the next screen
    next_index = index + 1
    next_paragraph = paragraphs[next_index] 

    #Webcreaping of images
    url = f"https://www.google.com/search?q={next_paragraph}&tbm=isch&tbs=isz:xxlarge,islt:qsvga"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    image_tags = soup.find_all("img")
    urls = [img["src"] for img in image_tags][1:7]
      

        # Step 6: Download the images
    if not os.path.exists("static/teditImages"):
      os.makedirs("static/teditImages")

    # for i, url in enumerate(urls):
    #      try:
    #          response = requests.get(url, stream=True)
    #          file = open(os.path.join(pathTImg, f"{i}.jpg"), "wb")
    #          for chunk in response.iter_content(1024):
    #              file.write(chunk)
    #          file.close()
    #      except:
    #          print(f"Failed to download {url}")
    for i, url in enumerate(urls):
        try:
            response = requests.get(url, stream=True)
            filename = f"{i}.jpg"
            filepath = os.path.join(pathTImg, filename)
            
            if os.path.exists(filepath):
                os.remove(filepath)
            
            file = open(filepath, "wb")
            for chunk in response.iter_content(1024):
                file.write(chunk)
            file.close()
            
            print(f"File {filename} downloaded successfully.")
            
        except:
            print(f"Failed to download {url}")


    return render_template('imageselect.html', index=next_index, paragraph=next_paragraph, img0=pathTImg+"/0.jpg", img1=pathTImg+"/1.jpg", img2=pathTImg+"/2.jpg", img3=pathTImg+"/3.jpg", img4=pathTImg+"/4.jpg", img5=pathTImg+"/5.jpg")


@app.route('/finalImg', methods=['POST'])
def finalImg():

    #Create Necessary Folders
    if not os.path.exists("static/finalized"):
      os.makedirs("static/finalized")
    
    idImg = request.json.get('idImg')
    print(idImg)
    
    


 
if __name__ == '__main__':
    app.run()