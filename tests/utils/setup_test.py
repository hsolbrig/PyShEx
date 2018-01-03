# Copyright (c) 2017, Mayo Clinic
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
from typing import Tuple, Optional

from ShExJSG import ShExJ
from pyjsg.jsglib import jsg
from rdflib import Graph, RDF, RDFS, XSD, Namespace
from rdflib.namespace import FOAF

from pyshex.shape_expressions_language.p5_context import Context

EX = Namespace("http://schema.example/")
INST = Namespace("http://inst.example/#")

rdf_header = f"""
prefix ex: <{EX}>
prefix : <{EX}>
prefix rdf: <{RDF}>
prefix rdfs: <{RDFS}>
prefix xsd: <{XSD}>
prefix inst: <{INST}>
prefix foaf: <{FOAF}>
"""


def setup_context(shex_str: str, rdf_str: Optional[str]):
    schema, g = setup_test(shex_str, rdf_str)
    if g is None:
        g = Graph()
        g.parse(rdf_header)
    return Context(g, schema)


def setup_test(shex_str: Optional[str], rdf_str: Optional[str]) -> Tuple[Optional[ShExJ.Schema], Optional[Graph]]:
    schema: ShExJ.Schema = jsg.loads(shex_str, ShExJ, strict=False) if shex_str else None
    if rdf_str:
        g = Graph()
        g.parse(data=rdf_str, format="turtle")
    else:
        g = None
    return schema, g


def gen_rdf(rdf_fragment: str) -> str:
    """ Edit rdf_fragment from the spec to be complete. We
    1) Add the rdf header and
    2) convert relative URI's into URI's based in the default space """
    return f"""{rdf_header}""" + re.sub(r'<([^.:>]+)>', r':\1', rdf_fragment)
