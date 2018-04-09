from typing import Callable, Optional, List, Union

from pyjsg.jsglib import jsg
from pyjsg.jsglib.jsg import isinstance_

from pyshex.shapemap_structure_and_language.p1_notation_and_terminology import RDFGraph, Node


class ParseNode:
    def __init__(self,
                 function: Callable[["Context", Union[RDFGraph, Node], jsg.JSGObject], bool],
                 expr: jsg.JSGObject,
                 object: Union[RDFGraph, Node]):
        self.function = function
        self.expr = expr
        self.graph = object if isinstance(object, RDFGraph) else None
        self.node = object if isinstance_(object, Node) else None
        self.result: bool = None
        self.fail_reason: Optional[str] = None
        self.nodes: List[ParseNode] = []
