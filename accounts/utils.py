import random
import string
import requests

def generate_otp(length=4):
    return ''.join(random.choices('0123456789', k=length))

def generate_password(length=8):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))





import requests

def send_sms_bdbulksms(phone_number: str, message: str, token: str) -> str:
    """
    Send SMS via bdbulksms API using POST and token auth.

    Args:
        phone_number: Recipient phone number (string)
        message: SMS message text (string)
        token: API token (string)

    Returns:
        "SENT" if message sent successfully,
        otherwise "FAILED"
    """

    url = "https://api.bdbulksms.net/api.php?json"
    data = {
        'token': token,
        'to': phone_number,
        'message': message,
    }

    try:
        response = requests.post(url, data=data, timeout=10)
        response.raise_for_status()
        result = response.json()
    except (requests.RequestException, ValueError) as e:
        print(f"SMS sending error: {e}")
        return "FAILED"

    # Result is expected to be a list of dicts [{ 'status': 'SENT' or other, ... }]
    if isinstance(result, list) and len(result) > 0 and 'status' in result[0]:
        return result[0]['status']
    else:
        return "FAILED"




