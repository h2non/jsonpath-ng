## [Unreleased]

## Added
- Support Python 3.13 and 3.14
- Typing for IDE autocomplete
- Support for EMOJI and CJK Unicode
- Support for `DatumInContext` in-place updating

## Changed
- Rename `ExtentedJsonPathParser`

## Fixed
- Fix `False` and `None` values
- Fix single constant case
- Update field filter to resolve wildcard path issue
- Vendor copy of ply and remove pickly support from the vendored copy to resolve [CVE-2025-56005](https://nvd.nist.gov/vuln/detail/CVE-2025-56005) 

## Removed
- Python 3.8 and 3.9 no longer supported

[Unreleased]: https://github.com/h2non/jsonpath-ng/compare/v1.7.0...HEAD
