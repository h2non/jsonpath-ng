1.6.0 / 2023-09-13
===================
  *  Enclose field names containing literals in quotes
  *  Add note about extensions
  *  Remove documentation status link
  *  Update supported versions in setup.py
  *  Add LICENSE file
  *  Code cleanup
  *  Remove dependency on six
  *  Update build status badge
  *  (origin/github-actions, github-actions) Remove testscenarios dependency
  *  Remove pytest version constraints
  *  Add testing with GitHub actions
  *  Escape back slashes in tests to avoid DeprecationWarning.
  *  Use raw strings for regular expressions to avoid DeprecationWarning.
  *  refactor(package): remove dependency for decorator
  *  Merge pull request #128 from michaelmior/hashable
  *  (origin/hashable, hashable) Make path instances hashable
  *  Merge pull request #122 from snopoke/snopoke-patch-1
  *  Add more detail to filter docs.
  *  remove incorrect parenthesis in filter examples
  *  Merge pull request #119 from snopoke/patch-1
  *  add 'sub' line with function param names
  *  readme formatting fixes
  *  chore(history): update
  *  Update __init__.py

1.5.3 / 2021-07-05
==================

  * Update __init__.py
  * Update setup.py
  * Merge pull request #72 from kaapstorm/find_or_create
  * Tests
  * Add `update_or_create()` method
  * Merge pull request #68 from kaapstorm/example_tests
  * Merge pull request #70 from kaapstorm/exceptions
  * Add/fix `__eq__()`
  * Add tests based on Stefan Goessner's examples
  * Tests
  * Allow callers to catch JSONPathErrors

v1.5.2 / 2020-09-07
===================

  * Merge pull request #41 from josephwhite13/allow-dictionary-filtering
  * Merge pull request #48 from back2root/master
  * Check for null value.
  * Merge pull request #40 from memborsky/add-regular-expression-contains-support
  * feat: support regular expression for performing contains (=~) filtering
  * if datum.value is a dictionary, filter on the list of values

1.5.1 / 2020-03-09
==================

  * feat(version): bump
  * fix(setup): strip extension

v1.5.0 / 2020-03-06
===================

  * feat(version): bump to 1,5.0
  * Merge pull request #13 from dcreemer/master
  * fix(travis): remove python 3.4 (deprecated)
  * refactor(docs): delete coverage badge
  * Merge pull request #25 from rahendatri/patch-1
  * Merge pull request #26 from guandalf/contains_operator
  * Merge pull request #31 from borysvorona/master
  * refactor(travis): update python versions
  * Merge pull request #34 from dchourasia/patch-1
  * Updated Filter.py to implement update function
  * added hook for catching null value instead of empty list in path
  * Ignore vscode folder
  * Contains operator implementation
  * Update requirements-dev.txt
  * setuptools>=18.5
  * update setuptools
  * update cryptography
  * new version of cryptography requires it
  * entry point conflict with https://pypi.org/project/jsonpath/
  * add str() method
  * clean up
  * remove extra print()
  * refactor(docs): remove codesponsor
  * feat(docs): add sponsor banner
  * Update .travis.yml
  * feat(History): add History file
  * fix(travis-ci): ignore versions
  * feat(requirements): add missing pytest-cov dependency
  * refactor(requirements): use version contraint
  * fix: remove .cache files
  * feat: add required files
  * fix(travis-ci): install proper packages
  * refactor(setup.py): update description
  * refactor(docs): remove downloads badge
  * fix(tests): pass unit tests
  * feat(docs): add TravisCI and PyPI badges
  * Merge pull request #2 from tomas-fp/master
  * feat(docs): update readme notes
  * feat(setup): increase version
  * Merge pull request #1 from kmmbvnr/patch-1
  * Fix github url on pypi

v1.4.3 / 2017-08-24
===================

  * fix(travis-ci): ignore versions
  * feat(requirements): add missing pytest-cov dependency
  * refactor(requirements): use version contraint
  * fix: remove .cache files
  * feat: add required files
  * fix(travis-ci): install proper packages
  * refactor(setup.py): update description
  * refactor(docs): remove downloads badge
  * fix(tests): pass unit tests
  * feat(docs): add TravisCI and PyPI badges
  * Merge pull request #2 from tomas-fp/master
  * feat(docs): update readme notes
  * feat(setup): increase version
  * Merge pull request #1 from kmmbvnr/patch-1
  * Fix github url on pypi
