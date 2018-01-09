from typing import Union

from rdflib import URIRef


class URIRedirector:
    def __init__(self, base: URIRef, target: str) -> None:
        self.base = base
        self.target = target

    def uri_for(self, uri: URIRef) -> Union[URIRef, str]:
        return str(uri).replace(self.base, self.target) if str(uri).startswith(self.base) else uri
