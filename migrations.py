from models import db, Contact
from faker import Factory

fake = Factory.create()
# Spanish
#fake = Factory.create('es_ES')
# Reload tables
db.drop_all()
db.create_all()
print("executed")
# Make 100 fake contacts
# for num in range(2):
#     fullname = fake.name().split()
#     name = fullname[0]
#     surname = ' '.join(fullname[1:])
#     #email = fake.email()
#     #phone = fake.phone_number()
#     # Save in database
#     mi_contacto = Contact(name=name, surname=surname)
#     db.session.add(mi_contacto)

db.session.commit()
