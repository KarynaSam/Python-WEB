from mongoengine import connect, Document, StringField, BooleanField

connect(host='mongodb+srv://Module9:wLcuUrRbu7CK2Y3d@eridas.p3ye6ga.mongodb.net/?retryWrites=true&w=majority')


class Client(Document):
    fullname = StringField(required=True)
    email = StringField()
    phone = StringField()
    address = StringField()
    sent_message = BooleanField()
    best_method = StringField()