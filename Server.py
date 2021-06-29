
import logging
from flask import Flask
from flask import request
from flask import Response
import json

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

uptimeCalls = 0

@app.route("/callback/text", methods=["GET"])
def index():
    global uptimeCalls

    if request.headers.getlist("X-Real-IP"):
        ip = request.headers.getlist("X-Real-IP")[0]
    else:
        ip = request.remote_addr

    uptimeCalls += 1
    app.logger.info("Total calls: " + str(uptimeCalls))

    return Response(ip, mimetype='text/html')


@app.route("/callback", methods=["GET"])
def json_out():
    global uptimeCalls

    if request.headers.getlist("X-Real-IP"):
        ip = request.headers.getlist("X-Real-IP")[0]
    else:
        ip = request.remote_addr

    uptimeCalls += 1
    app.logger.info("Total calls: " + str(uptimeCalls))

    ret = {"IP": ip}
    response = app.response_class(
        response=json.dumps(ret),
        status=200,
        mimetype='application/json'
    )
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0')
