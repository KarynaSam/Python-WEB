from mongoengine import connect, Document, StringField, ListField, ReferenceField

connect(host='mongodb+srv://Module9:wLcuUrRbu7CK2Y3d@eridas.p3ye6ga.mongodb.net/?retryWrites=true&w=majority')


class Author(Document):
    fullname = StringField(required=True)
    date_born = StringField()
    born_location = StringField()
    bio = StringField()


class Quotes(Document):
    author = ReferenceField(Author)
    tags = ListField(StringField())
    quote = StringField(required=True)