""" Hello Service
"""

from flask import Flask
from flask import jsonify
from flask import request

application = Flask(__name__)

VERSION = "0.1"

stored_messages = {}


@application.route('/')
def version():
    """ Root IRI returns the API version """
    return jsonify(version=VERSION)


@application.route('/messages', methods=['GET', 'POST'])
def messages():
    """ /messages collection allows POST of new messages and GET of all messages """
    if request.method == 'POST':
        message = request.get_json()
        application.logger.info("Posting message %s" % message.get('message'))
        result = validate_message(message)
        if result:
            print("ERROR: " + request.url + " : " + result)
            return jsonify(error=result), 400
        stored_messages[message.get("id")] = message
        response = jsonify(message)
        response.status_code = 201
        response.headers['Location'] = "/messages/" + str(message["id"])
        response.autocorrect_location_header = False
        return response
    else:  # GET
        return jsonify(list(stored_messages.values()))


@application.route('/messages/<int:message_id>', methods=['GET', 'DELETE'])
def message(message_id):
    """ can id can be used as a /cans path param to GET/DELETE a single can """
    if message_id not in stored_messages:
        return jsonify(error="message id not found"), 404
    if request.method == 'GET':
        return jsonify(stored_messages[message_id])
    elif request.method == 'DELETE':
        del stored_messages[message_id]
        return '', 204
    else:
        return jsonify(error="bad HTTP verb, only GET and DELETE supported"), 400


def validate_message(val_message):
    """ DbC checks for required message fields and settings
            returns False if message is valid
            returns a string describing the error otherwise
    """
    try:
        # Test id
        val_message["id"] = int(val_message["id"])
        if val_message["id"] < 0 or 999999999 < val_message["id"]:
            raise ValueError("message.id out of range [0..999999999]")
        if len(val_message.get("message")) < 1:
            raise ValueError("message has no value")
    except Exception as ex:
        return str(ex)
    return ""  # no errors
