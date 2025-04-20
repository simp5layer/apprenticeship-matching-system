import re  # Regular expressions module for pattern matching

# Check if an email is valid using a basic regex pattern
def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

# Check if a mobile number is valid (10-15 digits, optional +)
def is_valid_mobile(mobile):
    return re.match(r"^\+?\d{10,15}$", mobile) is not None

# Check if a GPA is a valid float between 0.0 and 5.0
def is_valid_gpa(gpa):
    try:
        gpa = float(gpa)
        return 0.0 <= gpa <= 5.0
    except (ValueError, TypeError):
        return False

# Check if a value is a positive float number
def is_positive_number(value):
    try:
        return float(value) > 0
    except (ValueError, TypeError):
        return False
      
