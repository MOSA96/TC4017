import argparse
import time

def initilize_parser():
    parser = argparse.ArgumentParser(
        prog='Converter',
        description='Converts file numbers to binary and hexadecimal base'
    )

    parser.add_argument('file', help="The name of the file to process.")
    args = parser.parse_args()
    return args


def file_to_list(file_path: str):
    lines_list = []
    invalid_count = 0

    with open(file_path, 'r', encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            raw = line.rstrip("\n")
            s = raw.strip()

            if s == "":
                print(f"[ERROR] Line {line_no}: empty line -> treated as nan")
                lines_list.append('nan')
                invalid_count += 1
                continue

            try:
                lines_list.append(int(s)) 
            except ValueError:
                print(f"[ERROR] Line {line_no}: invalid integer '{raw}' -> treated as nan")
                lines_list.append('nan')
                invalid_count += 1

    return lines_list, invalid_count


def numbers_to_binary(numbers_to_convert: list) -> list[str]:
    binary_arr = []
    for i in numbers_to_convert:
        if not isinstance(i, int):
            binary_arr.append('nan')
            continue

        if i == 0:
            binary_arr.append('0')
            continue

        sign = ''
        if i < 0:
            sign = '-'
            i = -i

        bits = []
        while i > 0:
            bits.append(str(i % 2))
            i //= 2

        binary_arr.append(sign + ''.join(reversed(bits)))
    return binary_arr


def numbers_to_hexadecimal(numbers_to_convert: list) -> list[str]:
    hexadecimal_arr = []
    hex_chars = '0123456789abcdef'

    for i in numbers_to_convert:
        if not isinstance(i, int):
            hexadecimal_arr.append('nan')
            continue

        if i == 0:
            hexadecimal_arr.append('0')
            continue

        sign = ''
        if i < 0:
            sign = '-'
            i = -i

        digits = []
        while i > 0:
            digits.append(hex_chars[i % 16])
            i //= 16

        hexadecimal_arr.append(sign + ''.join(reversed(digits)))

    return hexadecimal_arr


def arrays_to_file(original_arr: list, decimal_arr: list, hexadecimal_arr: list, time_elapsed: float, invalid_count: int):
    results = zip(original_arr, decimal_arr, hexadecimal_arr)

    with open("ConversionResults.txt", "w", encoding="utf-8") as f:
        f.write(f"Execution time: {time_elapsed:.6f} seconds\n")
        f.write(f"Invalid lines: {invalid_count}\n\n")

        f.write(f"{'Number':>8}  {'Binary':>12}  {'Hex':>8}\n")
        f.write(f"{'-'*8}  {'-'*12}  {'-'*8}\n")

        for orig, binary, hexa in results:
            f.write(f"{str(orig):>8}  {str(binary):>12}  {str(hexa):>8}\n")


def main():
    start = time.time()

    args = initilize_parser()
    filename = args.file

    numbers_list, invalid_count = file_to_list(filename)
    binary_list = numbers_to_binary(numbers_list)
    hexadecimal_list = numbers_to_hexadecimal(numbers_list)

    end = time.time()
    execution_time = end - start

    arrays_to_file(numbers_list, binary_list, hexadecimal_list, execution_time, invalid_count)

    print(f'Original: {numbers_list}')
    print(f'Binary: {binary_list}')
    print(f'Hexadecimal {hexadecimal_list}')
    print(f'Invalid lines: {invalid_count}')
    print(f'Execution took {execution_time:.6f} seconds')


if __name__ == '__main__':
    main()
