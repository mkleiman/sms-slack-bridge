from flask import Flask, request, Response
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import os
import re
import ssl
import certifi
from slack_sdk import WebClient
from slack_sdk.signature import SignatureVerifier

app = Flask(__name__)

# Initialize Twilio client
twilio_client = Client(
    os.getenv("TWILIO_ACCOUNT_SID"),
    os.getenv("TWILIO_AUTH_TOKEN")
)

# Initialize Slack client with proper SSL handling
ssl_context = None
try:
    # Try to use system certificates first
    slack_client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))
    print("✅ Using default SSL configuration")
except Exception as e:
    print(f"⚠️  Default SSL failed, trying custom SSL context: {e}")
    # Fallback to custom SSL context
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    ssl_context.verify_mode = ssl.CERT_REQUIRED
    ssl_context.check_hostname = True
    
    slack_client = WebClient(
        token=os.getenv("SLACK_BOT_TOKEN"),
        ssl=ssl_context
    )
    print("✅ Using custom SSL context")

# Initialize Slack signature verifier
slack_sig_verifier = SignatureVerifier(os.getenv("SLACK_SIGNING_SECRET"))

@app.route('/incoming/twilio', methods=['POST'])
def send_incoming_sms():
    try:
        from_number = request.form.get('From')
        sms_message = request.form.get('Body')
        
        message = f"Text message from {from_number}: {sms_message}"
        
        # Try to post to Slack
        try:
            if ssl_context:
                print(f"🔐 Attempting to post to Slack with custom SSL context: {ssl_context.verify_mode}")
            else:
                print("🔐 Attempting to post to Slack with default SSL configuration")
            
            slack_message = slack_client.chat_postMessage(
                channel='#texts', text=message)
            print(f"✅ Successfully posted to Slack: {message}")
        except Exception as e:
            print(f"❌ Failed to post to Slack: {e}")
            if ssl_context:
                print(f"🔍 SSL Context details: verify_mode={ssl_context.verify_mode}, check_hostname={ssl_context.check_hostname}")
            else:
                print("🔍 Using default SSL configuration")
            # Still return success to Twilio to avoid retries
        
        response = MessagingResponse()
        return Response(response.to_xml(), mimetype="text/html")
    except Exception as e:
        print(f"❌ Error in SMS endpoint: {e}")
        response = MessagingResponse()
        return Response(response.to_xml(), mimetype="text/html")

@app.route('/incoming/slack', methods=['POST'])
def send_incoming_slack():
    try:
        attributes = request.get_json()
        if 'challenge' in attributes:
            return Response(attributes['challenge'], mimetype="text/plain")
        
        incoming_slack_message_id, slack_message, channel = parse_message(attributes)
        if incoming_slack_message_id and slack_message:
            to_number = get_to_number(incoming_slack_message_id, channel)
            if to_number:
                try:
                    messages = twilio_client.messages.create(
                        to=to_number, from_=os.getenv("TWILIO_NUMBER"), body=slack_message)
                    print(f"✅ Successfully sent SMS to {to_number}: {slack_message}")
                except Exception as e:
                    print(f"❌ Failed to send SMS: {e}")
            return Response()
        return Response()
    except Exception as e:
        print(f"❌ Error in Slack endpoint: {e}")
        return Response()

def parse_message(attributes):
    if 'event' in attributes and 'thread_ts' in attributes['event']:
        return attributes['event']['thread_ts'], attributes['event']['text'], attributes['event']['channel']
    return None, None, None

def get_to_number(incoming_slack_message_id, channel):
    data = slack_client.conversations_history(channel=channel, latest=incoming_slack_message_id, limit=1, inclusive=1)
    if 'subtype' in data['messages'][0] and data['messages'][0]['subtype'] == 'bot_message':
        text = data['messages'][0]['text']
        phone_number = extract_phone_number(text)
        return phone_number
    return None

def extract_phone_number(text): 
    data = re.findall(r'\w+', text)
    if len(data) >= 4: 
        return data[3]
    return None

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug, host='0.0.0.0', port=port)
