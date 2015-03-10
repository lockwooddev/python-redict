from __future__ import absolute_import

import json

from redict.base import BaseRemapper
from redict import utils


class JsonRemapper(BaseRemapper):

    def pre_processor(self, data):
        return json.loads(data)

    def post_processor(self, data):
        json_string = json.dumps(data)
        if self.kwargs.get('minify', False):
            return utils.json_minify(json_string)
        return json_string
