import os
from flask import Flask,request
from dotenv import load_dotenv
from lib import process_event, verify_token
# Load .env file using:
load_dotenv()
app = Flask(__name__)
 

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        try:
            return verify_token(mode, token, challenge), 200
        except Exception as e:
            # // Responds with '403 Forbidden' if verify tokens do not match
            return b'',403
    elif request.method == 'POST':
        body = request.get_json()
        if process_event(body):
            return "EVENT_RECEIVED", 200
        return b"", 404 
 
app.run()