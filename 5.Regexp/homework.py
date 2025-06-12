import csv
import re
from pprint import pprint

with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

contacts_dict = {}

for contact in contacts_list[1:]:
    full_name = ' '.join(contact[:3]).split()
    lastname = full_name[0] if len(full_name) > 0 else ''
    firstname = full_name[1] if len(full_name) > 1 else ''
    surname = full_name[2] if len(full_name) > 2 else ''

    key = (lastname, firstname)

    phone = contact[5]
    if phone:
        phone = re.sub(r'[^0-9]', '', phone)
        if len(phone) == 11:
            phone = re.sub(r'^(\d{1})(\d{3})(\d{3})(\d{2})(\d{2})',
                           r'+7(\2)\3-\4-\5', phone)
        elif len(phone) > 11:
            phone = re.sub(r'^(\d{1})(\d{3})(\d{3})(\d{2})(\d{2})(\d+)',
                           r'+7(\2)\3-\4-\5 доб.\6', phone)

    if key in contacts_dict:
        existing_contact = contacts_dict[key]
        if not existing_contact[2] and surname:
            existing_contact[2] = surname
        if not existing_contact[3] and contact[3]:
            existing_contact[3] = contact[3]
        if not existing_contact[4] and contact[4]:
            existing_contact[4] = contact[4]
        if not existing_contact[5] and phone:
            existing_contact[5] = phone
        if not existing_contact[6] and contact[6]:
            existing_contact[6] = contact[6]
    else:
        contacts_dict[key] = [
            lastname,
            firstname,
            surname,
            contact[3],
            contact[4],
            phone,
            contact[6]
        ]

processed_list = [contacts_list[0]]
processed_list.extend(contacts_dict.values())

with open("phonebook.csv", "w", encoding="utf-8", newline='') as f:
    writer = csv.writer(f, delimiter=',')
    writer.writerows(processed_list)

pprint(processed_list)