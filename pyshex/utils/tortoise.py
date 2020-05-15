from rdflib import plugin
from rdflib.plugins.serializers.turtle import TurtleSerializer
from rdflib.serializer import Serializer


class Cornucopia:
    """
    An iterator that claims to contain everything
    """
    def __iter__(self):
        return self

    def __contains__(self, item):
        return True


class TurtleWithPrefixes(TurtleSerializer):
    """ A turtle serializer that always emits prefixes """
    def __init__(self, store):
        super().__init__(store)
        self.roundtrip_prefixes = Cornucopia()


def register():
    plugin.register('tortoise', Serializer, 'pyshex.utils.tortoise', 'TurtleWithPrefixes')
