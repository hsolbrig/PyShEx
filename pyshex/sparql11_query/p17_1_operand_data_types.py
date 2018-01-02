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
from typing import cast, Union

from rdflib import Literal, XSD, URIRef, BNode
from rdflib.term import Node


def is_typed_literal(n: Node) -> bool:
    return isinstance(n, Literal) and n.datatype is not None


def is_plain_literal(n: Node) -> bool:
    return isinstance(n, Literal) and n.datatype is None


def is_strict_numeric(n: Node) -> bool:
    """ numeric denotes typed literals with datatypes xsd:integer, xsd:decimal, xsd:float, and xsd:double. """
    return is_typed_literal(n) and cast(Literal, n).datatype in [XSD.integer, XSD.decimal, XSD.float, XSD.double]


def is_simple_literal(n: Node) -> bool:
    """ simple literal denotes a plain literal with no language tag. """
    return is_typed_literal(n) and cast(Literal, n).datatype is None and cast(Literal, n).language is None


def is_rdf_term(n: Node) -> bool:
    return isinstance(n, (URIRef, Literal, BNode))


def is_integer(n: Node) -> bool:
    return is_typed_literal(n) and cast(Literal, n).datatype in [
        XSD.integer,
        XSD.nonPositiveInteger,
        XSD.negativeInteger,
        XSD.long,
        XSD.int,
        XSD.short,
        XSD.byte,
        XSD.nonNegativeInteger,
        XSD.unsignedLong,
        XSD.unsignedInt,
        XSD.unsignedShort,
        XSD.unsignedByte,
        XSD.positiveInteger
    ]


def is_decimal(n: Node) -> bool:
    return is_integer(n) or is_typed_literal(n) and cast(Literal, n).datatype in [XSD.decimal]


def is_sparql_operand_datatype(n: Union[Node, str]) -> bool:
    # From: https://www.w3.org/TR/sparql11-query/#operandDataTypes
    return is_plain_literal(n) or (is_typed_literal(n) and cast(Literal, n).datatype in [
        XSD.integer,
        XSD.decimal,
        XSD.float,
        XSD.double,
        XSD.string,
        XSD.boolean,
        XSD.dateTime,
        XSD.nonPositiveInteger,
        XSD.negativeInteger,
        XSD.long,
        XSD.int,
        XSD.short,
        XSD.byte,
        XSD.nonNegativeInteger,
        XSD.unsignedLong,
        XSD.unsignedInt,
        XSD.unsignedShort,
        XSD.unsignedByte,
        XSD.positiveInteger
    ])
