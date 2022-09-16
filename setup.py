import io
import setuptools


setuptools.setup(
    name='jsonpath-ng-aerospike',
    version='1.5.3',
    description=(
        'A final implementation of JSONPath for Python that aims to be '
        'standard compliant, including arithmetic and binary comparison '
        'operators and providing clear AST for metaprogramming.'
    ),
    author='Tomas Aparicio, Julian Nguyen',
    author_email='tomas@aparicio.me, jnguyen@aerospike.com',
    url='https://github.com/aerospike-community/jsonpath-ng',
    license='Apache 2.0',
    long_description=io.open('README.rst', encoding='utf-8').read(),
    packages=['jsonpath_ng', 'jsonpath_ng.bin', 'jsonpath_ng.ext'],
    entry_points={
        'console_scripts': [
            'jsonpath_ng=jsonpath_ng.bin.jsonpath:entry_point'
        ],
    },
    test_suite='tests',
    install_requires=[
        'ply', 'decorator', 'six'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
	'Programming Language :: Python :: 3.7',
	'Programming Language :: Python :: 3.8',
    ],
)
