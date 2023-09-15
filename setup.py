import io
import setuptools


setuptools.setup(
    name='jsonpath-ng',
    version='1.6.0',
    description=(
        'A final implementation of JSONPath for Python that aims to be '
        'standard compliant, including arithmetic and binary comparison '
        'operators and providing clear AST for metaprogramming.'
    ),
    author='Tomas Aparicio',
    author_email='tomas@aparicio.me',
    url='https://github.com/h2non/jsonpath-ng',
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
        'ply'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11'
    ],
)
