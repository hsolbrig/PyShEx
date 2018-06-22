import os
import unittest
from typing import List

from pyshex import ShExEvaluator
from pyshex.shex_evaluator import EvaluationResult

shex = """{
  "@context": "http://www.w3.org/ns/shex.jsonld",
  "type": "Schema",
  "shapes": [
    {
      "type": "Shape",
      "id": "http://bioentity.io/vocab/SchemaDefinition",
      "expression": 
      {
         "type": "EachOf",
        "expressions": [
          {
            "predicate": "http://bioentity.io/vocab/id",
            "valueExpr": {
              "datatype": "http://www.w3.org/2001/XMLSchema#string",
              "type": "NodeConstraint"
            },
            "min": 1,
            "max": 1,
            "type": "TripleConstraint"
          },
          {
            "predicate": "http://bioentity.io/vocab/version",
            "valueExpr": {
              "datatype": "http://www.w3.org/2001/XMLSchema#string",
              "type": "NodeConstraint"
            },
            "min": 0,
            "max": 1,
            "type": "TripleConstraint"
          },
          {
            "predicate": "http://bioentity.io/vocab/imports",
            "valueExpr": {
              "datatype": "http://www.w3.org/2001/XMLSchema#string",
              "type": "NodeConstraint"
            },
            "min": 0,
            "max": -1,
            "type": "TripleConstraint"
          },
          {
            "predicate": "http://bioentity.io/vocab/license",
            "valueExpr": {
              "datatype": "http://www.w3.org/2001/XMLSchema#string",
              "type": "NodeConstraint"
            },
            "min": 0,
            "max": 1,
            "type": "TripleConstraint"
          }
        ]
      }
    }
  ]
}       
"""

shex2 = """{
  "@context": "http://www.w3.org/ns/shex.jsonld",
  "type": "Schema",
  "shapes": [
    { "type": "Shape",
      "id": "http://bioentity.io/vocab/PrefixList",
      "expression": {
        "type": "EachOf",
        "expressions": [
          {
            "predicate": "http://www.w3.org/1999/02/22-rdf-syntax-ns#first",
            "valueExpr": "http://bioentity.io/vocab/Prefix",
            "min": 0,
            "max": 1,
            "type": "TripleConstraint"
          },
          {
            "predicate": "http://www.w3.org/1999/02/22-rdf-syntax-ns#rest",
            "valueExpr": "http://bioentity.io/vocab/PrefixList",
            "min": 0,
            "max": 1,
            "type": "TripleConstraint"
          }
        ]
      }
    },
    {
      "type": "Shape",
      "id": "http://bioentity.io/vocab/SchemaDefinition",
      "expression": 
      {
         "type": "EachOf",
        "expressions": [
          {
            "predicate": "http://bioentity.io/vocab/id",
            "valueExpr": {
              "datatype": "http://www.w3.org/2001/XMLSchema#string",
              "type": "NodeConstraint"
            },
            "min": 1,
            "max": 1,
            "type": "TripleConstraint"
          },
          {
            "predicate": "http://bioentity.io/vocab/prefixes",
            "valueExpr": "http://bioentity.io/vocab/PrefixList",
            "min": 0,
            "max": -1,
            "type": "TripleConstraint"
          }
        ]
      }
    },
    {
         "id": "http://bioentity.io/vocab/Prefix",
         "expression": {
            "expressions": [
               {
                  "predicate": "http://bioentity.io/vocab/local_name",
                  "valueExpr": {
                     "datatype": "http://www.w3.org/2001/XMLSchema#string",
                     "type": "NodeConstraint"
                  },
                  "min": 1,
                  "max": 1,
                  "type": "TripleConstraint"
               },
               {
                  "predicate": "http://bioentity.io/vocab/prefix_uri",
                  "valueExpr": {
                     "datatype": "http://www.w3.org/2001/XMLSchema#string",
                     "type": "NodeConstraint"
                  },
                  "min": 0,
                  "max": 1,
                  "type": "TripleConstraint"
               }
            ],
            "type": "EachOf"
         },
         "type": "Shape"
      }
  ]
}       
"""

shex3 = """{
  "@context": "http://www.w3.org/ns/shex.jsonld",
  "type": "Schema",
  "shapes": [
    {
       "type": "Shape",
       "id": "http://bioentity.io/vocab/SlotDefinition",
       "expression": {
          "predicate": "http://bioentity.io/vocab/range",
          "valueExpr": "http://bioentity.io/meta/SlotRangeTypes",
          "min": 1,
          "max": 1,
          "type": "TripleConstraint"
      }
    },
     {
       "type": "Shape",
       "id": "http://bioentity.io/vocab/ClassDefinition",
       "expression": {
          "predicate": "http://www.w3.org/1999/02/22-rdf-syntax-ns#label",
          "min": 1,
          "max": 1,
          "type": "TripleConstraint"
      }
    },
     {
       "type": "Shape",
       "id": "http://bioentity.io/vocab/TypeDefinition",
       "expression": {
          "predicate": "http://www.w3.org/1999/02/22-rdf-syntax-ns#label",
          "min": 1,
          "max": 1,
          "type": "TripleConstraint"
      }
    },
    {
        "type": "NodeConstraint",
        "id": "http://bioentity.io/meta/Builtins",
        "values": ["http://www.w3.org/2001/XMLSchema#string",
                   "http://www.w3.org/2001/XMLSchema#integer", 
                   "http://www.w3.org/2001/XMLSchema#boolean", 
                   "http://www.w3.org/2001/XMLSchema#float", 
                   "http://www.w3.org/2001/XMLSchema#double", 
                   "http://www.w3.org/2001/XMLSchema#date", 
                   "http://www.w3.org/2001/XMLSchema#time", 
                   "http://www.w3.org/2001/XMLSchema#anyURI"]
    },
    {
      "type": "ShapeOr",
      "id": "http://bioentity.io/meta/SlotRangeTypes",
      "shapeExprs":
        [
          "http://bioentity.io/vocab/TypeDefinition",
          "http://bioentity.io/vocab/ClassDefinition",
          "http://bioentity.io/meta/Builtins"
        ]
    }
  ]
}
"""

fail_rdf_1 = """
@prefix biolink: <http://bioentity.io/vocab/> .
@prefix meta: <http://bioentity.io/meta/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

biolink:definitional biolink:domain biolink:SlotDefinition ;
    biolink:inherited true ;
    biolink:range biolink:junk ;
    rdf:label "definitional" ;
    skos:note "needs description" .
"""


class BioLinkTestCase(unittest.TestCase):
    cwd = os.path.abspath(os.path.dirname(__file__))
    meta_rdf_path = os.path.join(cwd, 'data', 'meta.ttl')
    meta_shex_path = os.path.join(cwd, 'data', 'meta.json')
    new_meta_shex_path = os.path.join(cwd, 'data', 'metashex.json')

    @staticmethod
    def eval_results(results: List[EvaluationResult]) -> bool:
        for r in results:
            if not r.result:
                print(f"\nshape: {r.start} focus: {r.focus}")
                print(f"{r.reason}")
        return all(r.result for r in results)

    def test_simple(self):
        with open(self.meta_rdf_path) as rdf:
            evaluator = ShExEvaluator(rdf.read(), shex,
                                      focus="https://biolink.github.io/metamodel/ontology/meta.ttl",
                                      start="http://bioentity.io/vocab/SchemaDefinition")
        self.assertTrue(self.eval_results(evaluator.evaluate()))

    def test_lists(self):
        with open(self.meta_rdf_path) as rdf:
            evaluator = ShExEvaluator(rdf.read(), shex2,
                                      focus="https://biolink.github.io/metamodel/ontology/meta.ttl",
                                      start="http://bioentity.io/vocab/SchemaDefinition")
        self.assertTrue(self.eval_results(evaluator.evaluate()))

    def test_full_meta(self):
        with open(self.meta_rdf_path) as rdf:
            with open(self.meta_shex_path) as shexf:
                evaluator = ShExEvaluator(rdf.read(), shexf.read(),
                                          focus="https://biolink.github.io/metamodel/ontology/meta.ttl",
                                          start="http://bioentity.io/vocab/SchemaDefinition")
        # Fails because
        # ---> Testing http://bioentity.io/vocab/local_name against (inner shape)
        #   ---> Testing http://www.w3.org/2001/XMLSchema#string against http://bioentity.io/vocab/Element
        #       No matching triples found for predicate http://www.w3.org/1999/02/22-rdf-syntax-ns#label
        self.assertFalse(evaluator.evaluate()[0].result)

    def test_new_meta(self):
        with open(self.meta_rdf_path) as rdf:
            with open(self.new_meta_shex_path) as shexf:
                evaluator = ShExEvaluator(rdf.read(), shexf.read(),
                                          focus="https://biolink.github.io/metamodel/ontology/meta.ttl",
                                          start="http://bioentity.io/vocab/SchemaDefinition")
        self.assertTrue(self.eval_results(evaluator.evaluate()))

    def test_range_construct(self):
        """ A range can be a builtin type, a TypeDefinition or a ClassDefinition """
        with open(self.meta_rdf_path) as rdf:
            evaluator = ShExEvaluator(rdf.read(), shex3,
                                      focus=["http://bioentity.io/vocab/abstract",
                                             "http://bioentity.io/vocab/class_definition_is_a",
                                             "http://bioentity.io/vocab/defining_slots"],
                                      start="http://bioentity.io/vocab/SlotDefinition")
        self.assertTrue(self.eval_results(evaluator.evaluate()))

        results = evaluator.evaluate(rdf=fail_rdf_1,
                                     focus="http://bioentity.io/vocab/definitional")
        self.assertFalse(any(r.result for r in results))


if __name__ == '__main__':
    unittest.main()
