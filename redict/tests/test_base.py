from redict import BaseRemapper


class TestBaseMapper:

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

    def test_init_without_keymap(self):
        instance = BaseRemapper({'a': 1})
        assert instance.data == {'a': 1}
        assert instance.kwargs == {}

    def test_init_with_keymap(self):
        instance = BaseRemapper({'a': 1}, keymap={})
        assert instance.data == {'a': 1}
        assert instance.kwargs == {'keymap': {}}

    def test_call_instance_with_keymap(self):
        keymap = {
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

        instance = BaseRemapper(self.data, keymap=keymap)
        result = instance()

        assert result == {
            'a': {
                'b': [
                    {
                        'c': [
                            {
                                'e': {},
                                'd': 123,
                                'g': [],
                                'f': 1.0
                            },
                            {},
                            {
                                'e': {},
                                'd': 456,
                                'g': [],
                                'f': 2.0
                            },
                            []
                        ]
                    }
                ]
            },
            'h': None,
            'i': 'name'
        }

    def test_call_instance_with_identical_keys(self):

        data = {
            'aaa': {
                'aaa': [
                    {
                        'aaa': [
                            1, 2, 3, 4, {'aaa': 1, 'bbb': {'aaa': 1.0}}, 5, [1, 2], 6
                        ],
                    },
                ]
            },
        }

        keymap = {'aaa': 'a'}

        instance = BaseRemapper(data, keymap=keymap)
        result = instance()

        assert result == {
            'a': {
                'a': [
                    {
                        'a': [
                            1, 2, 3, 4, {'a': 1, 'bbb': {'a': 1.0}}, 5, [1, 2], 6
                        ],
                    },
                ]
            },
        }

    def test_call_instance_without_keymap(self):
        instance = BaseRemapper(self.data)
        assert self.data == instance()
