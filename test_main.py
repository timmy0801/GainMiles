import unittest
from unittest.mock import patch, MagicMock
from main import (
    validate_employee_id,
    validate_name,
    validate_email,
    validate_department,
    validate_salary,
    validate_join_date,
    submit_row,
)


class TestValidateEmployeeId(unittest.TestCase):
    def setUp(self):
        self.seen_ids = set()

    def test_valid_id(self):
        self.assertIsNone(validate_employee_id("E001", self.seen_ids))

    def test_none_value(self):
        self.assertEqual(validate_employee_id(None, self.seen_ids), "Employee ID is required")

    def test_duplicate_id(self):
        validate_employee_id("E001", self.seen_ids)
        self.assertEqual(validate_employee_id("E001", self.seen_ids), "Employee ID must be unique")

    def test_unique_ids_added_to_seen(self):
        validate_employee_id("E001", self.seen_ids)
        validate_employee_id("E002", self.seen_ids)
        self.assertEqual(self.seen_ids, {"E001", "E002"})


class TestValidateName(unittest.TestCase):
    def test_valid_name(self):
        self.assertIsNone(validate_name("John Chan"))

    def test_none_value(self):
        self.assertIsNotNone(validate_name(None))

    def test_empty_string(self):
        self.assertIsNotNone(validate_name(""))

    def test_name_at_max_length(self):
        self.assertIsNone(validate_name("A" * 50))

    def test_name_exceeds_max_length(self):
        self.assertIsNotNone(validate_name("A" * 51))

    def test_single_character_name(self):
        self.assertIsNone(validate_name("A"))


class TestValidateEmail(unittest.TestCase):
    def test_valid_email(self):
        self.assertIsNone(validate_email("john@company.com"))

    def test_none_value(self):
        self.assertIsNotNone(validate_email(None))

    def test_missing_at_sign(self):
        self.assertIsNotNone(validate_email("johncompany.com"))

    def test_missing_domain(self):
        self.assertIsNotNone(validate_email("john@"))

    def test_missing_tld(self):
        self.assertIsNotNone(validate_email("john@company"))

    def test_valid_subdomain_email(self):
        self.assertIsNone(validate_email("john.chan@mail.company.com"))


class TestValidateDepartment(unittest.TestCase):
    def test_valid_department(self):
        self.assertIsNone(validate_department("IT"))

    def test_none_value(self):
        self.assertIsNotNone(validate_department(None))

    def test_empty_string(self):
        self.assertIsNotNone(validate_department(""))

    def test_whitespace_only(self):
        self.assertIsNotNone(validate_department("   "))


class TestValidateSalary(unittest.TestCase):
    def test_valid_salary(self):
        self.assertIsNone(validate_salary(50000))

    def test_none_value(self):
        self.assertIsNotNone(validate_salary(None))

    def test_zero_salary(self):
        self.assertIsNotNone(validate_salary(0))

    def test_negative_salary(self):
        self.assertIsNotNone(validate_salary(-100))

    def test_float_salary(self):
        self.assertIsNotNone(validate_salary(50000.5))

    def test_bool_salary(self):
        # bool 是 int 的子類別，True==1 應視為無效
        self.assertIsNotNone(validate_salary(True))

    def test_string_salary(self):
        self.assertIsNotNone(validate_salary("50000"))


class TestValidateJoinDate(unittest.TestCase):
    def test_valid_date(self):
        self.assertIsNone(validate_join_date("2022-03-15"))

    def test_invalid_format(self):
        self.assertIsNotNone(validate_join_date("15-03-2022"))

    def test_invalid_date(self):
        self.assertIsNotNone(validate_join_date("2022-13-01"))

    def test_none_value(self):
        self.assertEqual(validate_join_date(None), "join_date is required")

    def test_slash_format(self):
        self.assertIsNotNone(validate_join_date("2022/03/15"))


class TestSubmitRow(unittest.TestCase):
    RECORD = {
        "employee_id": "E001",
        "name": "John Chan",
        "email": "john.chan@company.com",
        "department": "IT",
        "salary": 50000,
        "join_date": "2022-03-15",
    }

    @patch("main.requests.post")
    def test_success_201(self, mock_post):
        mock_post.return_value = MagicMock(status_code=201)
        self.assertTrue(submit_row(self.RECORD, 2))

    @patch("main.requests.post")
    def test_failure_422(self, mock_post):
        mock_post.return_value = MagicMock(status_code=422, text="Unprocessable Entity")
        self.assertFalse(submit_row(self.RECORD, 2))

    @patch("main.requests.post")
    def test_network_exception(self, mock_post):
        import requests
        mock_post.side_effect = requests.RequestException("connection refused")
        self.assertFalse(submit_row(self.RECORD, 2))

    @patch("main.requests.post")
    def test_timeout(self, mock_post):
        import requests
        mock_post.side_effect = requests.Timeout("timed out")
        self.assertFalse(submit_row(self.RECORD, 2))


if __name__ == "__main__":
    unittest.main()
