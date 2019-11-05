from flask import make_response, abort
from database import Contact, Email
from peewee import SQL

def index(oid, page=1, pagesize=10, sortBy='id', order='asc'):
    """
    /api/contacts/{oid}/emails
    :return: list of a contact's emails
    """
    contact = Contact.get(Contact.id == oid)

    emails = []
    try: 
        emails = contact.emails
    except DoesNotExist:
        emails = []

    return {
        'emails': emails
    }
    
