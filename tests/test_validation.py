import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest  # Python's built-in testing framework
from utils.validation import is_valid_email, is_valid_mobile, is_valid_gpa, is_positive_number
from utils.encryption import hash_password, check_password

# Test cases for the validation utility functions
class TestValidation(unittest.TestCase):

    # Test email validation with valid and invalid examples
    def test_valid_email(self):
        self.assertTrue(is_valid_email("test@example.com"))
        self.assertFalse(is_valid_email("bademail.com"))

    # Test mobile number validation for correct and incorrect formats
    def test_valid_mobile(self):
        self.assertTrue(is_valid_mobile("+966501234567"))
        self.assertFalse(is_valid_mobile("12345"))

    # Test GPA validation for range and type correctness
    def test_valid_gpa(self):
        self.assertTrue(is_valid_gpa("4.0"))      # within range
        self.assertFalse(is_valid_gpa("5.5"))     # out of range
        self.assertFalse(is_valid_gpa("abc"))     # invalid input type

    # Test positive number check with valid and invalid inputs
    def test_positive_number(self):
        self.assertTrue(is_positive_number("100"))    # valid
        self.assertFalse(is_positive_number("-1"))    # negative
        self.assertFalse(is_positive_number("abc"))   # non-numeric

# Test cases for password hashing and verification
class TestEncryption(unittest.TestCase):

    # Test password hashing and correct/incorrect verification
    def test_password_hashing(self):
        pw = "MySecurePass123"
        hashed = hash_password(pw)  # Generate hash
        self.assertTrue(check_password(pw, hashed))         # Correct password
        self.assertFalse(check_password("WrongPass", hashed))  # Wrong password

# Run all test cases
if __name__ == '__main__':
    unittest.main()
