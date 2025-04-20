import bcrypt  # Library for hashing and verifying passwords securely

# Hash a plain-text password using bcrypt
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

# Check if a plain-text password matches the hashed password
def check_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())
