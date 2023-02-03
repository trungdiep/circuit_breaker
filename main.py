import random
import time
import requests

from flask import Flask, abort
app = Flask(__name__)


@app.route('/success')
def success_endpoint():
    return {
        "msg": "Call to this endpoint was a smashing success."
    }, 200


@app.route('/failure') # type: ignore   
def faulty_endpoint():
    rs = requests.get("http://localhost:5000/random")
    print(vars(rs))
    if rs.status_code >= 500:
        return {'test': 'test'}, 500


@app.route('/random')
def fail_randomly_endpoint():
    abort(501)
    r = random.randint(0, 1)
    if r == 0:
        return {
            "msg": "Success msg"
        }, 200

    return {
        "msg": "I will fail (sometimes)."
    }, 500
