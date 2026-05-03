from agents.pm_agent import create_pm_agent
from agents.specialist_agents import (
    create_ui_agent, create_frontend_agent, create_backend_agent,
    create_qa_agent, create_devops_agent
)
from message_bus import manager
from database import save_message
from datetime import datetime
import asyncio

async def broadcast_and_save(data):
    # Add timestamp if missing
    if "timestamp" not in data:
        data["timestamp"] = datetime.utcnow().isoformat()
    
    # Save to database
    save_message(data.get("from"), data.get("to"), data.get("message"), data["timestamp"])
    
    # Broadcast
    await manager.broadcast(data)

async def run_task(description: str, manager):
    print(f"DEBUG: Starting task with description: {description}")
    # Setup agents
    try:
        pm = create_pm_agent()
        ui = create_ui_agent()
        frontend = create_frontend_agent()
        backend = create_backend_agent()
        qa = create_qa_agent()
        devops = create_devops_agent()
        print("DEBUG: Agents created")
    except Exception as e:
        print(f"DEBUG: Error creating agents: {e}")
        return

    await broadcast_and_save({
        "from": "Project Manager",
        "to": "All",
        "message": f"🚀 Starting new project: {description}"
    })
    print("DEBUG: Broadcasted start message")

    # Step 1: PM analyzes
    try:
        print("DEBUG: PM running...")
        plan = await pm.run(f"Analyze this task and create a high-level plan: {description}", manager)
        print(f"DEBUG: PM plan: {plan[:100]}...")
    except Exception as e:
        print(f"DEBUG: Error in PM analysis: {e}")
        return
    
    # Step 2: UI/UX designs
    print("DEBUG: UI/UX running...")
    design = await ui.run(f"Based on this plan: {plan}, create a design brief and write it to design_brief.md using file_writer.", manager)
    print(f"DEBUG: UI/UX design: {design[:100]}...")
    
    # Step 3: Backend & Frontend development
    # Backend first usually for APIs
    print("DEBUG: Backend running...")
    be = await backend.run(f"Based on the design brief: {design}, write the backend code to the backend/ folder using file_writer.", manager)
    print(f"DEBUG: Backend code: {be[:100]}...")
    
    print("DEBUG: Frontend running...")
    fe = await frontend.run(f"Based on the design brief: {design} and backend plan: {be}, write the frontend code to the frontend/ folder using file_writer.", manager)
    print(f"DEBUG: Frontend code: {fe[:100]}...")
    
    # Step 4: QA review
    print("DEBUG: QA running...")
    review = await qa.run(f"Review the workspace and report any bugs or issues for the task: {description}. Write your report to qa_report.md.", manager)
    print(f"DEBUG: QA review: {review[:100]}...")
    
    # Step 5: DevOps
    print("DEBUG: DevOps running...")
    deploy = await devops.run(f"Prepare deployment files (Dockerfile, etc.) for this project: {description}. Write files to the devops/ folder.", manager)
    print(f"DEBUG: DevOps deploy: {deploy[:100]}...")
    
    # Final step: PM Summary
    await pm.run(f"The project is complete. Summarize everything that was built for the user.", manager)

    await broadcast_and_save({
        "from": "Project Manager",
        "to": "All",
        "message": "✅ All tasks completed. Files are ready in the workspace."
    })
