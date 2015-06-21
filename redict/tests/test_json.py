import json

from redict import JsonRemapper


class TestJsonRemapper:

    def setup(self):
        self.data = {
            'aaa': {
                'bbb': [
                    {
                        'ccc': [
                            {
                                'ddd': 123,
                                'eee': {},
                                'fff': 1.0,
                                'ggg': [],
                            },
                            {},
                            {
                                'ddd': 456,
                                'eee': {},
                                'fff': 2.0,
                                'ggg': [],
                            },
                            [],
                        ],
                    },
                ]
            },
            'hhh': None,
            'iii': 'name'
        }

        self.json_data = json.dumps(self.data)

        self.keymap = {
            'aaa': 'a',
            'bbb': 'b',
            'ccc': 'c',
            'ddd': 'd',
            'eee': 'e',
            'fff': 'f',
            'ggg': 'g',
            'hhh': 'h',
            'iii': 'i',
        }

    def test_remap_json_without_keymap(self):
        instance = JsonRemapper(self.json_data)
        assert self.json_data == instance()

    def test_remap_json_with_keymap(self):
        instance = JsonRemapper(self.json_data, keymap=self.keymap)
        result = instance()
        expected = (
            '{"a": {"b": [{"c": [{"e": {}, "d": 123, "g": [], "f": 1.0}, {}, '
            '{"e": {}, "d": 456, "g": [], "f": 2.0}, []]}]}, "h": null, "i": "name"}'
        )
        assert json.loads(expected) == json.loads(result)

    def test_remap_json_with_minifier(self):
        instance = JsonRemapper(self.json_data, keymap=self.keymap, minify=True)
        result = instance()
        expected = (
            '{"a":{"b":[{"c":[{"e":{},"d":123,"g":[],"f":1.0},{},'
            '{"e":{},"d":456,"g":[],"f":2.0},[]]}]},"h":null,"i":"name"}'
        )
        assert json.loads(expected) == json.loads(result)
