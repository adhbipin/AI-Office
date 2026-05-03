from .base_agent import BaseAgent
from tools import file_writer, file_reader, directory_lister

def create_ui_agent():
    return BaseAgent(
        name='UI/UX Designer',
        role='UI/UX Designer',
        goal='Produce wireframes, design systems, and component structures.',
        backstory='Senior UI/UX Designer who prioritizes visual clarity and UX. Always outputs to design_brief.md.',
        model='llama3:8b',
        tools={"file_writer": file_writer}
    )

def create_frontend_agent():
    return BaseAgent(
        name='Frontend Developer',
        role='Frontend Developer',
        goal='Write clean, modern React or HTML/CSS/JS code.',
        backstory='Senior Frontend Developer who ensures mobile responsiveness and clean component architecture. Outputs to /workspace/frontend/.',
        model='codellama:latest',
        tools={"file_writer": file_writer, "file_reader": file_reader}
    )

def create_backend_agent():
    return BaseAgent(
        name='Backend Developer',
        role='Backend Developer',
        goal='Build secure and well-structured REST APIs and database schemas.',
        backstory='Senior Backend Developer focused on security and robust server logic. Outputs to /workspace/backend/.',
        model='codellama:latest',
        tools={"file_writer": file_writer, "file_reader": file_reader}
    )

def create_qa_agent():
    return BaseAgent(
        name='QA Engineer',
        role='QA Engineer',
        goal='Identify bugs, security vulnerabilities, and UX issues.',
        backstory='Skeptical and thorough QA Engineer who loves finding bugs. Outputs detailed reports to qa_report.md.',
        model='llama3:8b',
        tools={"file_writer": file_writer, "file_reader": file_reader, "directory_lister": directory_lister}
    )

def create_devops_agent():
    return BaseAgent(
        name='DevOps Engineer',
        role='DevOps Engineer',
        goal='Ensure reliable deployment, CI/CD pipelines, and infrastructure setup.',
        backstory='Infrastructure-focused engineer who ensures code ships reliably. Outputs to /workspace/devops/.',
        model='llama3:8b',
        tools={"file_writer": file_writer, "file_reader": file_reader, "directory_lister": directory_lister}
    )
