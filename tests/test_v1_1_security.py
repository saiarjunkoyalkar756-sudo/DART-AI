# tests/test_v1_1_security.py — Automated Security & Authentication Test Suite
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from fastapi.testclient import TestClient
from app.main import app
from app.services.passwords import hash_password, verify_password, validate_password_strength

client = TestClient(app)

class Testv11SecurityUpgrade(unittest.TestCase):

    def test_password_strength_validator(self):
        # Weak password (short)
        valid, msg = validate_password_strength("Short1!")
        self.assertFalse(valid)
        
        # Weak password (missing special char)
        valid, msg = validate_password_strength("Password12345")
        self.assertFalse(valid)

        # Strong password
        valid, msg = validate_password_strength("SecurePass123!@#")
        self.assertTrue(valid)

    def test_password_hashing_and_verification(self):
        password = "MySecurePassword123!"
        hashed = hash_password(password)
        self.assertTrue(verify_password(password, hashed))
        self.assertFalse(verify_password("WrongPassword123!", hashed))

    def test_auth_signup_and_login_flow(self):
        test_email = "test.sec@dart.ai"
        test_password = "SecurePassword123!"
        
        # Signup
        signup_res = client.post("/api/auth/signup", json={
            "name": "Security Tester",
            "email": test_email,
            "password": test_password
        })
        self.assertIn(signup_res.status_code, [200, 400])

        # Login
        login_res = client.post("/api/auth/login", json={
            "email": test_email,
            "password": test_password
        })
        self.assertEqual(login_res.status_code, 200)
        self.assertIn("access_token", login_res.json())

    def test_security_headers_present(self):
        res = client.get("/health")
        headers = res.headers
        self.assertEqual(headers.get("x-frame-options"), "DENY")
        self.assertEqual(headers.get("x-content-type-options"), "nosniff")
        self.assertIn("Content-Security-Policy", headers)
        self.assertIn("Strict-Transport-Security", headers)

    def test_csrf_cookie_issued(self):
        res = client.get("/health")
        self.assertIn("dart_csrf_token", res.cookies)

    def test_audit_logs_endpoint(self):
        res = client.get("/api/security/audit-logs")
        self.assertEqual(res.status_code, 200)
        self.assertTrue(isinstance(res.json(), list))

    def test_api_keys_endpoint(self):
        res = client.get("/api/api-keys")
        self.assertEqual(res.status_code, 200)
        self.assertTrue(isinstance(res.json(), list))

if __name__ == "__main__":
    unittest.main()
