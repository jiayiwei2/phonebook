import csv
import logging
from contact import Contact
from datetime import datetime

class PhoneBook:
    """
    A class to manage a phone book of contacts.
    """
    def __init__(self):
        """Initialize an empty phone book and set up logging."""
        self.contacts = []
        logging.basicConfig(filename='phonebook.log', level=logging.INFO, format='%(asctime)s - %(message)s')

    def add_contact(self, contact):
        """Add a new contact to the phone book."""
        self.contacts.append(contact)
        contact.update_history("Added contact")
        logging.info(f"Added contact: {contact}")

    def view_contacts(self):
        """Display all contacts in the phone book."""
        if not self.contacts:
            print("No contacts found.")
        for contact in self.contacts:
            print(contact)

    def search_contacts(self, query):
        """Search for contacts by name or phone number."""
        results = [contact for contact in self.contacts if query.lower() in contact.first_name.lower() or query.lower() in contact.last_name.lower() or query in contact.phone_number]
        logging.info(f"Searched for: {query}, found {len(results)} results")
        return results

    def find_exact_contact(self, first_name, last_name, phone_number):
        """Find a contact by exact first name, last name, and phone number."""
        for contact in self.contacts:
            if (contact.first_name.lower() == first_name.lower() and
                contact.last_name.lower() == last_name.lower() and
                contact.phone_number == phone_number):
                return contact
        return None

    def update_contact(self, first_name, last_name, phone_number, new_contact):
        """Update an existing contact's information."""
        contact = self.find_exact_contact(first_name, last_name, phone_number)
        if contact:
            contact.first_name = new_contact.first_name
            contact.last_name = new_contact.last_name
            contact.phone_number = new_contact.phone_number
            contact.email = new_contact.email
            contact.address = new_contact.address
            contact.update_history(f"Updated contact from {contact}")
            logging.info(f"Updated contact: {contact} to {new_contact}")
            return True
        logging.warning(f"Exact contact to update not found for: {first_name} {last_name} {phone_number}")
        return False

    def delete_contact(self, query):
        """Delete a contact matching the query."""
        results = self.search_contacts(query)
        if results:
            for contact in results:
                self.contacts.remove(contact)
                contact.update_history("Deleted contact")
                logging.info(f"Deleted contact: {contact}")
            return True
        logging.warning(f"Contact to delete not found for query: {query}")
        return False

    def delete_contacts_batch(self, queries):
        
        for query in queries:
            self.delete_contact(query)

    def import_contacts_from_csv(self, file_path):
        """Import contacts from a CSV file."""
        try:
            with open(file_path, mode='r') as file:
                reader = csv.DictReader(file)
                headers = reader.fieldnames

                # Map related headers to expected fields
                header_mapping = {
                    'First Name': ['First Name', 'FirstName', 'first_name', 'firstname'],
                    'Last Name': ['Last Name', 'LastName', 'last_name', 'lastname'],
                    'Phone Number': ['Phone Number', 'PhoneNumber', 'phone_number', 'phonenumber'],
                    'Email': ['Email', 'Email Address', 'email', 'email_address'],
                    'Address': ['Address', 'address', 'Address (Optional)', 'address_optional']
                }

                def get_mapped_header(expected_header):
                    for header in header_mapping[expected_header]:
                        if header in headers:
                            return header
                    return None

                first_name_header = get_mapped_header('First Name')
                last_name_header = get_mapped_header('Last Name')
                phone_number_header = get_mapped_header('Phone Number')
                email_header = get_mapped_header('Email')
                address_header = get_mapped_header('Address')

                if not first_name_header or not last_name_header or not phone_number_header:
                    print("CSV file is missing mandatory headers. Please ensure it includes First Name, Last Name, and Phone Number.")
                    return

                for row in reader:
                    first_name = row.get(first_name_header)
                    last_name = row.get(last_name_header)
                    phone_number = row.get(phone_number_header)
                    email = row.get(email_header, None)
                    address = row.get(address_header, None)
                    try:
                        contact = Contact(first_name, last_name, phone_number, email, address)
                        self.add_contact(contact)
                    except ValueError as e:
                        logging.error(f"Error adding contact from row {row}: {e}")
                        print(f"Error adding contact from row {row}: {e}")
        except FileNotFoundError:
            print("CSV file not found. Please check the file path and try again.")
            logging.error("CSV file not found.")

    def sort_contacts(self, by='first_name'):
        """Sort contacts by first or last name."""
        if by == 'first_name':
            self.contacts.sort(key=lambda contact: contact.first_name.lower())
        elif by == 'last_name':
            self.contacts.sort(key=lambda contact: contact.last_name.lower())
        logging.info(f"Sorted contacts by {by}")

    def group_contacts_by_initial(self, by='last_name'):
        """Group contacts by the first letter of their name."""
        grouped_contacts = {}
        for contact in self.contacts:
            if by == 'first_name':
                initial = contact.first_name[0].upper()
            else:
                initial = contact.last_name[0].upper()
            if initial not in grouped_contacts:
                grouped_contacts[initial] = []
            grouped_contacts[initial].append(contact)
        logging.info(f"Grouped contacts by initial letter of {by}")
        return grouped_contacts

    def view_contact_history(self, contact):
        """Display the history of actions for a contact."""
        print(f"History for {contact.first_name} {contact.last_name}:")
        for entry in contact.history:
            print(entry)

    def filter_contacts_by_date(self, start_date, end_date):
        """Filter contacts created within a specified date range."""
        results = [contact for contact in self.contacts if start_date <= contact.created_at <= end_date]
        logging.info(f"Filtered contacts from {start_date} to {end_date}, found {len(results)} results")
        return results

    def validate_date(self, date_str):
        try:
            return datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            print(f"Invalid date format: {date_str}. Please use YYYY-MM-DD.")
            logging.error(f"Invalid date format: {date_str}")
            return None