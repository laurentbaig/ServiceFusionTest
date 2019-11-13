from peewee import *

DATABASE = './app.db'

database = SqliteDatabase(DATABASE)

class BaseModel(Model):
    class Meta:
        database = database
        
class Contact(BaseModel):
    id = AutoField()
    fname = CharField()
    lname = CharField()
    dob = DateField()

    def serialize(self):
        return {
            'id': self.id,
            'fname': self.fname,
            'lname': self.lname,
            'dob': self.dob,
            'emails': [ {'id': em.id, 'email': em.email } for em in self.emails ],
            'phones': [ {'id': ph.id, 'phone': ph.phone } for ph in self.phones ]
        }
    
class Address(BaseModel):
    id = AutoField()
    contact = ForeignKeyField(Contact, backref='addresses')
    full_address = CharField()
    # address1 = CharField()
    # address2 = CharField()
    # city = CharField()
    # state = CharField()
    # zip = CharField()
    # country = CharField()

    def serialize(self):
        return {
            'id': self.id,
            'contact_id': self.contact_id,
            'full_address': self.full_address
        }
    

class Email(BaseModel):
    id = AutoField()
    contact = ForeignKeyField(Contact, backref='emails')
    email = CharField()

    def serialize(self):
        return {
            'id': self.id,
            'contact_id': self.contact_id,
            'email': self.email
        }

class Phone(BaseModel):
    id = AutoField()
    contact = ForeignKeyField(Contact, backref='phones')
    phone = CharField()

    def serialize(self):
        return {
            'id': self.id,
            'contact_id': self.contact_id,
            'phone': self.phone
        }

if __name__ == '__main__':
    import sys
    import csv

    if '--create' in sys.argv:
        with database:
            database.create_tables([Contact, Email, Phone, Address])

    elif '--drop' in sys.argv:
        with database:
            database.drop_tables([Contact, Email, Phone, Address])

    elif '--seed' in sys.argv:
        def seed(fileName, obj):
            print(fileName)
            with open(fileName) as file:
                reader = csv.reader(file, delimiter=',')
                fields = next(reader)
                for row in reader:
                    d = dict(zip(fields, row))
                    obj.create(**d)

        for fname in [ ['contacts.csv', Contact],
                       ['emails-1.csv', Email],
                       ['emails-2.csv', Email],
                       ['emails-3.csv', Email]
                       ]:
            seed(*fname)
        

    else:
        print('--create: creates database tables')
        print('--drop: drop all database tables')
        print('--seed: seed database tables')
        
