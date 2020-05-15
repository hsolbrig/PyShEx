from sparqlslurper import SlurpyGraph

from pyshex import shex_evaluator
from pyshex.shex_evaluator import evaluate_cli as shexeval
from pyshex.user_agent import SlurpyGraphWithAgent


permagraph = None


def persistent_slurper(rdf: str) -> SlurpyGraph:
    global permagraph
    permagraph = SlurpyGraphWithAgent(rdf)
    return permagraph


shex_evaluator.SlurpyGraph = persistent_slurper

# The parameters are:
#   -ss   Use sparql slurper
#   -sq   SPARQL query
#  --stopafter 1    Don't go on.  (Could be "-se" if one wished)
#
#  If this is what you want, we can override the function that is called at the
#  end of each query

x = ["-ss",
     "-sq",
     'PREFIX wdt: <http://www.wikidata.org/prop/direct/>\n\nSELECT ?item WHERE { ?item wdt:P699 ?doid } LIMIT 100',
     "http://query.wikidata.org/sparql",
     "https://raw.githubusercontent.com/SuLab/Genewiki-ShEx/master/diseases/wikidata-disease-ontology.shex",  "-se"
     ]
shexeval(x)
# print(permagraph.serialize(format="turtle").decode())