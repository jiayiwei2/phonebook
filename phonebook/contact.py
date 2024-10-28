import re
from datetime import datetime

class Contact:
    """
    A class to represent a contact in the phone book.
    """
    def __init__(self, first_name, last_name, phone_number, email=None, address=None):
        """Initialize a new contact with the given details."""
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = self.validate_and_format_phone_number(phone_number)
        self.email = self.validate_email(email)
        self.address = address
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.history = []

    def validate_and_format_phone_number(self, phone_number):
        """Validate and format the phone number into (###) ###-#### format."""
        digits = re.sub(r'\D', '', phone_number)
        if len(digits) != 10:
            raise ValueError("Phone number must contain exactly 10 digits")
        formatted_number = f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
        return formatted_number

    def validate_email(self, email):
        """Validate the email address against standard criteria."""
        if email:
            pattern = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$')
            if not pattern.match(email):
                raise ValueError("Invalid email address")
        return email

    def update_history(self, action):
        """Record an action in the contact's history with a timestamp."""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.history.append(f"{timestamp} - {action}")

    def __str__(self):
        """Return a string representation of the contact."""
        return f"{self.first_name} {self.last_name}, {self.phone_number}, {self.email}, {self.address}"