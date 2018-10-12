from typing import Callable, Optional, List, Union, Tuple

from pyjsg.jsglib import isinstance_
from pyjsg.jsglib import JSGObject
from rdflib import BNode, URIRef, Graph

from pyshex.shapemap_structure_and_language.p1_notation_and_terminology import RDFGraph, Node


class ParseNode:
    def __init__(self,
                 function: Callable[["Context", Union[RDFGraph, Node], JSGObject], bool],
                 expr: JSGObject,
                 object: Union[RDFGraph, Node]):
        self.function = function
        self.expr = expr
        self.graph = object if isinstance(object, RDFGraph) else None
        self.node = object if isinstance_(object, Node) else None
        self.result: bool = None
        self.fail_reason: Optional[str] = None
        self.reason_stack: List[Tuple[Union[BNode, URIRef], Optional[str]]] = []
        self.nodes: List[ParseNode] = []

    def dump_bnodes(self, g: Graph, node: BNode, indent: str, top: bool=True) -> List[str]:
        indent = indent + "  "
        rval = []
        if top:
            for s, p in g.subject_predicates(node):
                rval.append(f"{indent}  {s} - {p} - []")
        for p, o in sorted(g.predicate_objects(node)):
            rval += [f"{indent}  [] {p} - {o}"]
            if isinstance(o, BNode):
                rval += self.dump_bnodes(g, o, indent, top=False)
        return rval

    def fail_reasons(self, g: Graph, depth: int=0) -> List[str]:
        def follow_reasons(d: int) -> List[str]:
            fr = []
            if self.fail_reason:
                fr.append(d * "  " + f"  {self.fail_reason}")
                d += 1
            for node in self.nodes:
                fr += node.fail_reasons(g, d)
            return fr

        rval = []
        for i in range(0, len(self.reason_stack)):
            node, shape_name = self.reason_stack[i]
            if not shape_name:
                shape_name = '(inner shape)'
            indent = (i+depth)*"  "
            rval.append(f"{indent}---> Testing {node} against {shape_name} ")
            if isinstance(node, BNode):
                rval += [f"{indent}     BNODE:"]
                rval += self.dump_bnodes(g, node, indent + ' ')
        rval += follow_reasons(depth + len(self.reason_stack))
        return rval

    def set_result(self, rval: bool) -> None:
        """ Set the result of the evaluation. If the result is true, prune all of the children that didn't cut it

        :param rval: Result of evaluation
        """
        self.result = rval
        if self.result:
            self.nodes = [pn for pn in self.nodes if pn.result]
