from typing import List

import jsonasobj
import requests
from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import URIRef


class SPARQLQuery:
    def __init__(self, sparql_endpoint: str, sparql_file_uri_or_text: str, ) -> None:
        """ Set up the query to run

        :param sparql_endpoint: URL of sparql endpoint
        :param sparql_file_uri_or_text: URI, filename or SPARQL text
        """
        if '\n' in sparql_file_uri_or_text or '\r' in sparql_file_uri_or_text or ' ' in sparql_file_uri_or_text:
            self.query = sparql_file_uri_or_text
        elif ':/' in sparql_file_uri_or_text:
            req = requests.get(sparql_file_uri_or_text)
            if not req.ok:
                raise ValueError(f"Unable to read {sparql_file_uri_or_text}")
            self.query = req.text
        else:
            with open(sparql_file_uri_or_text) as f:
                self.query = f.read()
        self.endpoint = SPARQLWrapper(sparql_endpoint)
        self.endpoint.setQuery(self.query)
        self.endpoint.setReturnFormat(JSON)

    def focus_nodes(self) -> List[URIRef]:
        result = self.endpoint.query()

        processed_results = jsonasobj.load(result.response)
        return [URIRef(row.item.value) for row in processed_results.results.bindings]
