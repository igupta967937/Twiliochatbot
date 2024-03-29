from flask_ngrok import run_with_ngrok
from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)
run_with_ngrok(app)
@app.route('/', methods=['POST'])
def index():
    new_msg = request.values.get('Body', '').lower()
    response = MessagingResponse()
    msg = response.message()
    responded = False

    if 'quote' in new_msg:
        r = requests.get('https://api.quotable.io/random')
        if r.status_code == 200:
            data = r.json()
            quote = (f'{data["content"]} ({data["author"]})')
        else:
            quote = 'I could not retrieve a quote at this time, sorry.'
        msg.body(quote)
        responded = True

    if not responded:
        msg.body('I am sorry i can only help with quotes!')
    return str(response)

if __name__ == '__main__':
    app.run()