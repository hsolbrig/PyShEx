from typing import Optional

from SPARQLWrapper import SPARQLWrapper
from pbr.version import VersionInfo
from sparqlslurper import SlurpyGraph, GraphDBSlurpyGraph

__version__ = VersionInfo('PyShEx')

# https://meta.wikimedia.org/wiki/User-Agent_policy:
#   The generic format is <client name>/<version> (<contact information>) <library/framework name>/<version>
#   [<library name>/<version> ...]. Parts that are not applicable can be omitted.

UserAgent = f"{__version__.package}/{__version__.version_string()} " \
            f"(https://github.com/hsolbrig/PyShEx; solbrig@jhu.edu)"


def SlurpyGraphWithAgent(endpoint: str, *args, persistent_bnodes: bool = False, agent: Optional[str] = None,
                 gdb_slurper: Optional[bool] = False, **kwargs) -> SlurpyGraph:
    rval = GraphDBSlurpyGraph(endpoint, *args, persistent_bnodes=persistent_bnodes, **kwargs) if gdb_slurper else \
        SlurpyGraph(endpoint, *args, persistent_bnodes=persistent_bnodes, **kwargs)
    rval.sparql.agent = agent if agent else UserAgent
    return rval

class SPARQLWrapperWithAgent(SPARQLWrapper):
    def __init__(self, endpoint, updateEndpoint=None, returnFormat=None, defaultGraph=None, agent=UserAgent):
        super().__init__(endpoint, updateEndpoint=updateEndpoint, returnFormat=returnFormat, defaultGraph=defaultGraph,
                         agent=agent)

