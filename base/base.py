""" Hello Service
"""

from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)

VERSION = "0.1"

messages = {}


@app.route('/')
def version():
    """ Root IRI returns the API version """
    return jsonify(version=VERSION)


@app.route('/messages', methods=['GET', 'POST'])
def messages():
    """ /messages collection allows POST of new messages and GET of all messages """
    if request.method == 'POST':
        message = request.get_json()
        result = validate_message(message)
        if result:
            print("ERROR: " + request.url + " : " + result)
            return jsonify(error=result), 400
        messages["id"] = message
        return jsonify(message), 201
    else:  # GET
        return jsonify(list(messages.values()))


@app.route('/waste/cans/<int:message_id>', methods=['GET', 'DELETE'])
def message(message_id):
    """ can id can be used as a /cans path param to GET/DELETE a single can """
    if message_id not in messages:
        return jsonify(error="message id not found"), 404
    if request.method == 'GET':
        return jsonify(messages[message_id])
    elif request.method == 'DELETE':
        del messages[message_id]
        return '', 204
    else:
        return jsonify(error="bad HTTP verb, only GET and DELETE supported"), 400


def validate_message(message):
    """ DbC checks for required message fields and settings
            returns False if message is valid
            returns a string describing the error otherwise
    """
    try:
        # Test id
        message["id"] = int(message["id"])
        if message["id"] < 0 or 999999999 < message["id"]:
            raise ValueError("message.id out of range [0..999999999]")
        if len(message.get("message")) < 1:
            raise ValueError("message.message has no value")
    except Exception as ex:
        return str(ex)
    return ""  # no errors
