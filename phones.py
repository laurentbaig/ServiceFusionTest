from flask import make_response, abort
from database import Contact, Email, Phone
from peewee import SQL, DoesNotExist


def index(cid):
    """
    /api/contacts/{cid}/phones
    :return: list of a contact's phones
    """
    contact = Contact.get(Contact.id == cid)

    phones = []
    for phone in contact.phones:
        phones.append(phone.serialize())

    return phones


def create(cid, phone):
    """
    /api/contacts/{cid}/phones
    Create new contact phone
    
    :param phone: phone information
    :return:      matching phone
    """
    phoneNumber = phone.get("phone", None)

    if phoneNumber is None:
        abort(406, "Phone field must not be empty")

    model = Phone.create(**{
        'phone': phoneNumber,
        'contact_id': cid
    })

    return make_response(f"{phoneNumber} successfully created for contact {cid}", 201)


def update(pid, phone):
    """
    /api/phones/{pid}
    Update phone identified by pid
   
    :param pid:    id of the phone to retrieve
    :param phone:  new phone information
    :return:       the new phone information
    """
    try:
        thePhone = Phone.get(Phone.id == pid)
    except DoesNotExist:
        abort(404, f"Phone with id {pid} not found")
    thePhone.phone = phone.get("phone")
    thePhone.save()

    return thePhone.serialize()


def delete(pid):
    """
    /api/phones/{pid}
    Delete phone identified by pid

    :param pid:    the id of the phone to be deleted
    :return:       the deleted phone
    """
    try:
        phone = Phone.get(Phone.id == pid)
    except:
        abort(404, f"Phone with id {pid} not found")

    phone.delete_instance()

    return phone.serialize()

