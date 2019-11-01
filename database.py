from peewee import SqliteDatabase, Model

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
    
class Email(BaseModel):
    id = AutoField()
    contactId = ForeignKeyField(Contact, backref='emails')
    email = CharField()

class Phone(BaseModel):
    id = AutoField()
    contactId = ForeignKeyField(Contact, backref='phones')
    phone = CharField()
    
    
def create_tables():
    with database:
        database.create_tables([Contact])
