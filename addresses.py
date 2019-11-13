from flask import make_response, abort
from database import Contact, Address
from peewee import SQL, DoesNotExist


def index(cid):
    """
    /api/contacts/{cid}/addresses
    :return: list of a contact's addresses
    """
    contact = Contact.get(Contact.id == cid)

    addresses = []
    for address in contact.addresses:
        addresses.append(address.serialize())

    return addresses


def create(cid, address):
    """
    /api/contacts/{cid}/addresses
    Create new contact address
    
    :param address: address information
    :return:        matching address
    """
    theAddress = address.get("address", None)

    if theAddress is None:
        abort(406, "Address field must not be empty")

    model = Address.create(**{
        'full_address': theAddress,
        'contact_id': cid
    })

    return make_response(f"{theAddress} successfully created for contact {cid}", 201)


def update(aid, address):
    """
    /api/addresses/{aid}
    Update address identified by aid
   
    :param aid:     id of the address to retrieve
    :param address: new address information
    :return:       the new address object
    """
    try:
        theAddress = Address.get(Address.id == aid)
    except DoesNotExist:
        abort(404, f"Address with id {aid} for contact {cid} not found")
    theAddress.full_address = address.get("address")
    theAddress.save()

    return theAddress.serialize()


def delete(aid):
    """
    /api/addresses/{aid}
    Delete addresses identified by aid

    :param aid:    new address information
    :return:       the deleted address
    """
    try:
        address = Address.get(Address.id == aid)
    except:
        abort(404, f"Email with id {aid} not found")

    address.delete_instance()

    return address.serialize()
    
