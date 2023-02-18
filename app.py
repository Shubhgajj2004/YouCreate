# import urllib.request
# from PIL import Image
# import requests
# import json

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

       return render_template('temp.html', index=0, paragraph=paragraphs[0])
       
     return render_template("index.html")

@app.route('/getImage/<int:index>', methods=['GET', 'POST'])
def getImage(story, index):
    return render_template("temp.html", result=story[index], index=index, data=story)


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
    return render_template('temp.html', index=next_index, paragraph=next_paragraph)

 
if __name__ == '__main__':
    app.run()