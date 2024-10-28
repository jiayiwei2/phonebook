import sys
from phonebook import PhoneBook
from contact import Contact

def main():
    """
    Main function to run the Phone Book Manager application.
    
    This function initializes the PhoneBook instance and provides a command-line 
    interface for users to interact with the phone book, allowing them to perform 
    operations such as adding, searching, viewing, updating, and deleting contacts.
    """
    phonebook = PhoneBook()

    while True:
        # Display the main menu options to the user
        print("\nPhone Book Manager")
        print("[ 1 ] [ + ] Add")
        print("[ 2 ] [ 🔍 ] Search")
        print("[ 3 ] [ 📋 ] View All")
        print("[ 4 ] [ 🔄 ] Update")
        print("[ 5 ] [ ❌ ] Delete")
        print("[ 6 ] [ 📜 ] History")
        print("[ 7 ] [ 🚪 ] Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            # Add contacts option
            print("1. Add a single contact")
            print("2. Import contacts from CSV")
            sub_choice = input("Enter your choice: ")

            if sub_choice == '1':
                # Collect individual contact details
                first_name = input("First Name: ").strip()
                last_name = input("Last Name: ").strip()
                if not first_name or not last_name:
                    print("First Name and Last Name are mandatory. Contact not added.")
                    continue

                phone_number = input("Phone Number: ")
                email = input("Email (Optional): ")
                address = input("Address (Optional): ")
                try:
                    # Create a new Contact instance and add it to the phone book
                    contact = Contact(first_name, last_name, phone_number, email, address)
                    phonebook.add_contact(contact)
                    print("Contact added successfully.")
                except ValueError as e:
                    print(f"Error: {e}")
            elif sub_choice == '2':
                # Import contacts from a CSV file
                try:
                    file_path = input("Enter CSV file path: ")
                    phonebook.import_contacts_from_csv(file_path)
                except KeyboardInterrupt:
                    print("\nOperation cancelled.")
            else:
                print("Invalid choice. Please try again.")
        elif choice == '2':
            # Search contacts option
            print("1. Search Contacts")
            print("2. Filter Contacts by Date")
            sub_choice = input("Enter your choice: ")

            if sub_choice == '1':
                # Perform search based on user query
                query = input("Enter search query: ")
                results = phonebook.search_contacts(query)
                if results:
                    for contact in results:
                        print(contact)
                else:
                    print("No contacts found.")
            elif sub_choice == '2':
                # Filter contacts based on the date range
                start_date = input("Enter start date (YYYY-MM-DD): ")
                end_date = input("Enter end date (YYYY-MM-DD): ")
                start_date = phonebook.validate_date(start_date)
                end_date = phonebook.validate_date(end_date)
                if start_date and end_date:
                    results = phonebook.filter_contacts_by_date(start_date, end_date)
                    if results:
                        for contact in results:
                            print(contact)
                    else:
                        print("No contacts found.")
            else:
                print("Invalid choice. Please try again.")
        elif choice == '3':
            # View and manage all contacts
            print("1. View All Contacts")
            print("2. Sort Contacts")
            print("3. Group Contacts")
            sub_choice = input("Enter your choice: ")

            if sub_choice == '1':
                # Display all contacts
                phonebook.view_contacts()
            elif sub_choice == '2':
                # Sort contacts by user-selected criteria
                print("1. Sort by first name")
                print("2. Sort by last name")
                sort_choice = input("Enter your choice: ")

                if sort_choice == '1':
                    phonebook.sort_contacts(by='first_name')
                    print("Contacts sorted by first name:")
                elif sort_choice == '2':
                    phonebook.sort_contacts(by='last_name')
                    print("Contacts sorted by last name:")
                else:
                    print("Invalid choice. Please try again.")
                    continue

                # Display sorted contacts
                phonebook.view_contacts()
            elif sub_choice == '3':
                # Group contacts by initial letter
                print("1. Group by first name")
                print("2. Group by last name")
                group_choice = input("Enter your choice: ")

                if group_choice == '1':
                    grouped_contacts = phonebook.group_contacts_by_initial('first_name')
                elif group_choice == '2':
                    grouped_contacts = phonebook.group_contacts_by_initial('last_name')
                else:
                    print("Invalid choice. Please try again.")
                    continue
                # Display grouped contacts
                for initial, contacts in grouped_contacts.items():
                    print(f"\nContacts starting with '{initial}':")
                    for contact in contacts:
                        print(contact)
            else:
                print("Invalid choice. Please try again.")
        elif choice == '4':
            # Update a contact
            query = input("Enter the name or phone number of the contact to update: ")
            results = phonebook.search_contacts(query)
            if not results:
                print("Contact not found. No updates were made.")
                continue

            print("Matching contacts found:")
            for index, contact in enumerate(results):
                print(f"[{index}] {contact}")

            try:
                # Get the index of the contact to update
                index = int(input("Enter the index of the contact you want to update: "))
                if index < 0 or index >= len(results):
                    print("Invalid index. No updates were made.")
                    continue
            except ValueError:
                print("Invalid input. Please enter a valid index.")
                continue

            contact_to_update = results[index]
            # Collect new contact details for the update

            new_first_name = input("New First Name: ").strip()
            new_last_name = input("New Last Name: ").strip()
            if not new_first_name or not new_last_name:
                print("First Name and Last Name are mandatory. Update not made.")
                continue

            new_phone_number = input("New Phone Number: ")
            new_email = input("New Email (Optional): ")
            new_address = input("New Address (Optional): ")
            
            # Confirm the update action
            print("\nAre you sure you want to update the contact with the following information?")
            print(f"First Name: {new_first_name}")
            print(f"Last Name: {new_last_name}")
            print(f"Phone Number: {new_phone_number}")
            print(f"Email: {new_email}")
            print(f"Address: {new_address}")
            confirm = input("Enter 'yes' to confirm, or anything else to cancel: ")

            if confirm.lower() == 'yes':
                try:
                    # Create a new contact instance and update it
                    new_contact = Contact(new_first_name, new_last_name, new_phone_number, new_email, new_address)
                    if phonebook.update_contact(contact_to_update.first_name, contact_to_update.last_name, contact_to_update.phone_number, new_contact):
                        print("Contact updated successfully.")
                    else:
                        print("Contact not found. No updates were made.")
                except ValueError as e:
                    print(f"Error: {e}")
            else:
                print("Update canceled.")
        elif choice == '5':
            # Delete a contact
            query = input("Enter the name or phone number of the contact to delete: ")
            results = phonebook.search_contacts(query)
            if not results:
                print("Contact not found. No deletions were made.")
                continue

            print("Matching contacts found:")
            for index, contact in enumerate(results):
                print(f"[{index}] {contact}")

            try:
                # Get the index of the contact to delete
                index = int(input("Enter the index of the contact you want to delete: "))
                if index < 0 or index >= len(results):
                    print("Invalid index. No deletions were made.")
                    continue
            except ValueError:
                print("Invalid input. Please enter a valid index.")
                continue

            contact_to_delete = results[index]
            
            # Confirm the deletion action
            print("\nAre you sure you want to delete the following contact?")
            print(contact_to_delete)
            confirm = input("Enter 'yes' to confirm, or anything else to cancel: ")

            if confirm.lower() == 'yes':
                if phonebook.delete_contact(contact_to_delete.first_name):
                    print("Contact deleted successfully.")
                else:
                    print("Contact not found. No deletions were made.")
            else:
                print("Deletion canceled.")
        elif choice == '6':
            # View contact history
            query = input("Enter the name or phone number of the contact to view history: ")
            results = phonebook.search_contacts(query)
            if not results:
                print("Contact not found.")
                continue

            print("Matching contacts found:")
            for index, contact in enumerate(results):
                print(f"[{index}] {contact}")

            try:
                # Get the index of the contact whose history is to be viewed
                index = int(input("Enter the index of the contact whose history you want to view: "))
                if index < 0 or index >= len(results):
                    print("Invalid index. No history was viewed.")
                    continue
            except ValueError:
                print("Invalid input. Please enter a valid index.")
                continue

            contact_to_view = results[index]
            phonebook.view_contact_history(contact_to_view)
        elif choice == '7':
            sys.exit()
            # Exit the application
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()