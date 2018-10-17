import sys
from setuptools import setup, find_packages


if sys.version_info < (3, 6):
    print("This module requires python 3.6 or later")
    sys.exit(1)

setup(
    name='PyShEx',
    version='0.5.9',
    packages = find_packages(exclude=['tests']),
    url="http://github.com/hsolbrig/PyShEx",
    license='Apache 2.0',
    author='Harold Solbrig',
    author_email='solbrig@solbrig-informatics.com',
    description='Python ShEx Implementation',
    install_requires=['ShExJSG>=0.5.1', 'PyShExC>=0.5.0', 'rdflib>=4.2.2', 'rdflib-jsonld>=0.4.0', 'requests',
                      'urllib3', 'sparql_slurper>=0.1.3'],
    tests_require=['PyJSG>=0.9.0', 'jsonasobj>=1.2.1', 'SPARQLWrapper>=1.8.2'],
    entry_points={
        'console_scripts': [
            'shexeval = pyshex.shex_evaluator:evaluate_cli'
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Compilers',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6']
)
