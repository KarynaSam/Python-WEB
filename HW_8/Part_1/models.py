from mongoengine import connect, Document, StringField, ListField, CASCADE, ReferenceField

connect(host='mongodb+srv://Module9:wLcuUrRbu7CK2Y3d@eridas.p3ye6ga.mongodb.net/?retryWrites=true&w=majority')


class Author(Document):
    fullname = StringField(required=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()


class Quotes(Document):
    author = ReferenceField(Author)
    tags = ListField(StringField())
    quote = StringField(required=True)
