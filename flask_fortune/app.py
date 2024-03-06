from flask import Flask, render_template, request, redirect, url_for
import requests
import datetime

app = Flask(__name__)

date = datetime.datetime.today().strftime("%Y/%m/%d")

def get_fortune(seiza):
   res = requests.get(url='http://api.jugemkey.jp/api/horoscope/free/'+ date)
   fortune = res.json()["horoscope"][date][seiza]
   print(fortune)
   return fortune

@app.route('/')
def index():
  return render_template('index.html', date=date)

@app.route('/fortune', methods=['POST'])
def fortune():
  seiza = int(request.form['seiza'])
  fortune = get_fortune(seiza)
  star = {1:'★', 2:'★★', 3:'★★★', 4:'★★★★', 5:'★★★★★'}
  return render_template('result.html', fortune=fortune, date=date, star=star, seiza=seiza)

if __name__ == "__main__":
    app.run(debug=True)

