from argparse import ArgumentParser

from telephone_operator import OperatorProcessor


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--list_operator_files", "-l", nargs="+", required=True, help="List of operator files")
    parser.add_argument("--phone_number_file", "-p", required=True, help="Phone number file path")
    parser.add_argument("--output_file", "-o", default="output.txt", help="Output file path")
    args = parser.parse_args()
    operator_processor = OperatorProcessor()
    operator_processor.preprocess_list_operator_files(args.list_operator_files)
    operator_processor.find_best_price_for_all_phone_numbers(args.phone_number_file, args.output_file)
