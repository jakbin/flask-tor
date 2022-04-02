from flask import Flask
from flask_tor import run_with_tor

app = Flask(__name__)
port = run_with_tor()

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == '__main__':
    app.run(port=port)
