"""
Script that computes descriptive statistics mean, median, mode, variance,
standard deviation.
"""

import argparse
import time


def initilize_parser():
    """
    Initializes argparser to accept params in file execution.

    file: name of the file.
    """
    parser = argparse.ArgumentParser(
        prog="compute_statistics",
        description="Computes descriptive statistics from a file with numbers"
    )

    parser.add_argument("file", help="The name of the file to process.")
    args = parser.parse_args()
    return args


def file_to_list(file_path: str):
    """
    Returns list of numbers in file, replacing invalid lines with 'nan'.

    :param file_path: file route
    :type file_path: str
    :return: (numbers_list, invalid_count)
    :rtype: tuple[list, int]
    """
    lines_list = []
    invalid_count = 0

    with open(file_path, "r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            raw = line.rstrip("\n")
            s = raw.strip()

            if s == "":
                print(f"[ERROR] Line {line_no}: empty line -> treated as nan")
                lines_list.append("nan")
                invalid_count += 1
                continue

            try:
                value = float(s)
                if value == float("inf") or value == float("-inf"):
                    raise ValueError("Infinity is not allowed")

                lines_list.append(value)
            except ValueError:
                print(f"[ERROR] Line {line_no}: invalid float '{raw}' -> treated as nan")
                lines_list.append("nan")
                invalid_count += 1

    return lines_list, invalid_count


def compute_mean(values: list) -> tuple[float, int]:
    """
    Computes mean using basic summation.

    :param values: list of numbers
    :type values: list
    :return: (mean, valid_count)
    :rtype: tuple[float, int]
    """
    total = 0.0
    count = 0

    for v in values:
        if not isinstance(v, float):
            continue
        total += v
        count += 1

    if count == 0:
        return float("nan"), 0

    return total / count, count


def compute_median(values: list) -> float:
    """
    Computes median.

    :param values: list of numbers
    :type values: list
    :return: median
    :rtype: float
    """
    valid = []
    for v in values:
        if isinstance(v, float):
            valid.append(v)

    n = len(valid)
    if n == 0:
        return float("nan")

    valid.sort()
    mid = n // 2

    if n % 2 == 1:
        return float(valid[mid])

    return (valid[mid - 1] + valid[mid]) / 2.0


def compute_mode(values: list):
    """
    Computes mode using a frequency dictionary.
    If multiple modes exist, returns a list of all modes.
    If all valid values appear once, returns 'nan'.

    :param values: list of numbers
    :type values: list
    :return: mode(s) or 'nan'
    """
    freq = {}
    valid_count = 0

    for v in values:
        if not isinstance(v, float):
            continue
        valid_count += 1
        freq[v] = freq.get(v, 0) + 1

    if valid_count == 0:
        return "nan"

    max_count = 0
    for _, count in freq.items():
        max_count = max(max_count, count)

    if max_count == 1:
        return "nan"

    modes = []
    for value, count in freq.items():
        if count == max_count:
            modes.append(value)

    return sorted(modes)


def compute_variance(values: list, mean_value: float) -> float:
    """
    Computes population variance.

    :param values: list of numbers.
    :type values: list
    :param mean_value: mean of valid floats
    :type mean_value: float
    :return: variance
    :rtype: float
    """
    total_sq_dev = 0.0
    count = 0

    for v in values:
        if not isinstance(v, float):
            continue
        diff = v - mean_value
        total_sq_dev += diff * diff
        count += 1

    if count == 0:
        return float("nan")

    return total_sq_dev / count


def compute_standard_deviation(variance_value: float) -> float:
    """
    Computes standard deviation as sqrt(variance) using Newton's method.

    :param variance_value: variance
    :type variance_value: float
    :return: standard deviation
    :rtype: float
    """

    if variance_value < 0:
        return float("nan")

    if variance_value == 0:
        return 0.0

    x = variance_value
    guess = x if x >= 1 else 1.0

    for _ in range(30):
        guess = 0.5 * (guess + x / guess)

    return guess


def statistics_to_file(stats: dict, time_elapsed: float):
    """
    Writes statistics results to StatisticsResults.txt.
    """
    with open("StatisticsResults.txt", "w", encoding="utf-8") as f:
        f.write(f"Execution time: {time_elapsed:.6f} seconds\n")
        f.write(f"Valid numbers: {stats["valid_count"]}\n")
        f.write(f"Invalid lines: {stats["invalid_count"]}\n\n")

        f.write("Descriptive Statistics\n")
        f.write("----------------------\n")
        f.write(f"Mean: {stats["mean"]}\n")
        f.write(f"Median: {stats["median"]}\n")
        f.write(f"Mode: {stats["mode"]}\n")
        f.write(f"Variance: {stats["variance"]}\n")
        f.write(f"Standard Deviation: {stats["std_dev"]}\n")


def main():
    """
    Program entry point.
    """
    start = time.time()

    args = initilize_parser()
    filename = args.file

    numbers_list, invalid_count = file_to_list(filename)

    mean_value, valid_count = compute_mean(numbers_list)
    median_value = compute_median(numbers_list)
    mode_value = compute_mode(numbers_list)
    variance_value = compute_variance(numbers_list, mean_value)
    std_dev_value = compute_standard_deviation(variance_value)

    end = time.time()
    execution_time = end - start

    stats = {
        "invalid_count": invalid_count,
        "mean": mean_value,
        "median": median_value,
        "valid_count": valid_count,
        "mode": mode_value,
        "variance": variance_value,
        "std_dev": std_dev_value,
    }

    statistics_to_file(stats, execution_time)

    print(f"Valid numbers: {valid_count}")
    print(f"Invalid lines: {invalid_count}")
    print("Descriptive Statistics")
    print("----------------------")
    print(f"Mean: {mean_value:.2f}")
    print(f"Median: {median_value:.2f}")
    print(f"Mode: {mode_value}")
    print(f"Variance: {variance_value:.2f}")
    print(f"Standard Deviation: {std_dev_value:.2f}")
    print(f"Execution took {execution_time:.6f} seconds")


if __name__ == "__main__":
    main()
