from typing import Union

from rdflib import URIRef


class URIRedirector:
    def __init__(self, base: URIRef, target: str) -> None:
        self.base = base
        self.target = target

    def uri_for(self, uri: URIRef) -> Union[URIRef, str]:
        unix_uri = str(uri).replace('\\', '/')
        return unix_uri.replace(self.base, self.target) if unix_uri.startswith(self.base) else uri
