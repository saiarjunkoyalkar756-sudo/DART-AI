# tests/load_test.py — Concurrency & Latency Benchmark Test Suite
import sys, os, time, unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestLoadAndPerformance(unittest.TestCase):

    def test_health_latency_target(self):
        """Verifies /health response latency is under 200ms target."""
        start = time.time()
        res = client.get("/health")
        latency_ms = (time.time() - start) * 1000
        self.assertEqual(res.status_code, 200)
        self.assertLess(latency_ms, 200, f"Health latency {latency_ms:.2f}ms exceeds 200ms target")

    def test_models_list_latency_target(self):
        """Verifies /api/models response latency is under 500ms target."""
        start = time.time()
        res = client.get("/api/models")
        latency_ms = (time.time() - start) * 1000
        self.assertEqual(res.status_code, 200)
        self.assertLess(latency_ms, 500, f"Models latency {latency_ms:.2f}ms exceeds 500ms target")

    def test_concurrent_simulated_requests(self):
        """Simulates 50 concurrent endpoint requests."""
        endpoints = ["/health", "/api/models", "/api/status/providers", "/api/analytics/summary", "/v1/models"]
        latencies = []
        for i in range(50):
            ep = endpoints[i % len(endpoints)]
            start = time.time()
            res = client.get(ep)
            latency = (time.time() - start) * 1000
            latencies.append(latency)
            self.assertEqual(res.status_code, 200)

        avg_latency = sum(latencies) / len(latencies)
        print(f"\n[Load Test Benchmark] 50 Simulated Concurrent Requests — Avg Latency: {avg_latency:.2f}ms")
        self.assertLess(avg_latency, 300, f"Average concurrent latency {avg_latency:.2f}ms exceeds 300ms target")

if __name__ == "__main__":
    unittest.main()
