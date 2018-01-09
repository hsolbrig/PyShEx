from typing import List, Dict, Set, Union, Optional, cast

from ShExJSG import ShExJ
from pyjsg.jsglib import jsg
from rdflib import Graph, ConjunctiveGraph, RDF, RDFS, URIRef, Namespace, Literal, BNode
from urllib.request import urlopen

from rdflib.collection import Collection

from pyshex.shape_expressions_language.p5_context import Context
from tests.utils.uri_redirector import URIRedirector

SHT = Namespace("http://www.w3.org/ns/shacl/test-suite#")
MF = Namespace("http://www.w3.org/2001/sw/DataAccess/tests/test-manifest#")


class ShExManifestEntry:
    def __init__(self, entryuri: URIRef, g: Graph, owner: "ShExManifest") -> None:
        """ An individual manifest entry

        :param entryuri: URI of the entry
        :param g: graph containing the entry
        """
        self.g = g
        self.entryuri = entryuri
        self.owner = owner
        action = self.g.value(self.entryuri, MF.action, any=False)
        assert action, "Invalid action list in entry"
        self.action_ = {p: o for p, o in g.predicate_objects(action)}
        assert self.action_, "No actions"

    def _action_obj(self, p) -> Union[URIRef, Literal]:
        return self.action_.get(p)

    @property
    def name(self) -> str:
        return str(self.g.value(self.entryuri, MF.name, any=False))

    @property
    def traits(self) -> Set[URIRef]:
        return set(self.g.objects(self.entryuri, SHT.trait))

    @property
    def comments(self) -> str:
        return '\n'.join([str(e) for e in self.g.objects(self.entryuri, RDFS.comment)])

    @property
    def status(self) -> URIRef:
        return self.g.value(self.entryuri, MF.status, any=False)

    @property
    def entry_type(self) -> URIRef:
        """ Possible types are:
        SHT.NegativeStructure
        SHT.NegativeSyntax
        SHT.RepresentationTest
        SHT.ValidationFailure
        SHT.ValidationTest
        """
        return self.g.value(self.entryuri, RDF.type, any=False)

    @property
    def should_parse(self) -> bool:
        return self.entry_type != SHT.NegativeSyntax

    @property
    def should_pass(self) -> bool:
        return self.entry_type == SHT.ValidationTest

    @property
    def schema_uri(self) -> Optional[URIRef]:
        return self._action_obj(SHT.schema)

    def schema(self) -> Optional[str]:
        if self.schema_uri:
            return self._fetch_schema(self.schema_uri)

    def shex_schema(self) -> Optional[ShExJ.Schema]:
        schema = self.schema()
        return jsg.loads(schema, ShExJ) if schema is not None else None

    @property
    def shape(self) -> Optional[URIRef]:
        return self._action_obj(SHT.shape)

    @property
    def data_uri(self) -> Optional[URIRef]:
        return self._action_obj(SHT.data)

    def data(self) -> Optional[str]:
        if self.data_uri:
            uri = self.owner.data_uri(self.data_uri)
            if isinstance(uri, URIRef):
                return urlopen(str(uri)).read().decode()
            else:
                with open(uri) as data_file:
                    return data_file.read()
        return None

    @property
    def focus(self) -> Optional[URIRef]:
        return self._action_obj(SHT.focus)

    def data_graph(self, fmt="turtle") -> Optional[Graph]:
        g = Graph()
        data_ttl = """@base <https://raw.githubusercontent.com/shexSpec/shexTest/master/validation/manifest> .
""" + self.data()
        g.parse(data=data_ttl, format=fmt)
        return g

    @property
    def externs(self) -> List[URIRef]:
        externs = self._action_obj(SHT.shapeExterns)
        return [] if externs is None else [e for e in Collection(self.g, externs)] \
            if isinstance(externs, BNode) else [externs]

    def resolve_extern(self, ref: ShExJ.shapeExprLabel) -> Optional[ShExJ.Shape]:
        pass

    def _fetch_schema(self, uri: URIRef) -> Optional[str]:
        # TODO: remove this when ShExC and ttl parsers are available
        schema_uri = self.owner.schema_uri(uri)
        if '.shextern' in str(self.owner.schema_uri(uri)):
            schema_uri_str = str(self.owner.schema_uri(uri)).replace(".shextern", ".jsontern")
        else:
            schema_uri_str = str(self.owner.schema_uri(uri)).replace(".shex", ".json")
        if isinstance(schema_uri, URIRef):
            return urlopen(schema_uri_str).read().decode()
        else:
            try:
                with open(schema_uri_str) as schema_file:
                    return schema_file.read()
            except FileNotFoundError as e:
                print(e.strerror)

    def extern_shape_for(self, ref: ShExJ.IRIREF) -> Optional[ShExJ.Shape]:
        for extern in self.externs:
            schema_str = self._fetch_schema(extern)
            if schema_str:
                schema = cast(ShExJ.Schema, jsg.loads(schema_str, ShExJ))
                cntxt = Context(None, schema)
                shape = cntxt.shapeExprFor(ref)
                if shape:
                    return shape
        return None

    def __str__(self):
        return str(self.name)


class ShExManifest:
    def __init__(self, file_loc: str, fmt: str='json-ld') -> None:
        self.g = ConjunctiveGraph()
        self.g.parse(file_loc, format=fmt)
        self.entries: Dict[str, List[ShExManifestEntry]] = {}

        self.schema_redirector: Optional[URIRedirector] = None
        self.data_redirector: Optional[URIRedirector] = None

        manifest = self.g.value(None, RDF.type, MF.Manifest, any=False)
        for e in Collection(self.g, self.g.value(manifest, MF.entries, any=False)):
            entry = ShExManifestEntry(e, self.g, self)
            self.entries.setdefault(str(entry), []).append(entry)

    def data_uri(self, uri: URIRef) -> Union[URIRef, str]:
        return self.data_redirector.uri_for(uri) if self.data_redirector else uri

    def schema_uri(self, uri: URIRef) -> Union[URIRef, str]:
        return self.schema_redirector.uri_for(uri) if self.schema_redirector else uri
