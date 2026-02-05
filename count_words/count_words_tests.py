"""
Tests for wordCount.py
"""

import pytest

from count_words import (
    file_to_words,
    count_word_frequencies,
    results_to_file,
)


def test_file_to_words_valid_and_invalid_tokens(tmp_path, capsys):
    """
    Verifies valid words.
    """
    p = tmp_path / "input.txt"
    p.write_text(
        "Hello world\nhi, there 123\nMiXeD case\nA1B test\n\n   \n",
        encoding="utf-8"
    )

    words, invalid_count = file_to_words(str(p))

    assert words == ["hello", "world", "there", "mixed", "case", "test"]
    assert invalid_count == 3

    captured = capsys.readouterr().out
    assert "[ERROR] Line 2:" in captured
    assert "invalid token 'hi,'" in captured
    assert "invalid token '123'" in captured
    assert "[ERROR] Line 4:" in captured
    assert "invalid token 'A1B'" in captured


def test_file_to_words_skips_empty_and_whitespace_only_lines(tmp_path, capsys):
    """
    Verifies empty lines are ignored and do not count as invalid tokens.
    """
    p = tmp_path / "input.txt"
    p.write_text("\n   \n\t\nword\n\n", encoding="utf-8")

    words, invalid_count = file_to_words(str(p))

    assert words == ["word"]
    assert invalid_count == 0
    assert capsys.readouterr().out == ""


def test_file_to_words_case_insensitive_lowercasing(tmp_path):
    """
    Verifies words are normalized to lowercase.
    """
    p = tmp_path / "input.txt"
    p.write_text("DOG Dog doG\nCaT cAt\n", encoding="utf-8")

    words, invalid_count = file_to_words(str(p))

    assert words == ["dog", "dog", "dog", "cat", "cat"]
    assert invalid_count == 0


def test_count_word_frequencies_basic():
    """
    Verifies correct counting of repeated words.
    """
    words = ["a", "b", "a", "c", "b", "a"]
    freqs = count_word_frequencies(words)
    assert freqs == {"a": 3, "b": 2, "c": 1}


def test_count_word_frequencies_empty_input():
    """
    Verifies empty input produces empty frequency map.
    """
    freqs = count_word_frequencies([])
    assert not freqs


def test_file_to_words_missing_file_raises():
    """
    Verifies correct error on unexistant file.
    """
    with pytest.raises(FileNotFoundError):
        file_to_words("this_file_should_not_exist_12345.txt")


def test_full_pipeline_file_to_output(tmp_path, monkeypatch, capsys):
    """
    Test complete pipeline.
    """
    monkeypatch.chdir(tmp_path)

    inp = tmp_path / "words.txt"
    inp.write_text("Dog cat dog\nCAT! 12 bird\nbird dog\n", encoding="utf-8")

    words, invalid_count = file_to_words(str(inp))
    freqs = count_word_frequencies(words)

    assert words == ["dog", "cat", "dog", "bird", "bird", "dog"]
    assert invalid_count == 2
    assert freqs == {"dog": 3, "cat": 1, "bird": 2}

    results_to_file(freqs, time_elapsed=0.0, invalid_count=invalid_count)

    out_path = tmp_path / "WordCountResults.txt"
    text = out_path.read_text(encoding="utf-8")

    assert "dog" in text
    assert "cat" in text
    assert "bird" in text

    captured = capsys.readouterr().out
    assert "[ERROR] Line 2:" in captured
    assert "invalid token 'CAT!'" in captured
    assert "invalid token '12'" in captured
