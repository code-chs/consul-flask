import json
import socket
import requests
from flask import Flask
from redis import Redis, RedisError

BASE_CONSUL_URL = 'http://consul:8500'


def connect_redis():
    url = BASE_CONSUL_URL + '/v1/catalog/service/redis'
    res = requests.get(url)
    data = json.loads(res.text)
    try:
        ret = Redis(
            host=data[0]["ServiceAddress"],
            db=0,
            socket_connect_timeout=2,
            socket_timeout=2)
    except RedisError:
        return False
    return ret


redis = connect_redis()

HOST = socket.gethostname()
ADDR = socket.gethostbyname(socket.gethostname())
PORT = 5000

app = Flask(__name__)


@app.route('/')
def hello():
    global redis
    try:
        visits = redis.incr("counter")
    except RedisError:
        visits = "<i>cannot connect to Redis</i>"

    html = "<b>Visits:</b> {visits}"

    return html.format(visits=visits)


@app.route('/health')
def hello_world():
    return "{'status':'healthy'}"


@app.route('/reconnect')
def reconnect():
    global redis
    redis = connect_redis()
    if redis:
        return 'reconnected to redis'
    return 'ERROR: cannot reconnect to redis'


def register():
    url = BASE_CONSUL_URL + '/v1/agent/service/register'
    data = {
        'Name': '{}'.format(ADDR),
        'Tags': ['flask'],
        'Address': ADDR,
        'Port': PORT,
        'Check': {
            'http':
            'http://{address}:{port}/health'.format(address=ADDR, port=PORT),
            'interval':
            '10s'
        }
    }
    res = requests.put(url, data=json.dumps(data))
    return res.text


if __name__ == "__main__":
    register()
    app.run(host="0.0.0.0", debug=False)
