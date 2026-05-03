from .base_agent import BaseAgent
from tools import file_writer, file_reader, directory_lister

def create_pm_agent():
    return BaseAgent(
        name='Project Manager',
        role='Project Manager',
        goal='Analyze tasks, delegate subtasks to specialists, and deliver reports.',
        backstory="""You are the Project Manager of an AI software agency. 
        When given a task, you must: (1) analyze it fully, (2) break it into clear subtasks 
        for each specialist agent, (3) assign each subtask, (4) track completion, and (5) deliver a final report. 
        Always be concise. Never do another agent's job.""",
        model='llama3:8b',
        tools={
            "file_writer": file_writer,
            "file_reader": file_reader,
            "directory_lister": directory_lister
        }
    )
