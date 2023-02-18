from sapling import SaplingClient
from flask import Flask , render_template , request

API_KEY = 'NLDUU0EBQN7S97RNAW0AYT35FFMO3BNY'
client = SaplingClient(api_key = API_KEY)

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def home():
    if request.method == 'POST':
        original = request.form.get('story')
        return result(original)
    return render_template('index.html')

 
@app.route('/result',methods=['GET','POST'])
def result(original):
    if request.method == "POST":
        text = str(original)
        edits = sorted(edits, key=lambda e: -1 * (e['sentence_start'] + e['start']))
        for edit in edits:
          start = edit['sentence_start'] + edit['start']
          end = edit['sentence_start'] + edit['end']
          # if start > len(text) or end > len(text):
          #   print(f'Edit start:{start}/end:{end} outside of bounds of text:{text}')
          #   continue
          text = text[: start] + edit['replacement'] + text[end:]
        return render_template('result.html',original = original,enhanced = text)

if __name__ == '__main__':
    app.run()