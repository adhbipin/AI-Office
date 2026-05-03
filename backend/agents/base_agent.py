import ollama
import json
import re
from datetime import datetime

class BaseAgent:
    def __init__(self, name, role, goal, backstory, model="llama3", tools=None):
        self.name = name
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.model = model
        self.tools = tools or {}
        self.system_prompt = f"""Role: {role}
Goal: {goal}
Backstory: {backstory}

CRITICAL: You MUST use the available tools to complete your task.
When you want to write a file, you MUST output the following exact format:
TOOL: file_writer(file_path='path/to/file.ext', content='file content here')

Available tools: {list(self.tools.keys())}
Always explain what you are doing, then use the tool, then summarize.
"""

    async def run(self, prompt, manager=None):
        if manager:
            await manager.broadcast({
                "from": self.name,
                "to": "All",
                "message": f"Thinking about: {prompt[:50]}...",
                "timestamp": datetime.utcnow().isoformat()
            })

        import asyncio
        response = await asyncio.to_thread(
            ollama.chat,
            model=self.model,
            messages=[
                {'role': 'system', 'content': self.system_prompt},
                {'role': 'user', 'content': prompt}
            ]
        )
        content = response['message']['content']
        print(f"DEBUG: {self.name} response raw: {content[:200]}...")

        # Handle tool calls (multiple matches allowed)
        # Use a more robust regex that handles multiline content
        tool_matches = re.finditer(r"TOOL: (\w+)\((.*?)\)", content, re.DOTALL)
        found_tools = False
        for match in tool_matches:
            found_tools = True
            tool_name = match.group(1)
            args_str = match.group(2).strip()
            print(f"DEBUG: Found tool call: {tool_name} with args: {args_str[:100]}...")
            
            try:
                # Basic parsing: split by comma, then by equals
                args = {}
                # Handle single quotes and double quotes for content
                # This simple split might fail if content has commas, so we use a more careful approach
                arg_pairs = re.findall(r"(\w+)\s*=\s*(['\"])(.*?)\2", args_str, re.DOTALL)
                for k, quote, v in arg_pairs:
                    args[k] = v
                
                if tool_name in self.tools:
                    tool_result = self.tools[tool_name](**args)
                    print(f"DEBUG: Tool {tool_name} result: {tool_result}")
                    content += f"\n\n🛠️ [System]: {tool_result}"
            except Exception as e:
                print(f"DEBUG: Tool {tool_name} execution failed: {e}")
                content += f"\n\n❌ [System Error]: {str(e)}"
        
        if not found_tools and "write" in prompt.lower():
             print(f"DEBUG: {self.name} was asked to write but no TOOL: call found.")

        if manager:
            await manager.broadcast({
                "from": self.name,
                "to": "All",
                "message": content,
                "timestamp": datetime.utcnow().isoformat()
            })
        
        return content
