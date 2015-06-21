import collections
import copy


class BaseRemapper(object):

    def __init__(self, data, **kwargs):
        self.data = copy.deepcopy(data)
        self.kwargs = kwargs

    def __call__(self):
        self.data = self.pre_processor(self.data)
        keys = self.build_keys()
        remapped_dict = self.rewrite_keys(keys)
        return self.post_processor(remapped_dict)

    def get_keymap(self):
        '''
        Get keymap from constructor kwargs
        '''
        return self.kwargs.get('keymap', {})

    def pre_processor(self, data):
        '''
        Pre-process orginal data
        '''
        return data

    def post_processor(self, data):
        '''
        Post-process remapped data
        '''
        return data

    def build_lookup(self, lookup, key):
        '''
        Append key to previous lookup if available else just return key
        '''
        if lookup:
            return '.'.join([lookup, key])
        return key

    def type_id(self, value):
        '''
        Return type identifier, list, dict or value
        '''
        if isinstance(value, list):
            return 0
        elif isinstance(value, dict):
            return 1
        return 2

    def build_keys(self):
        '''
        This method will walk the entire data dict and create a dict of keys with
        corresponding type

        {'key1.key2.0': 0}
        '''
        keys = collections.OrderedDict()

        def walk_keys(data, lookup=''):
            if not data:
                return True

            if isinstance(data, list):
                for i, obj in enumerate(data):
                    list_index = self.build_lookup(lookup, str(i))
                    keys[list_index] = self.type_id(obj)
                    walk_keys(obj, list_index)

            elif isinstance(data, dict):
                key_count = 0
                key_len = len(data)
                for key, value in data.items():
                    _type_id = self.type_id(value)
                    previous_lookup = lookup

                    if _type_id == 0 or _type_id == 1:
                        lookup = self.build_lookup(lookup, key)
                        keys[lookup] = _type_id
                        is_empty = walk_keys(value, lookup)
                        if is_empty:
                            lookup = previous_lookup
                        else:
                            # if not reached end of keys
                            if key_count < (key_len - 1):
                                lookup = previous_lookup
                            else:
                                lookup = ''

                    else:
                        keys[self.build_lookup(lookup, key)] = _type_id
                    key_count += 1
                key_count = 0

        # Run inner method
        walk_keys(self.data)
        return keys

    def is_int(self, string):
        '''
        Checks if string can be converted to int and returns boolean
        '''
        try:
            int(string)
            return True
        except ValueError:
            return False

    def remap_keys(self, keys):
        '''
        Maps keys list to new key map
        '''
        key_map = self.get_keymap()
        return [key_map.get(key, key) for key in keys]

    def alter_key(self, key):
        '''
        Use is_int and convert if string can be converted to int
        '''
        return int(key) if self.is_int(key) else key

    def walk_into(self, _dict, key):
        '''
        Recursively walks dictionary keys
        '''
        head, _, tail = key.partition('.')

        # Convert to int if key consists of number chars
        key = self.alter_key(key)
        if tail:
            # Convert to int if key consists of number chars
            head = self.alter_key(head)
            return self.walk_into(_dict[head], tail)
        return _dict[key]

    def rewrite_keys(self, keys):
        '''
        Builds a dictionary with the remapped keys, but original data
        '''
        container_types = {0: [], 1: {}}
        remapped_dict = {}

        for key, _type in keys.items():
            unpacked_keys = key.split(".")
            remapped_keys = self.remap_keys(unpacked_keys)

            # If head of the dict
            if len(remapped_keys) == 1:
                dict_ref = remapped_dict

            # If tail of the dict, generate key to be walked from parent keys
            # except last key. The key will be used to recursively walk trough
            # the dict till the end is reached and then returned as reference to
            # the new remapped_dict dict.
            else:
                walker_key = '.'.join(remapped_keys[:-1])
                dict_ref = self.walk_into(remapped_dict, walker_key)

            # The renamed new key to be set instead of the original key
            new_key = remapped_keys[-1]

            # If type is list or dict.
            if _type in container_types:

                # If integer key as string, append container type to list
                if self.is_int(new_key):
                    dict_ref.append(copy.deepcopy(container_types[_type]))
                # If string key, set container type to key
                else:
                    dict_ref[new_key] = copy.deepcopy(container_types[_type])

            else:
                if self.is_int(new_key):
                    # If integer key as string, append value to list
                    dict_ref.append(self.walk_into(self.data, key))
                else:
                    # If string key, set key and value
                    dict_ref[new_key] = self.walk_into(self.data, key)
        return remapped_dict
