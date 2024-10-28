import re

def validate_phone_number(phone_number):
    """Validate the phone number format."""
    pattern = re.compile(r'^\(\d{3}\) \d{3}-\d{4}$')
    if not pattern.match(phone_number):
        raise ValueError("Phone number must be in the format (###) ###-####")
    return phone_number

def validate_email(email):
    """Validate the email address format."""
    if email:
        pattern = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$')
        if not pattern.match(email):
            raise ValueError("Invalid email address")
    return email