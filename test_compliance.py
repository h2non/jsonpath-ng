#!/usr/bin/env python3
"""
JSONPath Compliance Test Suite Runner
Tests jsonpath-ng implementation against the official JSONPath compliance test suite.
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Union

import pytest
from jsonpath_ng import parse
from jsonpath_ng.exceptions import JsonPathParserError


def load_compliance_tests() -> List[Dict[str, Any]]:
    """Load the compliance test suite from cts.json"""
    cts_path = Path(__file__).parent / "jsonpath-compliance-test-suite" / "cts.json"
    if not cts_path.exists():
        raise FileNotFoundError(f"Compliance test suite not found at {cts_path}")
    
    with open(cts_path, 'r') as f:
        data = json.load(f)
    
    return data.get('tests', [])


def normalize_result(result: Any) -> Any:
    """Normalize result for comparison"""
    if isinstance(result, list):
        return [normalize_result(item) for item in result]
    elif isinstance(result, dict):
        return {k: normalize_result(v) for k, v in result.items()}
    else:
        return result


def run_jsonpath_query(selector: str, document: Any) -> tuple[List[Any], List[str]]:
    """
    Run a JSONPath query and return both values and paths.
    Returns (values, paths) tuple.
    """
    try:
        parsed = parse(selector)
        matches = parsed.find(document)
        
        values = [match.value for match in matches]
        paths = [str(match.full_path) for match in matches]
        
        return values, paths
    except Exception as e:
        # For invalid selectors, we expect an exception
        raise e


class TestComplianceSuite:
    """Test class for JSONPath compliance suite"""
    
    @pytest.mark.parametrize("test_case", load_compliance_tests())
    def test_compliance(self, test_case: Dict[str, Any]):
        """Test a single compliance test case"""
        name = test_case.get('name', 'unnamed')
        selector = test_case['selector']
        
        # Check if this is an invalid selector test
        if test_case.get('invalid_selector', False):
            # This selector should raise an exception
            document = test_case.get('document', {})
            with pytest.raises((JsonPathParserError, Exception)):
                run_jsonpath_query(selector, document)
            return
        
        # For valid selectors, we need document and expected result
        if 'document' not in test_case:
            pytest.skip(f"Test case '{name}' missing document")
            return
            
        document = test_case['document']
        
        try:
            actual_values, actual_paths = run_jsonpath_query(selector, document)
        except Exception as e:
            pytest.fail(f"Unexpected exception for test '{name}': {e}")
            return
        
        # Check results
        if 'result' in test_case:
            # Single expected result
            expected_values = test_case['result']
            normalized_actual = normalize_result(actual_values)
            normalized_expected = normalize_result(expected_values)
            
            assert normalized_actual == normalized_expected, (
                f"Test '{name}' failed:\n"
                f"Selector: {selector}\n"
                f"Document: {document}\n"
                f"Expected: {normalized_expected}\n"
                f"Actual: {normalized_actual}"
            )
        
        elif 'results' in test_case:
            # Multiple valid results (non-deterministic)
            expected_results = test_case['results']
            normalized_actual = normalize_result(actual_values)
            
            # Check if actual result matches any of the expected results
            match_found = False
            for expected in expected_results:
                normalized_expected = normalize_result(expected)
                if normalized_actual == normalized_expected:
                    match_found = True
                    break
            
            assert match_found, (
                f"Test '{name}' failed - no matching result:\n"
                f"Selector: {selector}\n"
                f"Document: {document}\n"
                f"Expected one of: {expected_results}\n"
                f"Actual: {normalized_actual}"
            )
        
        # Check paths if provided
        if 'result_paths' in test_case:
            expected_paths = test_case['result_paths']
            assert actual_paths == expected_paths, (
                f"Test '{name}' path mismatch:\n"
                f"Selector: {selector}\n"
                f"Expected paths: {expected_paths}\n"
                f"Actual paths: {actual_paths}"
            )


def main():
    """Run compliance tests directly"""
    tests = load_compliance_tests()
    print(f"Loaded {len(tests)} compliance tests")
    
    passed = 0
    failed = 0
    skipped = 0
    
    for i, test_case in enumerate(tests):
        name = test_case.get('name', f'test_{i}')
        selector = test_case['selector']
        
        try:
            print(f"Running test: {name}")
            
            # Check if invalid selector test
            if test_case.get('invalid_selector', False):
                document = test_case.get('document', {})
                try:
                    run_jsonpath_query(selector, document)
                    print(f"  FAIL: Expected exception for invalid selector '{selector}'")
                    failed += 1
                except:
                    print(f"  PASS: Correctly rejected invalid selector")
                    passed += 1
                continue
            
            # Skip if no document provided
            if 'document' not in test_case:
                print(f"  SKIP: No document provided")
                skipped += 1
                continue
                
            document = test_case['document']
            
            try:
                actual_values, actual_paths = run_jsonpath_query(selector, document)
            except Exception as e:
                print(f"  FAIL: Unexpected exception: {e}")
                failed += 1
                continue
            
            # Check results
            if 'result' in test_case:
                expected = test_case['result']
                if normalize_result(actual_values) == normalize_result(expected):
                    print(f"  PASS")
                    passed += 1
                else:
                    print(f"  FAIL: Expected {expected}, got {actual_values}")
                    failed += 1
                    
            elif 'results' in test_case:
                expected_results = test_case['results']
                match_found = any(
                    normalize_result(actual_values) == normalize_result(expected)
                    for expected in expected_results
                )
                if match_found:
                    print(f"  PASS")
                    passed += 1
                else:
                    print(f"  FAIL: Got {actual_values}, expected one of {expected_results}")
                    failed += 1
            else:
                print(f"  SKIP: No expected result")
                skipped += 1
                
        except Exception as e:
            print(f"  ERROR: {e}")
            failed += 1
    
    print(f"\nResults: {passed} passed, {failed} failed, {skipped} skipped")
    return failed == 0


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)