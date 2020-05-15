import os
import unittest

from rdflib import Graph, BNode

from pyshex.utils.n3_mapper import N3Mapper


class N3MapperUnitTest(unittest.TestCase):
    def test_basics(self):
        source_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'source')
        target_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'target')
        new_files = False

        os.makedirs(target_dir, exist_ok=True)
        self.maxDiff = None
        for f in os.listdir(source_dir):
            fpath = os.path.join(source_dir, f)
            if os.path.isfile(fpath):
                g = Graph()
                g.load(fpath, format='turtle')
                mapper = N3Mapper(g.namespace_manager)
                result = '\n'.join([mapper.n3(t)
                                    for t in sorted(list(g),
                                                    key=lambda t: (1, t) if isinstance(t[0], BNode) else (0, t))])
                tpath = os.path.join(target_dir, f)
                if not os.path.exists(tpath):
                    print(f"Creating: {tpath}")
                    with open(tpath, 'w') as t:
                        t.write(result)
                    new_files = True
                with open(tpath) as t:
                    self.assertEqual(t.read(), result)
            self.assertFalse(new_files, "New test files created - rerun")


if __name__ == '__main__':
    unittest.main()
