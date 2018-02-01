import re
from typing import cast, Union, TextIO
from urllib.request import urlopen

from ShExJSG import ShExJ
from pyjsg.jsglib import jsg
from pyshexc.parser_impl import generate_shexj


class SchemaLoader:
    def __init__(self, base_location=None, redirect_location=None, schema_type_suffix=None, base_uri=None) -> None:
        """ ShEx Schema loader, with the ability to redirect URI's to local directories or other URL's

        :param base_location: Location base supplied to `load` function
        :param redirect_location: Location to replace base for actual load
        :param schema_type_suffix: Replace schema file type suffix with this
        :param base_uri: Base URI to add to the schema before parsing for relative URI's
        """
        self.base_location = base_location
        self.redirect_location = redirect_location
        self.schema_format=schema_type_suffix
        self.base_uri = base_uri

    def load(self, schema_location: Union[str, TextIO]) -> ShExJ.Schema:
        """ Load a ShEx Schema from schema_location

        :param schema_location:  name or file-like object to deserialize
        :return: ShEx Schema represented by schema_location
        """
        if isinstance(schema_location, str):
            real_schema_location = self.location_rewrite(schema_location)
            if ':' in real_schema_location:
                schema_txt = urlopen(real_schema_location).read().decode()
            else:
                with open(real_schema_location) as schema_file:
                    schema_txt = schema_file.read()
        else:
            schema_txt = schema_location.read()
        return self.loads(schema_txt)

    @staticmethod
    def loads(schema_txt: str) -> ShExJ.Schema:
        """ Parse and return schema as a ShExJ Schema

        :param schema_txt: ShExC or ShExJ representation of a ShEx Schema
        :return: ShEx Schema representation of schema
        """
        if schema_txt.strip()[0] == '{':
            return cast(ShExJ.Schema, jsg.loads(schema_txt, ShExJ))
        else:
            return generate_shexj.parse(schema_txt)

    def location_rewrite(self, schema_location: str) -> str:
        rval = schema_location.replace(self.base_location, self.redirect_location) \
            if self.base_location and schema_location.startswith(self.base_location) else schema_location
        if self.schema_format:
            rval = re.sub(r'\.[^.]+?(tern)?$',f'.{self.schema_format}\\1', rval)
        return rval
