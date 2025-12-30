import pytest
from processor import DataTransformation, ProcessingEngine

def test_salary_transformation():
    transformer = DataTransformation()
    input_row = {'id': 1, 'value': 1000}
    result = transformer.transform(input_row)

    # Use pytest.approx to handle the tiny floating point differences
    assert result['value'] == pytest.approx(1100.0)

def test_error_handling():
    transformer = DataTransformation()
    bad_row = {'id': 2, 'value': 'invalid_string'}
    result = transformer.transform(bad_row)
    assert result is None

def test_parallel_processing():
    transformer = DataTransformation()
    engine = ProcessingEngine(processor=transformer, max_workers=2)
    test_data = [{'id': i, 'value': 100} for i in range(10)]

    results = engine.run_parallel(test_data)

    assert len(results) == 10
    # Update this line to use approx!
    assert results[0]['value'] == pytest.approx(110.0)