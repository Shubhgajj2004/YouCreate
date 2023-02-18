import urllib.request
from PIL import Image
import json
import requests
from bs4 import BeautifulSoup
import shutil
import re, os
from gtts import gTTS
from moviepy.editor import *
from flask import Flask , render_template , request, url_for , redirect , jsonify

app = Flask(__name__)

pathTImg = "static/teditImages"


@app.route('/', methods=['GET','POST'])
def home():
     if request.method == "POST":
       Title = request.form.get("Title")
       story = request.form.get("story")

        # Split the text by , and .
       paragraphs = re.split(r"[.]", story)
       sizePara = len(paragraphs)

       #Create Necessary Folders
       if not os.path.exists("static/audio"):
         os.makedirs("static/audio")
       if not os.path.exists("static/images"):
         os.makedirs("static/images")
       if not os.path.exists("static/videos"):
         os.makedirs("static/videos")
       
       url = f"https://www.google.com/search?q={paragraphs[0]},{Title}&tbm=isch&tbs=isz:l"
       response = requests.get(url)
       soup = BeautifulSoup(response.text, "html.parser")
       image_tags = soup.find_all("img")
       urls = [img["src"] for img in image_tags][1:7]
      

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

       return render_template('imageselect.html',Title = Title, index=0, paragraph=paragraphs[0], img0=pathTImg+"/0.jpg", img1=pathTImg+"/1.jpg", img2=pathTImg+"/2.jpg", img3=pathTImg+"/3.jpg", img4=pathTImg+"/4.jpg", img5=pathTImg+"/5.jpg")
       
     return render_template("index.html")



@app.route('/screen', methods=['POST'])
def screen():
    index = int(request.form['index'])
    story = request.form['story']
    title = request.form['title']

    paragraphs = re.split(r'[.]', story)

    if index >= len(paragraphs) - 1:
        # We've reached the end of the story, so redirect to the index page
        return redirect('/')

    # Render the next screen
    next_index = index + 1
    print(next_index)
    print(len(paragraphs))
    print("Good morning")

    if next_index==len(paragraphs)-1:
      print("Hello")
      print(next_index)
      merge()


    next_paragraph = paragraphs[next_index] 

    #Webcreaping of images
    url = f"https://www.google.com/search?q={next_paragraph},{title}&tbm=isch&tbs=isz:xxlarge,islt:qsvga"
    print(url)
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


    return render_template('imageselect.html', index=next_index, paragraph=next_paragraph,img0=pathTImg+"/0.jpg", img1=pathTImg+"/1.jpg", img2=pathTImg+"/2.jpg", img3=pathTImg+"/3.jpg", img4=pathTImg+"/4.jpg", img5=pathTImg+"/5.jpg")


@app.route('/finalImg', methods=['POST'])
def finalImg():

    # #Create Necessary Folders
    # if not os.path.exists("static/finalized"):
    #   os.makedirs("static/finalized")
    
    #getting the id of the image
    idImg = request.json.get('idImg')
    indvalue = request.json.get('ind')
    para = request.json.get('para')
    # print(para)

    #save the image to finalize folder
    imgUrl = "static/teditImages/"+idImg+".jpg"
    # urllib.request.urlretrieve(imgUrl, f"static/finalized/image{indvalue}.jpg")
    # print("The Generated Image Saved in Images Folder!")
    shutil.copy(imgUrl, f"static/images/image{indvalue}.jpg")
    print("The Generated Image Saved in Images Folder!")

     # Create gTTS instance and save to a file
    tts = gTTS(text=para, lang='en', slow=False)
    tts.save(f"static/audio/voiceover{indvalue}.mp3")
    print("The Paragraph Converted into VoiceOver & Saved in Audio Folder!")

    # Load the audio file using moviepy
    print("Extract voiceover and get duration...")
    audio_clip = AudioFileClip(f"static/audio/voiceover{indvalue}.mp3")
    audio_duration = audio_clip.duration

    # Load the image file using moviepy
    print("Extract Image Clip and Set Duration...")
    image_clip = ImageClip(f"static/images/image{indvalue}.jpg").set_duration(audio_duration)

    print("Concatenate Audio, Image, Text to Create Final Clip...")
    clip = image_clip.set_audio(audio_clip)
    video = CompositeVideoClip([clip])

    # Save the final video to a file
    video = video.write_videofile(f"static/videos/video{indvalue}.mp4", fps=24)
    print(f"The Video{indvalue} Has Been Created Successfully!")

    return "Hello"
    

def sorted_nicely( l ): 
    """ Sort the given iterable in the way that humans expect.""" 
    convert = lambda text: int(text) if text.isdigit() else text 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(l, key = alphanum_key)


    
@app.route('/merge')
def merge():  
  clips = []
  l_files = os.listdir("static/videos")
  s = sorted_nicely(l_files)
  print(s)

  for file in s:
    clip = VideoFileClip(f"static/videos/{file}")
    clips.append(clip)

  print("Concatenate All The Clips to Create a Final Video...")
  final_video = concatenate_videoclips(clips, method="compose")
  final_video = final_video.write_videofile("static/final_video.mp4")
  print("The Final Video Has Been Created Successfully!")
  
    


 
if __name__ == '__main__':
    app.run()