import re
from typing import Union, Dict, Optional

from rdflib import Namespace, Graph, RDF, RDFS, XSD, URIRef
from rdflib.namespace import DOAP, FOAF, DC, DCTERMS, VOID, SKOS, OWL, XMLNS


class PrefixLibrary:
    def __init__(self, schema: Optional[str]=None, **kwlibs: Union[str, Namespace]) -> None:
        """ Generate a prefix library from a ShEx schema

        :param schema: ShExC Schema
        """
        if schema is not None:
            for line in schema.split('\n'):
                line = line.strip()
                m = re.match(r'PREFIX\s+(\S+):\s+<(\S+)>', line)
                if not m:
                    m = re.match(r"@prefix\s+(\S+):\s+<(\S+)>\s+\.", line)
                if m:
                    setattr(self, m.group(1).upper(), Namespace(m.group(2)))

        for k, v in kwlibs.items():
            setattr(self, k.upper(), v if isinstance(v, Namespace) else Namespace(v))

    def __iter__(self):
        for k, v in self.__dict__.items():
            if isinstance(v, Namespace):
                yield (k, v)

    def __str__(self) -> str:
        rval = ""
        for k, v in self:
            rval += f"PREFIX {k.lower()}: <{str(v)}>\n"
        return rval + '\n'

    def add_bindings(self, g: Graph) -> "PrefixLibrary":
        """ Add bindings in the library to the graph

        :param g: graph to add prefixes to
        :return: PrefixLibrary object
        """
        for prefix, namespace in self:
            g.bind(prefix.lower(), namespace)
        return self

    def nsname(self, uri: Union[str, URIRef]) -> str:
        uri = str(uri)
        nsuri = ""
        prefix = None
        for pfx, ns in self:
            nss = str(ns)
            if uri.startswith(nss) and len(nss) > len(nsuri):
                nsuri = nss
                prefix = pfx
        return (prefix.lower() + ':' + uri[len(nsuri):]) if prefix is not None else uri


standard_prefixes = PrefixLibrary(None, rdf=RDF, rdfs=RDFS, xml=XMLNS, xsd=XSD)


known_prefixes = PrefixLibrary(None, dc=DC, dcterms=DCTERMS, doap=DOAP, foaf=FOAF, owl=OWL, rdf=RDF, rdfs=RDFS,
                               skos=SKOS, xsd=XSD, xmlns=XMLNS)
