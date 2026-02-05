"""
Tests for compute_statistics.py
"""

import pytest

from compute_statistics import (
    file_to_list,
    compute_mean,
    compute_median,
    compute_mode,
    compute_variance,
    compute_standard_deviation,
    statistics_to_file,
)


def test_compute_mean_with_floats():
    """
    Checks correct mean for float values.
    """
    mean_value, valid_count = compute_mean([1.5, 2.5, 3.0])
    assert valid_count == 3
    assert mean_value == pytest.approx(7.0 / 3.0)


def test_compute_median_even_count():
    """
    Checks correct median for even numbers.
    """
    assert compute_median([1.0, 4.0, 2.0, 3.0]) == 2.5


def test_compute_mode_no_mode_all_unique():
    """
    Checks correct output when all values are unique.
    """
    assert compute_mode([1.0, 2.0, 3.0]) == "nan"


def test_compute_variance_simple_case():
    """
    Checks variance in a simple known case.
    """
    values = [1.0, 2.0, 3.0]
    mean_value, _ = compute_mean(values)
    var_value = compute_variance(values, mean_value)
    assert var_value == pytest.approx(2.0 / 3.0)


def test_compute_standard_deviation_matches_sqrt():
    """
    Checks standard deviation matches sqrt(variance) for a known value.
    """
    var_value = 4.0
    std_value = compute_standard_deviation(var_value)
    assert std_value == pytest.approx(2.0)


def test_file_to_list_invalid_and_empty_lines(tmp_path, capsys):
    """
    Verifies correctness of invalid data and error capture.
    """
    p = tmp_path / "input.txt"
    p.write_text("10.5\nabc\n\n   \n-3.25\n", encoding="utf-8")

    numbers, invalid_count = file_to_list(str(p))

    assert numbers == [10.5, "nan", "nan", "nan", -3.25]
    assert invalid_count == 3

    captured = capsys.readouterr().out
    assert "[ERROR] Line 2:" in captured
    assert "[ERROR] Line 3:" in captured
    assert "[ERROR] Line 4:" in captured


def test_statistics_to_file_creates_output_file(tmp_path, monkeypatch):
    """
    Verifies correct writing to StatisticsResults.txt.
    """
    monkeypatch.chdir(tmp_path)
    stats = {
        "valid_count": 3,
        "invalid_count": 1,
        "mean": 2.0,
        "median": 2.0,
        "mode": [2.0],
        "variance": 0.5,
        "std_dev": 0.707106,
    }
    statistics_to_file(stats, time_elapsed=0.123456)

    out_path = tmp_path / "StatisticsResults.txt"
    assert out_path.exists()

    content = out_path.read_text(encoding="utf-8")
    assert "Execution time: 0.123456 seconds" in content
    assert "Valid numbers: 3" in content
    assert "Invalid lines: 1" in content
    assert "Descriptive Statistics" in content


def test_full_pipeline_file_to_output(tmp_path, monkeypatch):
    """
    Test complete pipeline.
    """
    monkeypatch.chdir(tmp_path)

    inp = tmp_path / "nums.txt"
    inp.write_text("0\n7.5\n-8\nbad\n2.5\n", encoding="utf-8")

    numbers, invalid_count = file_to_list(str(inp))

    mean_value, valid_count = compute_mean(numbers)
    median_value = compute_median(numbers)
    mode_value = compute_mode(numbers)
    variance_value = compute_variance(numbers, mean_value)
    std_dev_value = compute_standard_deviation(variance_value)

    assert numbers == [0.0, 7.5, -8.0, "nan", 2.5]
    assert invalid_count == 1
    assert valid_count == 4

    stats = {
        "valid_count": valid_count,
        "invalid_count": invalid_count,
        "mean": mean_value,
        "median": median_value,
        "mode": mode_value,
        "variance": variance_value,
        "std_dev": std_dev_value,
    }
    statistics_to_file(stats, time_elapsed=0.0)

    out_path = tmp_path / "StatisticsResults.txt"
    text = out_path.read_text(encoding="utf-8")

    assert "Descriptive Statistics" in text
    assert "Mean:" in text
    assert "Median:" in text
    assert "Variance:" in text
    assert "Standard Deviation:" in text
    assert "Invalid lines: 1" in text
