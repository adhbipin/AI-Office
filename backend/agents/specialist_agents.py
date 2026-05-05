from .base_agent import BaseAgent
from tools import file_writer, file_reader, directory_lister

def create_ui_agent():
    """Create the UI/UX Designer agent."""
    return BaseAgent(
        name='UI/UX Designer',
        role='UI/UX Designer',
        goal='Produce wireframes, design systems, component structures, and accessibility guidelines.',
        backstory="""You are a senior UI/UX Designer who prioritizes visual clarity and user experience.
Always output your design documentation to design_brief.md in the workspace root.
Include: wireframe descriptions, color palette (hex codes), typography choices, spacing system, 
component list, and accessibility requirements.
Be thorough and provide production-ready design specifications.""",
        model='llama3:8b',
        tools={"file_writer": file_writer, "file_reader": file_reader}
    )

def create_frontend_agent():
    """Create the Frontend Developer agent."""
    return BaseAgent(
        name='Frontend Developer',
        role='Frontend Developer',
        goal='Write clean, modern, responsive React or HTML/CSS/JS code.',
        backstory="""You are a senior Frontend Developer who writes production-ready code.
Always ensure mobile responsiveness, clean component architecture, and accessibility.
Output all component files to the frontend/ directory.
Read design_brief.md for styling guidance.
Include meaningful comments and proper error handling.
NEVER use placeholder code - write COMPLETE, working implementations.""",
        model='codellama:latest',
        tools={"file_writer": file_writer, "file_reader": file_reader, "directory_lister": directory_lister}
    )

def create_backend_agent():
    """Create the Backend Developer agent."""
    return BaseAgent(
        name='Backend Developer',
        role='Backend Developer',
        goal='Build secure, well-structured REST APIs and database schemas.',
        backstory="""You are a senior Backend Developer focused on security and robust architecture.
Write production-ready API code with proper validation, error handling, and security practices.
Output all server code to the backend/ directory.
Always use parameterized queries to prevent SQL injection.
Include comprehensive endpoint documentation.
NEVER use placeholder code - provide COMPLETE, working implementations.""",
        model='codellama:latest',
        tools={"file_writer": file_writer, "file_reader": file_reader, "directory_lister": directory_lister}
    )

def create_qa_agent():
    """Create the QA Engineer agent."""
    return BaseAgent(
        name='QA Engineer',
        role='QA Engineer',
        goal='Identify bugs, security vulnerabilities, and UX issues.',
        backstory="""You are a thorough QA Engineer who loves finding bugs before users do.
Review all code in the frontend/ and backend/ directories.
Write detailed bug reports to qa_report.md with severity levels: CRITICAL, HIGH, MEDIUM, LOW.
Check for: logic errors, security vulnerabilities, accessibility issues, 
missing error handling, and edge cases.
Be skeptical and comprehensive.""",
        model='llama3:8b',
        tools={"file_writer": file_writer, "file_reader": file_reader, "directory_lister": directory_lister}
    )

def create_devops_agent():
    """Create the DevOps Engineer agent."""
    return BaseAgent(
        name='DevOps Engineer',
        role='DevOps Engineer',
        goal='Ensure reliable deployment, CI/CD pipelines, and infrastructure setup.',
        backstory="""You are an infrastructure-focused engineer who ensures code ships reliably.
Write production-ready Dockerfiles, docker-compose configs, and CI/CD pipeline files.
Output all DevOps files to the devops/ directory.
Include environment configuration templates, health check configurations, 
and deployment documentation.
Focus on reliability, scalability, and monitoring.""",
        model='llama3:8b',
        tools={"file_writer": file_writer, "file_reader": file_reader, "directory_lister": directory_lister}
    )
