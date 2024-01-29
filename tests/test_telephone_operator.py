import os
from unittest import TestCase
from faker import Faker

from telephone_operator import OperatorProcessor, validate_operator_line_in_file

fake = Faker()


class TelephoneOperatorTestCase(TestCase):
    def doCleanups(self):
        if os.path.exists("tests/test_operator_file.txt"):
            os.remove("tests/test_operator_file.txt")
        if os.path.exists("tests/test_operator_file2.txt"):
            os.remove("tests/test_operator_file2.txt")

    def test_validate_operator_line_in_file(self):
        self.assertRaises(ValueError, validate_operator_line_in_file, "")
        self.assertRaises(ValueError, validate_operator_line_in_file, "prefix")
        self.assertRaises(ValueError, validate_operator_line_in_file, "prefix price")
        self.assertRaises(ValueError, validate_operator_line_in_file, "prefix\tprice\textra")
        self.assertRaises(ValueError, validate_operator_line_in_file, "prefix\tprice")
        price = fake.pyfloat()
        self.assertEqual(validate_operator_line_in_file(f"prefix\t{price}"), ("prefix", price))

    def test_update_operators_set(self):
        operator_processor = OperatorProcessor()
        first_prefix, first_price = fake.pystr(), fake.pyfloat()
        operator_processor.update_operators_set([f"{first_prefix}\t{first_price}"], "operator_name")
        self.assertEqual(operator_processor.operators[first_prefix][0], (first_price, "operator_name"))
        second_price = first_price + 1
        operator_processor.update_operators_set([f"{first_prefix}\t{second_price}"], "operator_name")
        self.assertEqual(operator_processor.operators[first_prefix][0], (first_price, "operator_name"))
        self.assertEqual(operator_processor.operators[first_prefix][1], (second_price, "operator_name"))

    def test_preprocess_operator_file(self):
        operator_processor = OperatorProcessor()
        first_prefix, first_price = fake.pystr(), fake.pyfloat()
        second_price = first_price + 1
        prefix2, price2 = fake.pystr(), fake.pyfloat()
        with open("tests/test_operator_file.txt", "w") as f:
            f.write(f"{first_prefix}\t{first_price}\n")
            f.write(f"{first_prefix}\t{second_price}\n")
            f.write(f"{prefix2}\t{price2}\n")
        operator_processor.preprocess_operator_file("tests/test_operator_file.txt")
        expected_output = {
            first_prefix: [(first_price, "test_operator_file"), (second_price, "test_operator_file")],
            prefix2: [(price2, "test_operator_file")]
        }
        self.assertEqual(operator_processor.operators[first_prefix], expected_output[first_prefix])
        self.assertEqual(operator_processor.operators[prefix2], expected_output[prefix2])

    def test_preprocess_list_operator_files(self):
        operator_processor = OperatorProcessor()
        first_prefix, first_price = fake.pystr(), fake.pyfloat()
        second_price = first_price + 1
        prefix2, price2 = fake.pystr(), fake.pyfloat()
        with open("tests/test_operator_file.txt", "w") as f:
            f.write(f"{first_prefix}\t{first_price}\n")
            f.write(f"{first_prefix}\t{second_price}\n")
        with open("tests/test_operator_file2.txt", "w") as f:
            f.write(f"{prefix2}\t{price2}\n")
        operator_processor.preprocess_list_operator_files([
            "tests/test_operator_file.txt",
            "tests/test_operator_file2.txt"
        ])
        expected_output = {
            first_prefix: [(first_price, "test_operator_file"), (second_price, "test_operator_file")],
            prefix2: [(price2, "test_operator_file2")]
        }
        self.assertEqual(operator_processor.operators[first_prefix], expected_output[first_prefix])
        self.assertEqual(operator_processor.operators[prefix2], expected_output[prefix2])

    def test_find_best_price(self):
        operator_processor = OperatorProcessor()
        first_prefix, first_price = fake.pystr(), fake.pyfloat()
        second_price = first_price + 1
        prefix2, price2 = fake.pystr(), fake.pyfloat()
        operator_processor.operators = {
            first_prefix: [(first_price, "test_operator_file"), (second_price, "test_operator_file")],
            prefix2: [(price2, "test_operator_file")]
        }
        self.assertEqual(operator_processor.find_best_price(first_prefix), (first_prefix, (first_price, "test_operator_file")))
        self.assertEqual(operator_processor.find_best_price(prefix2), (prefix2, (price2, "test_operator_file")))
        self.assertEqual(operator_processor.find_best_price(prefix2 + "1"), (prefix2, (price2, "test_operator_file")))
        self.assertIsNone(operator_processor.find_best_price("1" + prefix2))


