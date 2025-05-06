from twilio.rest import Client
from geopy.geocoders import Nominatim
import requests

# 🚨 WARNING: Hardcoding credentials is not secure! Use environment variables instead.
ACCOUNT_SID = "acc id"
AUTH_TOKEN = "acc token"
TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"  # Twilio Sandbox Number

# Emergency Contacts in WhatsApp format (FIXED HOSPITAL NUMBER)
POLICE_WHATSAPP = "whatsapp:+911234567890"
HOSPITAL_WHATSAPP = "whatsapp:+14155238886"  # Use a single valid number

# Function to Get Approximate Location
def get_location():
    try:
        response = requests.get("https://ipinfo.io/json")
        data = response.json()
        location = data["loc"].split(",")  # Extract lat, lon
        latitude, longitude = location[0], location[1]

        # Convert to Address
        geolocator = Nominatim(user_agent="geoapi")
        address = geolocator.reverse(f"{latitude}, {longitude}").address

        maps_link = f"https://www.google.com/maps/search/?api=1&query={latitude},{longitude}"
        return address, maps_link
    except Exception as e:
        return "Location Unavailable", ""

# Function to Send WhatsApp Message (FIXED to use dynamic `to`)
def send_whatsapp(to, message):
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    try:
        msg = client.messages.create(
            from_=TWILIO_WHATSAPP_NUMBER,
            body=message,
            to=to  # ✅ Dynamically sending to correct recipient
        )
        print(f"✅ WhatsApp message sent to {to}: {msg.sid}")
    except Exception as e:
        print(f"❌ Error sending WhatsApp message: {e}")

# Function to Trigger Alert with Location
def alert_authorities(event):
    if event == "accident_detected":
        address, maps_link = get_location()
        message = f"🚨 Emergency Alert: Accident detected!\n📍 Location: {address}\n🔗 Map: {maps_link}"

        send_whatsapp(POLICE_WHATSAPP, message)
        send_whatsapp(HOSPITAL_WHATSAPP, message)

# Trigger alert
alert_authorities("accident_detected")
