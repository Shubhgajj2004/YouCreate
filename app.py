from sapling import SaplingClient
import re
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
        edits = client.edits(original,session_id='test_session')
        edits = sorted(edits, key=lambda e: -1 * (e['sentence_start'] + e['start']))
        for edit in edits:
          start = edit['sentence_start'] + edit['start']
          end = edit['sentence_start'] + edit['end']
          # if start > len(text) or end > len(text):
          #   print(f'Edit start:{start}/end:{end} outside of bounds of text:{text}')
          #   continue
          text = text[: start] + edit['replacement'] + text[end:]
          texts = re.split(r"[,.]", text)
          for i in texts:
              l = len(i.split(" "))
              if l < 10:
                  texts.remove(i)
        return render_template('result.html',original = original,enhanced = text,texts = texts)

if __name__ == '__main__':
    app.run()