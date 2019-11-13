from flask import make_response, abort
from datetime import datetime
from database import Contact, Email, Phone
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
def index(page=1, pagesize=10, sortby='id', sortdir='asc', search=None):
    """
    /api/contacts
    :return: list of contacts with paging information
    """
    if search is not None:
        return searchContacts(search)

    contacts = Contact.select().order_by(
        SQL(f"{sortby} COLLATE NOCASE {sortdir}")
    ).paginate(page, pagesize)
    emails = Email.select()
    phones = Phone.select()

    contacts_with_emails_iter = prefetch(contacts, emails, phones)
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
    
def searchContacts(searchString):
    print(searchString)
    if len(searchString.split()) > 1:
        first, last = searchString.split()
        contacts = Contact.select().where((Contact.fname.contains(first)) &
                                          (Contact.lname.contains(last)))
    else:
        contacts = Contact.select().where(Contact.fname.contains(searchString))

    returnList = []
    for c in contacts[:25]:
        returnList.append(c.serialize())

    return {
        'data': returnList,
        'numberRecords': len(returnList),
        'page': 1,
        'pagesize': 25
    }
        

def create(contact):
    """
    Create new contact

    :param contact: contact information
    :return:    matching contact
    """
    print(contact)
    fname = contact.get("fname", None)
    lname = contact.get("lname", None)
    dob = contact.get("dob", None)
    # emails = contact.get("emails", [])

    if fname is None or lname is None or dob is None:
        abort(406, f"Entries must not be empty")

    contact = Contact.create(**{
        'fname': fname,
        'lname': lname,
        'dob': dob[:10]
    })

    # if len(emails) > 0:
    #     for email in emails:
    #         Email.create(**{
    #             'contact_id': contact.id,
    #             'email': email
    #         })

    # return make_response(f"{fname} {lname} successfully created", 201)
    return contact.serialize()


# create GET one handler
def read(cid):
    """
    Read one contact identified by cid

    :param cid: id of the contact to retrieve
    :return:    matching contact
    """
    try:
        contact = Contact.get(Contact.id == cid)
    except StopIteration:
        abort(404, f"Contact with id {cid} not found")

    return contact.serialize()


# create PUT handler
def update(cid, contact):
    """
    Update contact identified by cid

    :param cid:     id of the contact to retrieve
    :param contact: new contact information
    :return:        matching contact
    """
    try:
        theContact = Contact.get(Contact.id == cid)
    except DoesNotExist:
        abort(404, f"Contact with id {cid} not found")

    # update with new information
    print(contact)
    theContact.fname = contact.get('fname')
    theContact.lname = contact.get('lname')
    theContact.dob = contact.get('dob')
    theContact.save()
            
    return theContact.serialize()



# create DELETE handler
def delete(cid):
    """
    Delete contact identified by cid

    :param cid:     id of the contact to retrieve
    :param contact: new contact information
    :return:        matching contact
    """
    try:
        contact = Contact.get(Contact.id == cid)
    except DoesNotExist:
        abort(404, f"Contact with id {cid} not found")

    contact.delete_instance(recursive=True)
    
    return contact.serialize()

