import re

def validate_email(email):
    """Validate email format using regex."""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email))

def validate_password(password):
    """
    Validate password strength:
    - At least 8 characters
    - Contains both uppercase and lowercase letters
    - Contains at least one digit
    """
    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'\d', password):
        return False
    return True
