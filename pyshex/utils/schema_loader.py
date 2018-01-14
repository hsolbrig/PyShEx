# Copyright (c) 2018, Mayo Clinic
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this
#     list of conditions and the following disclaimer.
#
#     Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions and the following disclaimer in the documentation
#     and/or other materials provided with the distribution.
#
#     Neither the name of the Mayo Clinic nor the names of its contributors
#     may be used to endorse or promote products derived from this software
#     without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, 
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGE.
import re
from typing import cast, Union, TextIO
from urllib.request import urlopen

from ShExJSG import ShExJ
from pyjsg.jsglib import jsg
from pyshexc.parser_impl import generate_shexj


class SchemaLoader:
    def __init__(self, base_location=None, redirect_location=None, schema_format=None) -> None:
        self.base_location = base_location
        self.redirect_location = redirect_location
        self.schema_format=schema_format

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
