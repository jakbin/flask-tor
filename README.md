# flask-tor

Run your flask website in tor using flask_tor.It doesn’t interfere with other tor processes on your computer, so you can use the Tor Browser or the system tor on their own.

 [![PyPI version](https://badge.fury.io/py/flask-tor.svg)](https://badge.fury.io/py/flask-tor)
 [![Downloads](https://pepy.tech/badge/flask-tor/month)](https://pepy.tech/project/flask-tor)
 [![Downloads](https://static.pepy.tech/personalized-badge/flask-tor?period=total&units=international_system&left_color=green&right_color=blue&left_text=Total%20Downloads)](https://pepy.tech/project/flask-tor)
 ![Python 3.6](https://img.shields.io/badge/python-3.6-yellow.svg)


### Disclaimer:-
Use it only for educational purpose.

## Features
- No need root permission
- Multiple instances

## Compatability
Python 3.6+ is required.

## Installation

```bash
pip install flask-tor
```

## Quickstart
1. Import with ```from flask_tor import run_with_tor``` .
2. call function `run_with_tor()` , store as variable and give it as port argument in flask app.

```python
# flask_tor_example.py
from flask import Flask
from flask_tor import run_with_tor

app = Flask(__name__)
port = run_with_tor()

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == '__main__':
    app.run(port=port)
```

Running the example:
```bash
python flask_tor_example.py
connecting_to_tor: 100% - Done                                                       
 * Running on <random_adress>.onion
 * Serving Flask app "main"
 * Debug mode: off
 * Running on http://127.0.0.1:<port>/
```

### Credit :- [onionshare](https://github.com/onionshare/onionshare)