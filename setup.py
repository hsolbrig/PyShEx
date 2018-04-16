import sys
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.version_info < (3, 6):
    print("This module requires python 3.6 or later")
    sys.exit(1)

setup(
    name='PyShEx',
    version='0.5.4',
    packages=['scripts', 'pyshex', 'pyshex.shape_expressions_language', 'pyshex.shapemap_structure_and_language',
              'pyshex.sparql11_query', 'pyshex.utils', 'pyshex.parse_tree'],
    url="http://github.com/hsolbrig/PyShEx",
    license='Apache 2.0',
    author='Harold Solbrig',
    author_email='solbrig@solbrig-informatics.com',
    description='Python ShEx Implementation',
    install_requires=['ShExJSG>=0.2.1', 'PyShExC>=0.3.4', 'rdflib>=4.2.2', 'rdflib-jsonld>=0.4.0', 'requests',
                      'urllib3', 'sparql_slurper'],
    tests_require=['PyJSG', 'jsonasobj', 'SPARQLWrapper'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Compilers',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6']
)
