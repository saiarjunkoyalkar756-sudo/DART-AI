# tests/test_api.py — Automated Pytest Integration & Security Test Suite
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestDartProductionAPI(unittest.TestCase):

    def test_health_check(self):
        res = client.get("/health")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["status"], "healthy")

    def test_get_models_list(self):
        res = client.get("/api/models")
        self.assertEqual(res.status_code, 200)
        models = res.json()
        self.assertTrue(len(models) > 10)
        self.assertTrue(any(m["id"] == "deepseek-v3" for m in models))
        self.assertTrue(any(m["id"] == "auto" for m in models))

    def test_provider_status_health(self):
        res = client.get("/api/status/providers")
        self.assertEqual(res.status_code, 200)
        providers = res.json()["providers"]
        self.assertTrue(len(providers) >= 6)
        self.assertTrue(all(p["status"] == "healthy" for p in providers))

    def test_analytics_summary(self):
        res = client.get("/api/analytics/summary")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("active_users", data)
        self.assertIn("total_messages", data)

    def test_user_memories_crud(self):
        # Fetch initial endpoint to obtain CSRF cookie
        init_res = client.get("/health")
        csrf_token = init_res.cookies.get("dart_csrf_token")
        headers = {"X-CSRF-Token": csrf_token} if csrf_token else {}

        # Create memory
        res = client.post("/api/memories", json={"memory_key": "lang", "memory_value": "Python 3.12"}, headers=headers)
        self.assertEqual(res.status_code, 200)
        mid = res.json()["id"]

        # Fetch memories
        res_get = client.get("/api/memories")
        self.assertEqual(res_get.status_code, 200)
        self.assertTrue(any(m["id"] == mid for m in res_get.json()))

        # Delete memory
        res_del = client.delete(f"/api/memories/{mid}", headers=headers)
        self.assertEqual(res_del.status_code, 200)

    def test_rbac_admin_protection(self):
        # Request without admin auth header should be rejected (401)
        res_unauth = client.get("/api/admin/metrics")
        self.assertEqual(res_unauth.status_code, 401)

        # Request with valid admin auth header should succeed (200)
        res_auth = client.get("/api/admin/metrics", headers={"Authorization": "Bearer admin-secret-key"})
        self.assertEqual(res_auth.status_code, 200)
        self.assertIn("database_engine", res_auth.json())

    def test_public_v1_developer_api(self):
        res = client.get("/v1/models")
        self.assertEqual(res.status_code, 200)
        self.assertIn("object", res.json())
        self.assertEqual(res.json()["object"], "list")

if __name__ == "__main__":
    unittest.main()
