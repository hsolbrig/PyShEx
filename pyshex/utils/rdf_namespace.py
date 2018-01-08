""" Typed namespace wrapper for rdflib """
import typing

from rdflib import Namespace, URIRef


class RDFNamespace(Namespace):
    def __getitem__(self, *args) -> URIRef:
        return typing.cast(URIRef,  super().__getitem__(*args))

    def __getattr__(self, item) -> URIRef:
        return typing.cast(URIRef, super().__getattr__(item))
