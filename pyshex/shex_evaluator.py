import sys
from argparse import ArgumentParser
from typing import Optional, Union, List, NamedTuple, Type

from CFGraph import CFGraph
from ShExJSG import ShExJ, ShExC
from rdflib import Graph, URIRef, RDF
from rdflib.util import guess_format
from sparql_slurper import SlurpyGraph

from pyshex.shape_expressions_language.p5_2_validation_definition import isValid
from pyshex.shape_expressions_language.p5_context import Context
from pyshex.shapemap_structure_and_language.p3_shapemap_structure import FixedShapeMap, ShapeAssociation, START, \
    START_TYPE
from pyshex.utils.schema_loader import SchemaLoader


class EvaluationResult(NamedTuple):
    result: bool
    focus: Optional[URIRef]
    start: Optional[URIRef]
    reason: Optional[str]


# Handy types
URI = Union[str, URIRef]        # URI as an argument
URILIST = List[URI]             # List of URI's as an argument
URIPARM = Union[URI, URILIST]       # Choice of URI or list
STARTPARM = [Union[Type[START], START_TYPE, URILIST]]


def normalize_uri(u: URI) -> URIRef:
    """ Return a URIRef for a str or URIRef """
    return u if isinstance(u, URIRef) else URIRef(str(u))


def normalize_urilist(ul: URILIST) -> List[URIRef]:
    """ Return a list of URIRefs for ul """
    return [normalize_uri(u) for u in ul]


def normalize_uriparm(p: URIPARM) -> List[URIRef]:
    """ Return an optional list of URIRefs for p"""
    return normalize_urilist(p) if isinstance(p, List) else \
        normalize_urilist([p]) if isinstance(p, (str, URIRef)) else p


def normalize_startparm(p: STARTPARM) -> List[Union[type(START), START_TYPE, URIRef]]:
    """ Return the startspec for p """
    if not isinstance(p, list):
        p = [p]
    return [normalize_uri(e) if isinstance(e, str) and e is not START else e for e in p]


class ShExEvaluator:
    """ Shape Expressions Evaluator """

    def __init__(self,
                 rdf: Optional[Union[str, Graph]] = None,
                 schema: Optional[Union[str, ShExJ.Schema]] = None,
                 focus: Optional[URIPARM] = None,
                 start: STARTPARM = None,
                 rdf_format: str = "turtle",
                 debug: bool = False,
                 debug_slurps: bool = False,
                 over_slurp: bool = None) -> None:
        """ Evaluator constructor.  All of the parameters below can be set in the constructor or at runtime

        :param rdf: RDF string, file name, URL or Graph for evaluation.
        :param schema: ShEx Schema to evaluate. Can be ShExC, ShExJ or a pre-parsed schema
        :param focus: focus node(s).  If absent, all non-BNode subjects in the graph are evaluated
        :param start: start node(s). If absent, the START node in the schema is used
        :param rdf_format: format for RDF. Default: "Turtle"
        :param debug: emit semi-helpful debug information
        :param debug: debug graph fetch calls
        :param over_slurp: Controls whether SPARQL slurper does exact or over slurps
        """
        self.rdf_format = rdf_format
        self.g = None
        self.rdf = rdf
        self._schema = None
        self.schema = schema
        self._focus = None
        self.focus = focus
        self.start = start
        self.debug = debug
        self.debug_slurps = debug_slurps
        self.over_slurp = over_slurp

    @property
    def rdf(self) -> str:
        """

        :return: The rendering of whatever RDF is currently being evaluated
        """
        return self.g.serialize(format=self.rdf_format).decode()

    @rdf.setter
    def rdf(self, rdf: Optional[Union[str, Graph]]) -> None:
        """ Set the RDF DataSet to be evaulated.  If ``rdf`` is a string, the presence of a return is the
        indicator that it is text instead of a location.

        :param rdf: File name, URL, representation of rdflib Graph
        """
        if isinstance(rdf, Graph):
            self.g = rdf
        else:
            self.g = Graph()
            if isinstance(rdf, str):
                if '\n' in rdf or '\r' in rdf:
                    self.g.parse(data=rdf, format=self.rdf_format)
                elif ':' in rdf:
                    self.g.parse(location=rdf, format=self.rdf_format)
                else:
                    self.g.parse(source=rdf, format=self.rdf_format)

    @property
    def schema(self) -> Optional[str]:
        """

        :return: The ShExC representation of the schema if one is supplied
        """
        return str(ShExC(self._schema)) if self._schema else None

    @schema.setter
    def schema(self, shex: Optional[Union[str, ShExJ.Schema]]) -> None:
        """ Set the schema to be used.  Schema can either be a ShExC or ShExJ string or a pre-parsed schema.

        :param shex:  Schema
        """
        if shex is not None:
            if isinstance(shex, ShExJ.Schema):
                self._schema = shex
            else:
                shext = shex.strip()
                if ('\n' in shex or '\r' in shex) or shext[0] in '#<_: ':
                    self._schema = SchemaLoader().loads(shex)
                else:
                    self._schema = SchemaLoader().load(shex) if isinstance(shex, str) else shex
                if self._schema is None:
                    raise ValueError("Unable to parse shex file")

    @property
    def focus(self) -> Optional[List[URIRef]]:
        """
        :return: The list of focus nodes (if any)
        """
        return self._focus

    @property
    def foci(self) -> List[URIRef]:
        """

        :return: The current set of focus nodes
        """
        return self._focus if self._focus else sorted([s for s in set(self.g.subjects()) if isinstance(s, URIRef)])

    @focus.setter
    def focus(self, focus: Optional[URIPARM]) -> None:
        """ Set the focus node(s).  If no focus node is specified, the evaluation will occur for all non-BNode
        graph subjects.  Otherwise it can be a string, a URIRef or a list of string/URIRef combinations

        :param focus: None if focus should be all URIRefs in the graph otherwise a URI or list of URI's
        """
        self._focus = normalize_uriparm(focus) if focus else None

    @property
    def start(self) -> STARTPARM:
        """

        :return: The schema start node(s)
        """
        return self._start

    @start.setter
    def start(self, start: STARTPARM) -> None:
        self._start = normalize_startparm(start) if start else [START]

    def evaluate(self,
                 rdf: Optional[Union[str, Graph]] = None,
                 shex: Optional[Union[str, ShExJ.Schema]] = None,
                 focus: Optional[URIPARM] = None,
                 start: STARTPARM = None,
                 rdf_format: Optional[str] = None,
                 debug: Optional[bool] = None,
                 debug_slurps: Optional[bool] = None,
                 over_slurp: Optional[bool] = None) -> List[EvaluationResult]:
        if rdf is not None or shex is not None or focus is not None or start is not None:
            evaluator = ShExEvaluator(rdf if rdf is not None else self.g,
                                      shex if shex is not None else self._schema,
                                      focus if focus is not None else self.focus,
                                      start if start is not None else self.start if self.start else START,
                                      rdf_format if rdf_format is not None else self.rdf_format)
        else:
            evaluator = self

        if START in self.start and evaluator._schema.start is None:
            return [EvaluationResult(False, None, None, 'START node is not specified')]

        cntxt = Context(evaluator.g, evaluator._schema)
        cntxt.debug_context.debug = debug if debug is not None else self.debug
        cntxt.debug_context.trace_slurps = debug_slurps if debug_slurps is not None else self.debug_slurps
        cntxt.over_slurp = self.over_slurp if over_slurp is not None else self.over_slurp

        rval = []
        for focus in evaluator.foci:
            start_list: List[Union[URIRef, START]] = []
            for start in evaluator.start:
                if start is START:
                    start_list.append(evaluator._schema.start)
                elif isinstance(start, START_TYPE):
                    start_list += list(evaluator.g.objects(focus, start.start_predicate))
                else:
                    start_list.append(start)
            if start_list:
                for start_node in start_list:
                    map_ = FixedShapeMap()
                    map_.add(ShapeAssociation(focus, start_node))
                    success, fail_reasons = isValid(cntxt, map_)
                    rval.append(EvaluationResult(success, focus, start_node,
                                                 '\n'.join(fail_reasons) if not success else ''))
            else:
                rval.append(EvaluationResult(False, focus, None, "No start node located"))
        return rval


def genargs(prog: Optional[str]=None) -> ArgumentParser:
    """
    Create a command line parser
    :return: parser
    """
    parser = ArgumentParser(prog)
    parser.add_argument("rdf", help="Input RDF file or SPARQL endpoint if slurper option set")
    parser.add_argument("shex", help="ShEx specification")
    parser.add_argument("-f", "--format", help="Input RDF Format", default="turtle")
    parser.add_argument("-s", "--start", help="Start shape. If absent use ShEx start node.")
    parser.add_argument("-ut", "--usetype", help="Start shape is rdf:type of focus", action="store_true")
    parser.add_argument("-sp", "--startpredicate", help="Start shape is object of this predicate")
    parser.add_argument("-fn", "--focus", help="RDF focus node")
    parser.add_argument("-A", "--allsubjects", help="Evaluate all non-bnode subjects in the graph", action="store_true")
    parser.add_argument("-d", "--debug", action="store_true", help="Add debug output")
    parser.add_argument("-ss", "--slurper", action="store_true", help="Use SPARQL slurper graph")
    parser.add_argument("-cf", "--flattener", action="store_true", help="Use RDF Collections flattener graph")
    return parser


def evaluate_cli(argv: Optional[List[str]] = None, prog: Optional[str]=None) -> bool:
    opts = genargs(prog).parse_args(argv if argv is not None else sys.argv[1:])
    if opts.slurper and opts.flattener:
        print("Error: Cannot combine slurper and flattener graphs")
        return False
    if not opts.format:
        opts.format = guess_format(opts.rdf)
    if not opts.format:
        print('Error: Cannot determine RDF format from file name - use "--format" option')
        return False
    g = SlurpyGraph(opts.rdf) if opts.slurper else CFGraph() if opts.flattener else Graph()
    if not opts.slurper:
        g.load(opts.rdf, format=opts.format)
    if not (opts.focus or opts.allsubjects):
        print('Error: You must specify one or more graph focus nodes or use the "-A" option')
        return False

    start = []
    if opts.start:
        start.append(opts.start)
    if opts.usetype:
        start.append(START_TYPE(RDF.type))
    if opts.startpredicate:
        start.append(START_TYPE(opts.startpredicate))
    if not start:
        start.append(START)

    result = ShExEvaluator(g, opts.shex, opts.focus, start, rdf_format=opts.format, debug=opts.debug).evaluate()
    success = all(r.result for r in result)
    if not success:
        print("Errors:")
        for rslt in result:
            if not rslt.result:
                print(f"""  Focus: {rslt.focus}
  Start: {rslt.start}
  Reason: {str(rslt.reason).strip()}
""")
    return success
