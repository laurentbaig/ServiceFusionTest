from flask import make_response, abort
from datetime import datetime
import csv

CONTACTS = []
with open('contacts.csv') as contactsFile:
    reader = csv.reader(contactsFile, delimiter=',')
    fields = next(reader)
    for row in reader:
        CONTACTS.append(dict(zip(fields, row)))

def get_timestamp():
    return datetime.now().strftime(('%Y-%m-%d %H:%M:%S'))

# Create GET all handler
def index():
    """
    /api/contacts
    :return: list of people
    """
    global CONTACTS
    
    return CONTACTS


def create(contact):
    """
    Create new contact

    :param contact: contact information
    :return:    matching contact
    """
    fname = contact.get("fname", None)
    lname = contact.get("lname", None)
    dob = contact.get("dob", None)

    if fname is None or lname is None or dob is None:
        abort(406, f"Entries must not be empty")
        
    try:
        contact = next(filter(lambda x: x['fname'] == fname and x['lname'] == lname, CONTACTS))
        abort(406, f"Contact '{fname} {lname}' already exists")
    except StopIteration:
        pass

    maxId = max(map(lambda x: x['id'], CONTACTS))
    CONTACTS.append({
        'id': maxId + 1,
        'fname': fname,
        'lname': lname,
        'dob': dob
        })
            
    return make_response(f"{fname} {lname} successfully created", 201)


# create GET one handler
def read(oid):
    """
    Read one contact identified by oid

    :param oid: id of the contact to retrieve
    :return:    matching contact
    """
    global CONTACTS
    
    try:
        contact = next(filter(lambda x: x['id'] == str(oid), CONTACTS))
    except StopIteration:
        abort(404, f"Contact with id {oid} not found")

    return contact
                    

# create PUT handler
def update():
    #
    return


# create DELETE handler
def delete():
    #
    return

