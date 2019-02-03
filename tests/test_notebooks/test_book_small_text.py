import unittest

from pyshex import ShExEvaluator
from rdflib import Namespace

BASE = Namespace("https://www.w3.org/2017/10/bibframe-shex/")

shex = """
BASE <https://www.w3.org/2017/10/bibframe-shex/> 
PREFIX bf: <http://bibframe.org/vocab/>
PREFIX madsrdf: <http://www.loc.gov/mads/rdf/v1#>
PREFIX locid: <http://id.loc.gov/vocabulary/identifiers/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

<Work> EXTRA a {
  a [bf:Work] ;
  bf:class @<Classification> ;
  bf:creator @<Person> ;
  bf:derivedFrom IRI ;
  bf:hasRelationship @<Relationship> ;
  bf:language [<http://id.loc.gov/vocabulary/languages/>~] ;
  bf:subject @<Topic>* ;
 ^bf:instanceOf @<Instance> ;
}

<Classification> [<http://id.loc.gov/authorities/classification/>~] AND {
  a [bf:LCC] ;
  bf:label LITERAL
}

<Instance> {
  a [bf:Instance] ;
  bf:contributor @<Person> ;
  bf:derivedFrom IRI ;
  bf:instanceOf @<Work> ;
}

<Person> {
  a [bf:Person] ;
  bf:label LITERAL ;
  madsrdf:elementList @<ElementList>
}

<ElementList> CLOSED {
  rdf:first @<MadsElement> ;
  rdf:rest  [rdf:nil] OR @<ElementList>
}

<MadsElement> {
  a [ madsrdf:NameElement
      madsrdf:DateNameElement
      madsrdf:TopicElement
 ] ;
  madsrdf:elementValue LITERAL
}

<Relationship> {
  a [bf:Work] ;
  bf:title LITERAL ;
  bf:contributor {
    a [bf:name] ;
    bf:label LITERAL ;
    madsrdf:elementList @<ElementList>
  }
}

<MadsTopic> {
  a [madsrdf:Topic] ;
  a [madsrdf:Authority] ;
  madsrdf:authoritativeLabel [@en @fr @de] ;
  madsrdf:elementList @<ElementList>
}

<Topic> {
  a [bf:Topic]? ;
  a [madsrdf:ComplexSubject] ;
  bf:label LITERAL ;
  madsrdf:authoritativeLabel [@en @fr @de] ;
  madsrdf:componentList @<TopicList>
}

<TopicList> CLOSED {
  rdf:first @<MadsTopic> ;
  rdf:rest  [rdf:nil] OR @<TopicList>
}


"""

rdf = """
@base <https://www.w3.org/2017/10/bibframe-shex/> .
PREFIX bf: <http://bibframe.org/vocab/>
PREFIX madsrdf: <http://www.loc.gov/mads/rdf/v1#>
PREFIX locid: <http://id.loc.gov/vocabulary/identifiers/>

<samples9298996> a bf:Text, bf:Work ;
  bf:class <http://id.loc.gov/authorities/classification/PZ3> ;
  bf:creator [ a bf:Person ;
    bf:label "Dickens, Charles, 1812-1870." ;
    madsrdf:elementList (
      [ a madsrdf:NameElement ; madsrdf:elementValue "Dickens, Charles," ]
      [ a madsrdf:DateNameElement ; madsrdf:elementValue "1812-1870." ] ) ] ;
  bf:derivedFrom <http://id.loc.gov/resources/bibs/9298996> ;
  bf:hasRelationship [ a bf:Work ;
    bf:title "Oliver Twist." ;
    bf:contributor [ a bf:name ;
      bf:label "Oliver Twist." ;
      madsrdf:elementList (
        [ a madsrdf:NameElement ; madsrdf:elementValue "Oliver Twist." ] ) ] ] ;
  bf:language <http://id.loc.gov/vocabulary/languages/eng> ;
  bf:subject
    [ a bf:Topic, madsrdf:ComplexSubject ;
      bf:label "Criminals--Fiction" ;
      madsrdf:authoritativeLabel "Criminals--Fiction"@en ;
      madsrdf:componentList (
        [ a madsrdf:Authority, madsrdf:Topic ;
          madsrdf:authoritativeLabel "Criminals"@en ;
          madsrdf:elementList (
            [ a madsrdf:TopicElement ; madsrdf:elementValue "Criminals"@en ] ) ]
    ) ] ;
.

<http://id.loc.gov/authorities/classification/PZ3> a bf:LCC ;
  bf:label "PZ3.D55O165PR4567" .

[] a bf:Instance ;
  bf:contributor [
    a bf:Person ;
    bf:label "Greenawalt, Lambert, 1890- [from old catalog]" ;
    madsrdf:elementList (
      [ a madsrdf:NameElement ; madsrdf:elementValue "Greenawalt, Lambert," ]
      [ a madsrdf:DateNameElement ; madsrdf:elementValue "1890- [ from old catalog]" ]
  ) ] ;
  bf:derivedFrom <http://id.loc.gov/resources/bibs/9298996> ;
  bf:instanceOf <samples9298996> ;
.
"""


class BookSmallTextTestCase(unittest.TestCase):
    def test_it(self):
        results = ShExEvaluator().evaluate(rdf, shex, focus=BASE.samples9298996, start=BASE.Work)
        self.assertTrue(all(r.result for r in results))


if __name__ == '__main__':
    unittest.main()
