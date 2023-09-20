from twilio.rest import Client

def send_sms_alert(customer, item):
    # Initialize Twilio client
    client = Client("TWILIO_ACCOUNT_SID", "TWILIO_AUTH_TOKEN")

    # Create and send SMS
    message = client.messages.create(
        body=f"New order: {item}",
        from_="YOUR_TWILIO_PHONE_NUMBER",
        to=customer.phone_number  # Assuming you have a phone_number field in the Customer model
    )