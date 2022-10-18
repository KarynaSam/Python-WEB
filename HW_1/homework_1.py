from abc import abstractmethod, ABC
import json
import pickle


class SerializationInterface(ABC):

    @abstractmethod
    def save_file(self, data, file):
        pass

    @abstractmethod
    def read_file(self, file):
        pass


class SerializeJSON(SerializationInterface):

    def save_file(self, data, file):
        with open(file, 'w') as fh:
            json.dump(data, fh)

    def read_file(self, file):
        with open(file, 'r') as fh:
            return json.load(fh)


class SerializeBIN(SerializationInterface):

    def save_file(self, data, file):
        with open(file, 'wb') as fh:
            pickle.dump(data, fh)

    def read_file(self, file):
        with open(file, 'rb') as fh:
            return pickle.load(fh)


class Meta(type):

    def __new__(cls, name, bases, attrs):
        attrs['class_number'] = Meta.class_number
        Meta.class_number += 1
        return super().__new__(cls, name, bases, attrs)


Meta.class_number = 0


class Cls1(metaclass=Meta):

    def __init__(self, data):

        self.data = data


class Cls2(metaclass=Meta):

    def __init__(self, data):

        self.data = data


json_s = SerializeJSON()
json_s.save_file({'Name': 'Karyna Samoilenko', 'Age': 24}, 'data.json')
print(json_s.read_file('data.json'))
bin_s = SerializeBIN()
bin_s.save_file({'Name': 'Karyna Samoilenko', 'Age': 24}, 'data.bin')
print(bin_s.read_file('data.bin'))

assert (Cls1.class_number, Cls2.class_number) == (0, 1)
a, b = Cls1(''), Cls2('')
assert (a.class_number, b.class_number) == (0, 1)