# tests/test_v2_swarm.py — Autonomous Multi-Agent Swarm Test Suite
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from fastapi.testclient import TestClient
from app.main import app
from app.agents.orchestrator import OrchestratorAgent
from app.agents.researcher import ResearcherAgent
from app.agents.coder import CoderAgent
from app.agents.critic import CriticAgent

client = TestClient(app)

class TestSwarmEngine(unittest.TestCase):

    def test_orchestrator_goal_decomposition(self):
        orch = OrchestratorAgent()
        plan = orch.decompose_goal("Build an AI microservice in Python")
        self.assertEqual(len(plan), 4)
        self.assertEqual(plan[0]["agent"], "Planner")
        self.assertEqual(plan[1]["agent"], "Researcher")
        self.assertEqual(plan[2]["agent"], "Coder")
        self.assertEqual(plan[3]["agent"], "Critic")

    def test_researcher_agent(self):
        res = ResearcherAgent()
        out = res.execute_research("FastAPI Security Best Practices")
        self.assertIn("synthesis", out)
        self.assertTrue(len(out["synthesis"]) > 0)

    def test_coder_agent(self):
        coder = CoderAgent()
        out = coder.generate_implementation("REST API", "Research findings")
        self.assertIn("code", out)
        self.assertIn("python", out["code"])

    def test_critic_agent(self):
        critic = CriticAgent()
        out = critic.audit_code("def example(): pass")
        self.assertIn("score", out)
        self.assertGreaterEqual(out["score"], 90)

    def test_swarm_tasks_history_endpoint(self):
        res = client.get("/api/swarm/tasks")
        self.assertEqual(res.status_code, 200)
        self.assertTrue(isinstance(res.json(), list))

if __name__ == "__main__":
    unittest.main()
