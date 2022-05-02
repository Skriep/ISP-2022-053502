from myserializer.packer import Packer


def test_dict():
    mydict = {
        'key': 'value',
        123: 456,
        12.3: 4.56,
        1.4j + 3: "that's complex!",
        (1, 2, 3): (4, 5, 6)
    }
    packed = Packer.pack(mydict)
    unpacked = Packer.unpack(packed)
    assert all(unpacked[key] == value for key, value in mydict.items())
