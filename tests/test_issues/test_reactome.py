import jsonasobj
import unittest

import os
import requests
from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd
from ShExJSG import Schema, ShExC
from rdflib import URIRef

from pyshex import PrefixLibrary, ShExEvaluator


def get_sparql_dataframe(service, query):
    """
    Helper function to convert SPARQL results into a Pandas data frame.
    """
    sparql = SPARQLWrapper(service)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    result = sparql.query()

    processed_results = jsonasobj.load(result.response)
    cols = processed_results.head.vars

    out = []
    for row in processed_results.results.bindings:
        item = []
        for c in cols:
            item.append(row._as_dict.get(c, {}).get('value'))
        out.append(item)

    return pd.DataFrame(out, columns=cols)


class ReactomeTestCase(unittest.TestCase):

    def test_andras_loop(self):
        manifast_wikipathways = \
            "https://raw.githubusercontent.com/shexSpec/schemas/master/Wikidata/pathways/Reactome/manifest.json"
        manifest = jsonasobj.loads(requests.get(manifast_wikipathways).text)

        for case in manifest:
            print(case._as_json_dumps())
            if case.data.startswith("Endpoint:"):
                sparql_endpoint = case.data.replace("Endpoint: ", "")
                schema = requests.get(case.schemaURL).text
                shex = ShExC(schema).schema
                print("==== Schema =====")
                print(shex._as_json_dumps())
                pfx = PrefixLibrary(schema, wikidata="http://www.wikidata.org/entity/")

                evaluator = ShExEvaluator(schema=shex, debug=True)
                sparql_query = case.queryMap.replace("SPARQL '''", "").replace("'''@START", "")

                df = get_sparql_dataframe(sparql_endpoint, sparql_query)
                for wdid in df.item:
                    slurpeddata = requests.get(wdid + ".ttl")
                    results = evaluator.evaluate(rdf=slurpeddata.text, focus=wdid, debug=True)
                    for result in results:
                        if result.result:
                            print(str(result.focus) + ": CONFORMS")
                        else:
                            print(
                                "item with issue: " + str(result.focus) + " - " + "shape applied: " + str(result.start))

    def test_single_reactome(self):
        data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data'))
        with open(os.path.join(data_path, 'reactome.shex')) as shexf:
            shex = shexf.read()
        pfx = PrefixLibrary(shex)
        results = ShExEvaluator(os.path.join(data_path, 'Q29017194.ttl'), shex, pfx.WD.Q29017194).evaluate(debug=False)
        self.assertTrue(all(r.result for r in results))


if __name__ == '__main__':
    unittest.main()
