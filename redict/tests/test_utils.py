import json
import textwrap

from redict import utils


class JsonMinifyTestCase:

    def template(self, json_string, expected):
        in_dict = json.loads(utils.json_minify(json_string))
        expected_dict = json.loads(expected)
        assert in_dict == expected_dict

    def test_1(self):
        json_string = textwrap.dedent('''
            // this is a JSON file with comments
            {
                "foo": "bar",    // this is cool
                "bar": [
                    "baz", "bum"
                ],
            /* the rest of this document is just fluff
               in case you are interested. */
                "something": 10,
                "else": 20
            }

            /* NOTE: You can easily strip the whitespace and comments
               from such a file with the JSON.minify() project hosted
               here on github at http://github.com/getify/JSON.minify
            */''')

        self.template(
            json_string,
            '{"foo":"bar","bar":["baz","bum"],"something":10,"else":20}'
        )

    def test_2(self):
        self.template(textwrap.dedent(
            '{"/*":"*/","//":"",/*"//"*/"/*/"://"//"}'),
            '{"/*":"*/","//":"","/*/":"//"}'
        )

    def test_3(self):
        json_string = textwrap.dedent(
            r'''
            /*
            this is a
            multi line comment */{

            "foo"
            :
                "bar/*"// something
                ,    "b\"az":/*
            something else */"blah"

            }
            '''
        )
        self.template(
            json_string,
            r'{"foo":"bar/*","b\"az":"blah"}'
        )

    def test_4(self):
        self.template(textwrap.dedent(
            r'''{"foo": "ba\"r//", "bar\\": "b\\\"a/*z", "baz\\\\": /* yay */ "fo\\\\\"*/o"}'''),
            r'{"foo":"ba\"r//","bar\\":"b\\\"a/*z","baz\\\\":"fo\\\\\"*/o"}'
        )
