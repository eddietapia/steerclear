from flask import Flask
app = Flask(__name__)

@app.route("/buzz", methods=['GET','POST'])
def buzz():
  return "BUZZ"

if __name__=="__main__":
  app.run(host='10.52.88.73')
