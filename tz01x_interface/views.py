import os
import requests
from django.http import HttpResponse, Http404
from rest_framework.views import APIView

class WebhookInterface(APIView):
    def get(self, request, *args, **kwargs):

        VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
        mode = request.GET.get("hub.mode")
        token = request.GET.get("hub.verify_token")
        challenge = request.GET.get("hub.challenge")
        try:
            return HttpResponse(verify_token(mode, token, challenge, VERIFY_TOKEN))
        except Exception as e:
            # // Responds with '403 Forbidden' if verify tokens do not match
            return HttpResponse(status=403)

    def post(self, request, *args, **kwargs):
        body = request.data
        if process_event(body):
            return HttpResponse(content="EVENT_RECEIVED")
        return Http404()


def verify_token(mode, token, challenge, VERIFY_TOKEN):
    if mode and token:
        # Check the mode and token sent are correct
        if mode == "subscribe" and token == VERIFY_TOKEN:
            # // Respond with 200 OK and challenge token from the request
            print("WEBHOOK_VERIFIED")
            return challenge
    raise Exception("not verify")


def process_event(body):
    if body.get('object') == 'page':
        for entry in body.get('entry'):
            webhook_event = entry['messaging'][0]
            sender_psid = webhook_event\
                .get('sender')\
                .get('id')
            if (webhook_event.get("message")):
                handleMessage(sender_psid, webhook_event['message'])
            elif webhook_event.get("postback"):
                handlePostback(sender_psid, webhook_event['postback'])
                pass
        return True
    return False


def handleMessage(sender_psid, received_message):
    response = {}
    if received_message.get('text'):
        response = {
            "text": f"you sent the message: {received_message['text']} Now send me an image!"
        }
    elif received_message.get("attachments"):
        attachment_urls = received_message["attachments"][0]["payload"]["url"]
        response = {
            "attachment":{
            "type":"image", 
            "payload":{
                "url":attachment_urls, 
                "is_reusable":True
            }
            },
            "text":"is this the image"
            
        }
    callSendAPI(sender_psid, response)


def handlePostback(sender_psid, received_postback):
    pass


def callSendAPI(sender_psid, response):
    request_body = {
        "recipient": {
            "id": sender_psid,
        },
        "message": response,
    }
    PAGE_ACCESS_TOKEN = os.environ.get('PAGE_ACCESS_TOKEN')
    url = f"https://graph.facebook.com/v2.6/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    response = requests.post(url, json = request_body)
    if response.status_code:
        print("message sent")
    else:
        print("error "+ response.text)
    