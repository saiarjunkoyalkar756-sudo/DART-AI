# app/api/swarm.py — Agent Swarm API & SSE Streaming Router
import uuid, json, time, asyncio
from datetime import datetime, timezone
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional

from app.api.db import get_db
from app.agents.orchestrator import OrchestratorAgent
from app.agents.researcher import ResearcherAgent
from app.agents.coder import CoderAgent
from app.agents.critic import CriticAgent

router = APIRouter()

orchestrator = OrchestratorAgent()
researcher = ResearcherAgent()
coder = CoderAgent()
critic = CriticAgent()

class SwarmExecuteRequest(BaseModel):
    goal: str

@router.post("/swarm/execute")
async def execute_swarm_goal(req: SwarmExecuteRequest, request: Request):
    """
    Submits a high-level goal to the Autonomous Agent Swarm and returns
    a real-time SSE stream of Planner, Researcher, Coder, and Critic agent steps.
    """
    goal = req.goal.strip()
    if not goal:
        raise HTTPException(status_code=400, detail="Goal prompt cannot be empty")

    user = getattr(request.state, "user", None)
    uid = user["id"] if user else "dev_user"
    task_id = f"swarm_{uuid.uuid4().hex[:12]}"
    now = datetime.now(timezone.utc).isoformat()

    # Save task to DB
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO swarm_tasks (id, user_id, goal, status, created_at) VALUES (?, ?, ?, 'processing', ?)",
            (task_id, uid, goal, now)
        )
        conn.commit()

    async def event_generator():
        yield f"event: swarm_start\ndata: {json.dumps({'task_id': task_id, 'goal': goal})}\n\n"
        await asyncio.sleep(0.3)

        # 1. Orchestrator Step
        steps = orchestrator.decompose_goal(goal)
        yield f"event: agent_step\ndata: {json.dumps({'agent': 'Planner', 'step': 1, 'title': steps[0]['title'], 'thought': steps[0]['thought'], 'output': f'Plan created with {len(steps)} sub-tasks.'})}\n\n"
        await asyncio.sleep(0.4)

        # 2. Researcher Step
        res_output = researcher.execute_research(goal)
        yield f"event: agent_step\ndata: {json.dumps({'agent': 'Researcher', 'step': 2, 'title': steps[1]['title'], 'thought': steps[1]['thought'], 'output': res_output['synthesis']})}\n\n"
        await asyncio.sleep(0.4)

        # 3. Coder Step
        coder_output = coder.generate_implementation(goal, res_output['synthesis'])
        yield f"event: agent_step\ndata: {json.dumps({'agent': 'Coder', 'step': 3, 'title': steps[2]['title'], 'thought': steps[2]['thought'], 'output': coder_output['code']})}\n\n"
        await asyncio.sleep(0.4)

        # 4. Critic Step
        critic_output = critic.audit_code(coder_output['code'])
        yield f"event: agent_step\ndata: {json.dumps({'agent': 'Critic', 'step': 4, 'title': steps[3]['title'], 'thought': steps[3]['thought'], 'output': critic_output['audit_report']})}\n\n"
        await asyncio.sleep(0.3)

        # Complete Task
        final_artifact = f"# Agent Swarm Execution Artifact\n\n## Goal\n{goal}\n\n## Implementation\n{coder_output['code']}\n\n{critic_output['audit_report']}"
        
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE swarm_tasks SET status = 'completed', result = ?, completed_at = ? WHERE id = ?",
                (final_artifact, datetime.now(timezone.utc).isoformat(), task_id)
            )
            conn.commit()

        yield f"event: swarm_complete\ndata: {json.dumps({'task_id': task_id, 'status': 'completed', 'final_artifact': final_artifact})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

@router.get("/swarm/tasks")
def get_swarm_tasks(request: Request):
    user = getattr(request.state, "user", None)
    uid = user["id"] if user else "dev_user"
    with get_db() as conn:
        cursor = conn.cursor()
        rows = cursor.execute("SELECT id, goal, status, created_at, completed_at FROM swarm_tasks WHERE user_id = ? ORDER BY created_at DESC LIMIT 20", (uid,)).fetchall()
        if not rows:
            now = datetime.now(timezone.utc).isoformat()
            return [{
                "id": "swarm_demo_1",
                "goal": "Build an AI Agent Swarm System in Python",
                "status": "completed",
                "created_at": now,
                "completed_at": now
            }]
        return [{"id": r[0], "goal": r[1], "status": r[2], "created_at": r[3], "completed_at": r[4]} for r in rows]

@router.get("/swarm/tasks/{task_id}")
def get_swarm_task_details(task_id: str):
    with get_db() as conn:
        cursor = conn.cursor()
        row = cursor.execute("SELECT id, goal, status, result, created_at, completed_at FROM swarm_tasks WHERE id = ?", (task_id,)).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Swarm task not found")
        return {"id": row[0], "goal": row[1], "status": row[2], "result": row[3], "created_at": row[4], "completed_at": row[5]}
