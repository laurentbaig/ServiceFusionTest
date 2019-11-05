from flask import make_response, abort
from datetime import datetime
from database import Contact, Email
from peewee import SQL, DoesNotExist, prefetch

# CONTACTS = []
# with open('contacts.csv') as contactsFile:
#     reader = csv.reader(contactsFile, delimiter=',')
#     fields = next(reader)
#     for row in reader:
#         CONTACTS.append(dict(zip(fields, row)))

def get_timestamp():
    return datetime.now().strftime(('%Y-%m-%d %H:%M:%S'))

# Create GET all handler
def index(page=1, pagesize=10, sortby='id', sortdir='asc'):
    """
    /api/contacts
    :return: list of contacts with paging information
    """
    contacts = Contact.select().order_by(SQL(f"{sortby} COLLATE NOCASE {sortdir}")).paginate(page, pagesize)
    emails = Email.select()

    contacts_with_emails_iter = prefetch(contacts, emails)
    data = []
    for contact in contacts_with_emails_iter:
        data.append(
            contact.serialize()
            # {
            #     'id': contact.id,
            #     'fname': contact.fname,
            #     'lname': contact.lname,
            #     'dob': contact.dob,
            #     'emails': [ {'id': em.id, 'email': em.email } for em in contact.emails ]
            # }
        )

    return {
        'data': data,
        'numberRecords': Contact.select().count(),
        'page': page,
        'pagesize': pagesize
    }
    

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

    contact = Contact.create(**{
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
    try:
        contact = Contact.get(Contact.id == oid)
    except StopIteration:
        abort(404, f"Contact with id {oid} not found")

    return contact.serialize()
    # return {
    #     'id': contact.id,
    #     'fname': contact.fname,
    #     'lname': contact.lname,
    #     'dob': contact.dob,
    #     'emails': [ {'id': em.id, 'email': em.email } for em in contact.emails ]
    # }
                    

# create PUT handler
def update(oid, contact):
    """
    Update contact identified by oid

    :param oid:     id of the contact to retrieve
    :param contact: new contact information
    :return:        matching contact
    """
    try:
        theContact = Contact.get(Contact.id == oid)
    except DoesNotExist:
        abort(404, f"Contact with id {oid} not found")

    # update with new information
    upd = {}
    for key in ["fname", "lname", "dob"]:
        value = contact.get(key, None)
        if value is not None:
            upd[key] = value
    theContact.update(**upd)
            
    return theContact.serialize()
    #return {
    #    'id': theContact.id,
    #    'fname': theContact.fname,
    #    'lname': theContact.lname,
    #    'dob': theContact.dob,
    #    'emails': [ {'id': em.id, 'email': em.email } for em in theContact.emails ]
    #}
                    



# create DELETE handler
def delete(oid):
    """
    Delete contact identified by oid

    :param oid:     id of the contact to retrieve
    :param contact: new contact information
    :return:        matching contact
    """
    try:
        contact = Contact.get(Contact.id == oid)
    except DoesNotExist:
        abort(404, f"Contact with id {oid} not found")

    idx = CONTACTS.index(contact)
    del CONTACTS[idx]
    
    return contact.serialize()
    # return {
    #     'id': contact.id,
    #     'fname': contact.fname,
    #     'lname': contact.lname,
    #     'dob': contact.dob,
    #     'emails': [ {'id': em.id, 'email': em.email } for em in contact.emails ]
    # }

