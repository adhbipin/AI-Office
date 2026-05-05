from agents.pm_agent import create_pm_agent
from agents.specialist_agents import (
    create_ui_agent, create_frontend_agent, create_backend_agent,
    create_qa_agent, create_devops_agent
)
from message_bus import manager
from database import save_message
from datetime import datetime
import asyncio

async def broadcast_and_save(agent_from: str, agent_to: str, message: str, msg_type: str = "chat"):
    """Broadcast a message to all clients and save to database."""
    data = {
        "from": agent_from,
        "to": agent_to,
        "message": message,
        "type": msg_type,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    # Save to database
    save_message(agent_from, agent_to, message, data["timestamp"], msg_type)
    
    # Broadcast to all connected clients
    await manager.broadcast(data)

async def run_task(description: str, msg_manager):
    """Run a complete task through all agents."""
    print(f"\n{'='*60}")
    print(f"🚀 STARTING TASK: {description}")
    print(f"{'='*60}\n")

    # Initialize agents
    print("📍 Creating agents...")
    try:
        pm = create_pm_agent()
        ui = create_ui_agent()
        frontend = create_frontend_agent()
        backend = create_backend_agent()
        qa = create_qa_agent()
        devops = create_devops_agent()
        print("✅ All agents created\n")
    except Exception as e:
        print(f"❌ Failed to create agents: {e}")
        await broadcast_and_save("System", "Error", f"Failed to initialize agents: {e}", "error")
        return

    # Notify start
    await broadcast_and_save("Project Manager", "All", f"🚀 Starting new task: {description}")

    # Step 1: PM analyzes and plans
    print("📌 Step 1: PM analyzes task...")
    try:
        plan = await pm.run(
            f"""Analyze this task and create a comprehensive high-level plan:
            
TASK: {description}

Break it into clear subtasks for each team member (UI/UX Designer, Frontend Developer, 
Backend Developer, QA Engineer, DevOps Engineer). 
Write the complete project plan to plan.md in the workspace root.
Include specific deliverables for each team member.
Be detailed and thorough.""",
            msg_manager
        )
        print(f"✅ PM plan created\n")
    except Exception as e:
        print(f"❌ PM analysis failed: {e}")
        await broadcast_and_save("System", "Error", f"PM analysis failed: {e}", "error")
        return

    # Step 2: UI/UX Designer creates design
    print("📌 Step 2: UI/UX Designer creates design brief...")
    try:
        design = await ui.run(
            f"""Based on this project plan:

{plan}

Create a comprehensive design brief and write it to design_brief.md.
Include:
- ASCII wireframe of the main page/interface
- Complete color palette with hex codes
- Typography choices (font families, sizes, weights)
- Spacing and grid system
- Component list with descriptions
- Accessibility requirements (WCAG 2.1 AA minimum)
- Responsive breakpoints (mobile, tablet, desktop)

Be production-ready and thorough.""",
            msg_manager
        )
        print(f"✅ Design brief created\n")
    except Exception as e:
        print(f"❌ UI/UX design failed: {e}")
        await broadcast_and_save("System", "Error", f"UI/UX design failed: {e}", "error")
        return

    # Step 3: Backend Developer builds API
    print("📌 Step 3: Backend Developer writes server code...")
    try:
        be_code = await backend.run(
            f"""Based on the project plan:

{plan}

And the design brief:

{design}

Write complete, production-ready backend code.
Include:
- REST API endpoints with proper HTTP methods
- Database schema with all tables and relationships
- Input validation and error handling
- Security best practices (parameterized queries, authentication)
- Comprehensive API documentation
- Environment configuration template

Write all files to the backend/ directory.
IMPORTANT: Write COMPLETE, working code. No placeholders.""",
            msg_manager
        )
        print(f"✅ Backend code created\n")
    except Exception as e:
        print(f"❌ Backend development failed: {e}")
        await broadcast_and_save("System", "Error", f"Backend development failed: {e}", "error")
        return

    # Step 4: Frontend Developer writes UI code
    print("📌 Step 4: Frontend Developer writes client code...")
    try:
        fe_code = await frontend.run(
            f"""Based on the design brief:

{design}

And the backend API documentation:

{be_code}

Write complete, production-ready frontend code.
Include:
- All HTML components mentioned in the design
- Complete CSS styling following the design system
- JavaScript/React functionality for interactivity
- Responsive design for all breakpoints
- Accessibility features (alt text, ARIA labels, keyboard navigation)
- Error handling and loading states

Write all files to the frontend/ directory.
IMPORTANT: Write COMPLETE, working code. No placeholders.""",
            msg_manager
        )
        print(f"✅ Frontend code created\n")
    except Exception as e:
        print(f"❌ Frontend development failed: {e}")
        await broadcast_and_save("System", "Error", f"Frontend development failed: {e}", "error")
        return

    # Step 5: QA Engineer reviews code
    print("📌 Step 5: QA Engineer reviews all code...")
    try:
        qa_report = await qa.run(
            f"""Review all code in the workspace (frontend/ and backend/ directories).

Check for:
1. Logic errors and bugs
2. Security vulnerabilities (SQL injection, XSS, CSRF, etc.)
3. Accessibility issues (WCAG 2.1 compliance)
4. Missing error handling
5. Performance problems
6. Edge cases not covered
7. Code quality and best practices

Write a detailed report to qa_report.md with:
- Summary of findings
- Detailed bug list with severity (CRITICAL, HIGH, MEDIUM, LOW)
- Recommendations for fixes
- Overall assessment

Be thorough and professional.""",
            msg_manager
        )
        print(f"✅ QA review completed\n")
    except Exception as e:
        print(f"❌ QA review failed: {e}")
        await broadcast_and_save("System", "Error", f"QA review failed: {e}", "error")
        return

    # Step 6: DevOps Engineer prepares deployment
    print("📌 Step 6: DevOps Engineer prepares deployment...")
    try:
        devops_files = await devops.run(
            f"""Prepare production deployment configuration for this application.

Create:
1. Dockerfile for containerizing the application
2. docker-compose.yml for local development
3. GitHub Actions CI/CD pipeline configuration
4. Environment configuration template (.env.example)
5. Deployment checklist and instructions
6. Health check and monitoring configuration

Write all files to the devops/ directory.
Include:
- Security best practices
- Scalability considerations
- Monitoring and logging setup
- Database migration strategy

Be production-ready and thorough.""",
            msg_manager
        )
        print(f"✅ DevOps files created\n")
    except Exception as e:
        print(f"❌ DevOps preparation failed: {e}")
        await broadcast_and_save("System", "Error", f"DevOps preparation failed: {e}", "error")
        return

    # Final: PM delivers summary
    print("📌 Final: PM delivers summary...")
    try:
        summary = await pm.run(
            f"""All team members have completed their work. 
            
Provide a final comprehensive summary of what was built:
- Overview of the completed application
- Key features implemented
- Files created and their purposes
- Next steps for deployment
- Any important notes for the development team

Be concise but thorough.""",
            msg_manager
        )
        print(f"✅ Summary delivered\n")
    except Exception as e:
        print(f"❌ Summary failed: {e}")

    # Notify completion
    await broadcast_and_save(
        "Project Manager",
        "All",
        "✅ ALL TASKS COMPLETED. All deliverables are in the workspace. Project ready for review and deployment.",
        "complete"
    )

    print(f"\n{'='*60}")
    print(f"🎉 TASK COMPLETE!")
    print(f"{'='*60}\n")
