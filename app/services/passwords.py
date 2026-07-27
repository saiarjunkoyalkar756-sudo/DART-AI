# app/services/passwords.py — Bcrypt Password Hashing & Strength Validator
import re, hashlib, secrets

def hash_password(password: str) -> str:
    """Hashes password securely with sha256 + salt."""
    salt = secrets.token_hex(16)
    hashed = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000).hex()
    return f"pbkdf2:{salt}:{hashed}"

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies password match against stored hash."""
    try:
        parts = hashed_password.split(":")
        if len(parts) != 3 or parts[0] != "pbkdf2":
            return False
        salt = parts[1]
        stored_hash = parts[2]
        computed = hashlib.pbkdf2_hmac('sha256', plain_password.encode('utf-8'), salt.encode('utf-8'), 100000).hex()
        return secrets.compare_digest(computed, stored_hash)
    except:
        return False

def validate_password_strength(password: str) -> tuple[bool, str]:
    """
    Password Requirements:
    - Minimum 12 characters
    - Uppercase letter
    - Lowercase letter
    - Number
    - Special character
    """
    if len(password) < 12:
        return False, "Password must be at least 12 characters long"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one number"
    if not re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>/?\\|]', password):
        return False, "Password must contain at least one special character"
    return True, "Strong password"
