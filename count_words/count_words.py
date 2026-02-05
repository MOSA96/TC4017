"""
Script that counts distinct words and their frequency in a file.
"""

import argparse
import time


def initilize_parser():
    """
    Initializes argparser to accept params in file execution.

    file: name of the file to process.
    """
    parser = argparse.ArgumentParser(
        prog='count_words',
        description='Counts distinct words and their frequency in a file'
    )

    parser.add_argument('file', help="The name of the file to process.")
    args = parser.parse_args()
    return args


def file_to_words(file_path: str):
    """
    Reads a file and extracts words separated by whitespace.

    :param file_path: file route
    :type file_path: str
    :return: (words_list, invalid_count)
    :rtype: tuple[list[str], int]
    """
    words_list = []
    invalid_count = 0

    with open(file_path, 'r', encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            raw = line.rstrip("\n")
            s = raw.strip()

            if s == "":
                continue

            tokens = s.split()

            for token in tokens:
                if token.isalpha():
                    words_list.append(token.lower())
                else:
                    print(f"[ERROR] Line {line_no}: invalid token '{token}' -> ignored")
                    invalid_count += 1

    return words_list, invalid_count


def count_word_frequencies(words: list) -> dict:
    """
    Counts frequencies of words.

    :param words: list of valid words
    :type words: list
    :return: mapping of word -> frequency
    :rtype: dict
    """
    freqs = {}
    for w in words:
        if w in freqs:
            freqs[w] += 1
        else:
            freqs[w] = 1
    return freqs


def results_to_file(freqs: dict, time_elapsed: float, invalid_count: int):
    """
    Writes results to WordCountResults.txt.

    :param freqs: dict of count words
    :type freqs: dict
    :param time_elapsed: execution time in seconds
    :type time_elapsed: float
    :param invalid_count: number of invalid tokens
    :type invalid_count: int
    """
    items = list(freqs.items())
    items.sort(key=lambda x: x[0])

    with open("WordCountResults.txt", "w", encoding="utf-8") as f:
        f.write(f"Execution time: {time_elapsed:.6f} seconds\n")
        f.write(f"Invalid tokens: {invalid_count}\n\n")

        f.write(f"{'Word':<20}  {'Count':>10}\n")
        f.write(f"{'-'*20}  {'-'*10}\n")

        for word, count in items:
            f.write(f"{word:<20}  {str(count):>10}\n")


def main():
    """
    Program entry point.

    Parses command-line arguments to get an input file path, reads words from
    the file, counts distinct words and their frequencies, measures total
    runtime, writes results to WordCountResults.txt, and prints results to the
    console. Invalid tokens are reported but do not stop execution.
    """
    start = time.time()

    args = initilize_parser()
    filename = args.file

    words_list, invalid_count = file_to_words(filename)
    freqs = count_word_frequencies(words_list)

    end = time.time()
    execution_time = end - start

    results_to_file(freqs, execution_time, invalid_count)

    items = list(freqs.items())
    items.sort(key=lambda x: x[0])

    print("Word frequencies:")
    print(f"{'Word':<20}  {'Count':>10}")
    print(f"{'-'*20}  {'-'*10}")

    for word, count in items:
        print(f"{word:<20}  {str(count):>10}")

    print(f"Invalid tokens: {invalid_count}")
    print(f"Execution took {execution_time:.6f} seconds")


if __name__ == '__main__':
    main()
