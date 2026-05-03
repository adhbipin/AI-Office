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
        self.system_prompt = f"Role: {role}\nGoal: {goal}\nBackstory: {backstory}\n\nYou can use tools by outputting: TOOL: tool_name(arg1='val1', ...)\nAvailable tools: {list(self.tools.keys())}"

    async def run(self, prompt, manager=None):
        if manager:
            await manager.broadcast({
                "from": self.name,
                "to": "All",
                "message": "Thinking...",
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

        # Handle tool calls (multiple matches allowed)
        tool_matches = re.finditer(r"TOOL: (\w+)\((.*?)\)", content, re.DOTALL)
        for match in tool_matches:
            tool_name = match.group(1)
            args_str = match.group(2).strip()
            
            # Sanitize args_str for eval
            try:
                # Basic parsing: split by comma, then by equals
                args = {}
                # This is a very simple parser for arg='val'
                for part in re.split(r",(?=(?:[^']*'[^']*')*[^']*$)", args_str):
                    if '=' in part:
                        k, v = part.split('=', 1)
                        args[k.strip()] = v.strip().strip("'").strip('"')
                
                if tool_name in self.tools:
                    tool_result = self.tools[tool_name](**args)
                    content += f"\n\n🛠️ [Tool Output ({tool_name})]: {tool_result}"
            except Exception as e:
                content += f"\n\n❌ [Tool Error ({tool_name})]: {str(e)}"

        if manager:
            await manager.broadcast({
                "from": self.name,
                "to": "All",
                "message": content,
                "timestamp": datetime.utcnow().isoformat()
            })
        
        return content
