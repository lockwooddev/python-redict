from redict import BaseRemapper


class TestBaseMapper:

    def setup(self):
        self.data = {
            'aaa': {
                'aaa': [
                    {'aaa': 1, 'bbb': [5, 6], 'ccc': 8, 'ddd': {'eee': None}, 'fff': True},
                    [],
                    {'aaa': 1, 'bbb': [], 'ccc': 8, 'ddd': {}, 'fff': True},
                    {},
                ]
            },
            'bbb': 3,
            'ccc': [1],
            'ddd': {
                'eee': {
                    'fff': False
                }
            }
        }

    def test_init_without_keymap(self):
        instance = BaseRemapper({'a': 1})
        assert instance.data == {'a': 1}
        assert instance.kwargs == {}

    def test_init_with_keymap(self):
        instance = BaseRemapper({'a': 1}, keymap={})
        assert instance.data == {'a': 1}
        assert instance.kwargs == {'keymap': {}}

    def test_call_instance_without_keymap(self):
        instance = BaseRemapper(self.data)
        assert self.data == instance()

    def test_keymap(self):
        data = {
            'aaa': {
                'aaa': [
                    {'aaa': 1, 'bbb': [5, 6], 'ccc': 8, 'ddd': {'eee': None}, 'fff': True},
                    [],
                    {'aaa': 1, 'bbb': [], 'ccc': 8, 'ddd': {}, 'fff': True},
                    {},
                ]
            },
            'bbb': 3,
            'ccc': [1],
            'ddd': {
                'eee': {
                    'fff': False
                }
            }
        }

        keymap = {'aaa': 'a'}

        instance = BaseRemapper(data, keymap=keymap)
        keys = instance.build_keys()

        expected_keys = {
            'aaa': 1,
            'aaa.aaa': 0,
            'aaa.aaa.0': 1,
            'aaa.aaa.0.fff': 2,
            'aaa.aaa.0.aaa': 2,
            'aaa.aaa.0.bbb': 0,
            'aaa.aaa.0.bbb.0': 2,
            'aaa.aaa.0.bbb.1': 2,
            'aaa.aaa.0.ccc': 2,
            'aaa.aaa.0.ddd': 1,
            'aaa.aaa.0.ddd.eee': 2,

            'aaa.aaa.1': 0,

            'aaa.aaa.2': 1,
            'aaa.aaa.2.fff': 2,
            'aaa.aaa.2.aaa': 2,
            'aaa.aaa.2.bbb': 0,
            'aaa.aaa.2.ccc': 2,
            'aaa.aaa.2.ddd': 1,

            'aaa.aaa.3': 1,

            'bbb': 2,

            'ccc': 0,
            'ccc.0': 2,

            'ddd': 1,
            'ddd.eee': 1,
            'ddd.eee.fff': 2,
        }

        assert expected_keys == keys

    def test_call_instance_with_keymap(self):
        keymap = {
            'aaa': 'a',
            'bbb': 'b',
            'ccc': 'c',
            'ddd': 'd',
            'eee': 'e',
            'fff': 'f',
        }

        instance = BaseRemapper(self.data, keymap=keymap)
        result = instance()

        assert result == {
            'a': {
                'a': [
                    {'a': 1, 'c': 8, 'b': [5, 6], 'd': {'e': None}, 'f': True},
                    [],
                    {'a': 1, 'c': 8, 'b': [], 'd': {}, 'f': True},
                    {}
                ]
            },
            'c': [1],
            'b': 3,
            'd': {
                'e': {
                    'f': False
                }
            }
        }
