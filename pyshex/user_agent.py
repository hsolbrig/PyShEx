from SPARQLWrapper import SPARQLWrapper
from pbr.version import VersionInfo
from sparql_slurper import SlurpyGraph, Optional

__version__ = VersionInfo('PyShEx')

# https://meta.wikimedia.org/wiki/User-Agent_policy:
#   The generic format is <client name>/<version> (<contact information>) <library/framework name>/<version>
#   [<library name>/<version> ...]. Parts that are not applicable can be omitted.

UserAgent = f"{__version__.package}/{__version__.version_string()} " \
            f"(https://github.com/hsolbrig/PyShEx; solbrig@jhu.edu)"


class SlurpyGraphWithAgent(SlurpyGraph):
    def __init__(self, endpoint: str, *args, persistent_bnodes: bool = False, agent: Optional[str] = None,
                 **kwargs) -> None:
        """ A slurpy graph that includes a user agent """
        super().__init__(endpoint, *args, persistent_bnodes=persistent_bnodes, **kwargs)
        self.sparql.agent = agent if agent else UserAgent


class SPARQLWrapperWithAgent(SPARQLWrapper):
    def __init__(self, endpoint, updateEndpoint=None, returnFormat=None, defaultGraph=None, agent=UserAgent):
        super().__init__(endpoint, updateEndpoint=updateEndpoint, returnFormat=returnFormat, defaultGraph=defaultGraph,
                         agent=agent)

