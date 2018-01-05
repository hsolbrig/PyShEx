from typing import List, Dict, Set, Union, Optional

from ShExJSG import ShExJ
from pyjsg.jsglib import jsg
from rdflib import Graph, ConjunctiveGraph, RDF, RDFS, URIRef, Namespace, Literal
from urllib.request import urlopen

from rdflib.collection import Collection

SHT = Namespace("http://www.w3.org/ns/shacl/test-suite#")
MF = Namespace("http://www.w3.org/2001/sw/DataAccess/tests/test-manifest#")


class ShExManifestEntry:
    def __init__(self, entryuri: URIRef, g: Graph) -> None:
        """ An individual manifest entry

        :param entryuri: URI of the entry
        :param g: graph containing the entry
        """
        self.g = g
        self.entryuri = entryuri
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
        # TODO: remove this when ShExC and ttl parsers are available
        schema_uri = str(self.schema_uri).replace(".shex", ".json")
        return urlopen(schema_uri).read().decode() if self.schema_uri else None

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
        return urlopen(self.data_uri).read().decode() if self.data_uri else None

    @property
    def focus(self) -> Optional[URIRef]:
        return self._action_obj(SHT.focus)

    def data_graph(self, fmt="turtle") -> Optional[Graph]:
        g = Graph()
        g.parse(self.data_uri, format=fmt)
        return g

    def __str__(self):
        return str(self.name)


class ShExManifest:
    def __init__(self, file_loc: str, fmt: str='json-ld') -> None:
        self.g = ConjunctiveGraph()
        self.g.parse(file_loc, format=fmt)
        self.entries: Dict[str, List[ShExManifestEntry]] = {}

        manifest = self.g.value(None, RDF.type, MF.Manifest, any=False)
        for e in Collection(self.g, self.g.value(manifest, MF.entries, any=False)):
            entry = ShExManifestEntry(e, self.g)
            self.entries.setdefault(str(entry), []).append(entry)
