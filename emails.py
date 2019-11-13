from flask import make_response, abort
from database import Contact, Email
from peewee import SQL, DoesNotExist


def index(cid):
    """
    /api/contacts/{cid}/emails
    :return: list of a contact's emails
    """
    contact = Contact.get(Contact.id == cid)

    emails = []
    for email in contact.emails:
        emails.append(email.serialize())

    return emails


def create(cid, email):
    """
    /api/contacts/{cid}/emails
    Create new contact email
    
    :param email: email information
    :return:      matching email
    """
    emailAddress = email.get("email", None)

    if emailAddress is None:
        abort(406, "Email field must not be empty")

    model = Email.create(**{
        'email': emailAddress,
        'contact_id': cid
    })

    return make_response(f"{emailAddress} successfully created for contact {cid}", 201)


def update(eid, email):
    """
    /api/emails/{eid}
    Update email identified by eid
   
    :param eid:    id of the email to retrieve
    :param email:  new email information
    :return:       the new email information
    """
    try:
        theEmail = Email.get(Email.id == eid)
    except DoesNotExist:
        abort(404, f"Email with ie {eid} for contact {cid} not found")
    theEmail.email = email.get("email")
    theEmail.save()

    return theEmail.serialize()


def delete(eid):
    """
    /api/emails/{eid}
    Delete email identified by eid

    :param eid:    new contact information
    :return:       the deleted email
    """
    try:
        email = Email.get(Email.id == eid)
    except:
        abort(404, f"Email with id {eid} not found")

    email.delete_instance()

    return email.serialize()
    
