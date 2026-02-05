"""
Tests for convert_numbers.py
"""

import pytest

from convert_numbers import (
    file_to_list,
    numbers_to_binary,
    numbers_to_hexadecimal,
    arrays_to_file,
)


def test_numbers_to_binary_zero():
    """
    Checks correct output to binary for 0.
    """
    assert numbers_to_binary([0]) == ["0"]

def test_numbers_to_hexadecimal_zero():
    """
    Checks correct output to hexadecimal for 0.
    """
    assert numbers_to_hexadecimal([0]) == ["0"]

def test_numbers_to_binary_negative_numbers():
    """
    Checks correct output to binary for negative numbers.
    """
    # -5 -> -101, -1 -> -1, -2 -> -10
    assert numbers_to_binary([-5, -1, -2]) == ["-101", "-1", "-10"]

def test_numbers_to_hexadecimal_negative_numbers():
    """
    Checks correct output to hexadecimal for negative numbers.
    """
    # -26 -> -1a, -15 -> -f
    assert numbers_to_hexadecimal([-26, -15]) == ["-1a", "-f"]

def test_file_to_list_invalid_and_empty_lines(tmp_path, capsys):
    """
    Verifies correctness of invalidad data.
    Verifies error capture.
    
    :param tmp_path: Temporary file path for testing.
    :param capsys: Fixture to capture output
    """
    p = tmp_path / "input.txt"
    # includes: valid int, invalid token, empty line, whitespace, valid negative
    p.write_text("10\nabc\n\n   \n-3\n", encoding="utf-8")

    numbers, invalid_count = file_to_list(str(p))

    assert numbers == [10, "nan", "nan", "nan", -3]
    assert invalid_count == 3

    captured = capsys.readouterr().out
    assert "[ERROR] Line 2:" in captured
    assert "[ERROR] Line 3:" in captured
    assert "[ERROR] Line 4:" in captured


def test_converters_pass_through_nan_for_non_ints():
    """
    Verifies correct transformation of data.
    """
    data = [3, "nan", 0, None, -2]
    assert numbers_to_binary(data) == ["11", "nan", "0", "nan", "-10"]
    assert numbers_to_hexadecimal(data) == ["3", "nan", "0", "nan", "-2"]


def test_file_to_list_missing_file_raises():
    """
    Verifies correct error on unexistant file.
    """
    with pytest.raises(FileNotFoundError):
        file_to_list("this_file_should_not_exist_12345.txt")


def test_arrays_to_file_creates_output_file(tmp_path, monkeypatch):
    """
    Verifies correct writting to file.
    
    :param tmp_path:  Temporary file path for testing.
    :param monkeypatch: Fixture to mock file path.
    """

    monkeypatch.chdir(tmp_path)

    original = [0, -2, "nan", 5]
    binaries = ["0", "-10", "nan", "101"]
    hexes = ["0", "-2", "nan", "5"]

    arrays_to_file(original, binaries, hexes, time_elapsed=0.123456, invalid_count=1)

    out_path = tmp_path / "ConversionResults.txt"
    assert out_path.exists()

    content = out_path.read_text(encoding="utf-8")
    assert "Execution time: 0.123456 seconds" in content
    assert "Invalid lines: 1" in content
    assert "Number" in content and "Binary" in content and "Hex" in content


def test_full_pipeline_file_to_output(tmp_path, monkeypatch):
    """
    Test complete pipeline.
    
    :param tmp_path:  Temporary file path for testing.
    :param monkeypatch: Fixture to mock file path.
    """
    monkeypatch.chdir(tmp_path)

    inp = tmp_path / "nums.txt"
    inp.write_text("0\n7\n-8\nbad\n", encoding="utf-8")

    numbers, invalid_count = file_to_list(str(inp))
    binaries = numbers_to_binary(numbers)
    hexes = numbers_to_hexadecimal(numbers)

    assert numbers == [0, 7, -8, "nan"]
    assert invalid_count == 1
    assert binaries == ["0", "111", "-1000", "nan"]
    assert hexes == ["0", "7", "-8", "nan"]

    arrays_to_file(numbers, binaries, hexes, time_elapsed=0.0, invalid_count=invalid_count)

    out_path = tmp_path / "ConversionResults.txt"
    text = out_path.read_text(encoding="utf-8")

    assert "0" in text
    assert "111" in text
    assert "-1000" in text
    assert "nan" in text
