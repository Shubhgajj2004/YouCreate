import os
from flask import Flask , render_template , request, url_for , redirect , jsonify

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def home():
     if request.method == "POST":
       Title = request.form.get("Title")
       story = request.form.get("story")
       return "Your name is "+Title + story
     return render_template("index.html")
 
if __name__ == '__main__':
    app.run()