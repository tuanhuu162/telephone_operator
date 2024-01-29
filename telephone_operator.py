import os
from collections import defaultdict
from heapq import heappush
from typing import Tuple, Optional


def validate_operator_line_in_file(line: str) -> Tuple[str, float]:
    """
    Validate line in operator file
    :param line: line in file
    :return: prefix and price
    """
    line = line.strip()
    if not line:
        raise ValueError("Empty line")
    prefix_and_price = line.split()
    if len(prefix_and_price) != 2:
        raise ValueError(f"Invalid format in file, file format should be: prefix\tprice")
    return prefix_and_price[0], float(prefix_and_price[1])


class OperatorProcessor:

    def __init__(self):
        self.operators = defaultdict(list)

    def update_operators_set(self, operator_info: list[str], operator_name: str) -> None:
        """
        update operators set with new operator info
        :param operator_info: list of operator info
        :param operator_name: operator name
        :return:
        """
        for line in operator_info:
            prefix, price = validate_operator_line_in_file(line)
            heappush(self.operators[prefix], (price, operator_name))

    def preprocess_operator_file(self, file_path: str) -> None:
        """
        Process file contain prefix telephone number and price for a single operator.
        :param file_path:
        :return:
        """
        operator_name = os.path.basename(file_path)
        with open(file_path, 'r') as f:
            self.update_operators_set(f.readlines(), operator_name)

    def preprocess_list_operator_files(self, list_file_paths: list[str]) -> None:
        """
        Process list of file contain prefix telephone number and price for each operator.
        File name is operator name
        :param list_file_paths:
        :return:
        """
        for path in list_file_paths:
            self.preprocess_operator_file(path)

    def find_best_price(self, phone_number: str) -> Optional[Tuple[str, Tuple[float, str]]]:
        """
        Find best price for given phone number
        :param phone_number: phone number
        :return: best price and operator name
        """
        for i in range(len(phone_number), 0, -1):
            prefix = phone_number[:i]
            if prefix in self.operators:
                return prefix, self.operators[prefix][0]
        return None

    def find_best_price_for_all_phone_numbers(self, input_file_path: str, output_path: str) -> None:
        """
        Find best price for all phone numbers listed in input file
        :param input_file_path: input file contain list of phone numbers
        :param output_path: output file path
        :return: None
        """
        with open(input_file_path, 'r') as f, open(output_path, "w") as output_file:
            output_file.write("Phone number, Operator, Price\n")
            for line in f.readlines():
                phone_number = line.strip()
                best_price = self.find_best_price(phone_number)

                if best_price:
                    output_file.write(f"{phone_number}, {best_price[1][1]}, {best_price[1][0]}\n")
                else:
                    output_file.write(f"{phone_number}, not found,\n")
        print(f"Finished finding best price for all phone numbers in file {input_file_path} and write to {output_path}")
