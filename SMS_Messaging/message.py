# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client

# Find your Account SID and Auth Token at twilio.com/console,
# then set TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN in your environment.
account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
client = Client("ACb5d73c5da17de12aa2c21a7f16696c0a", "dc369bf57a6291d2428aa31f8dbfa1de")

message = client.messages.create(
    to="+18035870302",
    from_="+17372583478",
    body="sms_account_alerts"
)

print(message.sid)
