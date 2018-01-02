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

""" Implemention of `5.6 Schema Requirements <http://shex.io/shex-semantics/#schema-requirements>`_

The semantics defined above assume two structural requirements beyond those imposed by the grammar of the
abstract syntax. These ensure referential integrity and eliminate logical paradoxes such as those that arrise
through the use of negation. These are not constraints expressed by the schema but instead those imposed on
the schema.
"""
from ShExJSG import ShExJ

from pyshex.shape_expressions_language.p5_3_shape_expressions import satisfies
from pyshex.shape_expressions_language.p5_7_semantic_actions import semActsSatisfied
from pyshex.shape_expressions_language.p5_context import Context
from pyshex.shapemap_structure_and_language.p3_shapemap_structure import ShapeMapType
from pyshex.utils.schema_utils import reference_of


def conforms(S: ShExJ.Schema, m: ShapeMapType, cntxt: Context) -> bool:
    """ `5.6.1 Schema Validation Requirement <http://shex.io/shex-semantics/#validation-requirement>`_
    
    A graph G is said to conform with a schema S with a ShapeMap m when:

    Every, SemAct in the startActs of S has a successful evaluation of semActsSatisfied.
    Every node n in m conforms to its associated shapeExprRefs sen where for each shapeExprRef sei in sen:
        sei references a ShapeExpr in shapes, and
        satisfies(n, sei, G, m) for each shape sei in sen.

    :param S:  schema
    :param m: ShapeMap
    :param cntxt: context carrying the Graph and other useful things
    :return:
    """
    return semActsSatisfied(S.startActs, cntxt) and \
        all(reference_of(S, sa.shapeLabel) is not None and
            satisfies(sa.nodeSelector, reference_of(S, sa.shapeLabel), cntxt) for sa in m)


def valid_shape_references(S: ShExJ.Schema, cntxt: Context) -> bool:
    """ `5.6.2 Shape Expression Reference Requirement <http://shex.io/shex-semantics/#shapeExprRef-requirement>`_"""
    return True


def valid_triple_references(S: ShExJ.Schema, cntxt: Context) -> bool:
    """ `5.6.3 Triple Expression Reference Requirement <http://shex.io/shex-semantics/#tripleExprRef-requirement>`_"""
    return True


def valid_negations(S: ShExJ.Schema, cntxt: Context) -> bool:
    """ `5.6.4 <http://shex.io/shex-semantics/#negation-requirement>`_"""
    return True
