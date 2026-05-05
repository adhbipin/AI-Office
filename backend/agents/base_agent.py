import ollama
import json
import re
import asyncio
from datetime import datetime

class BaseAgent:
    def __init__(self, name: str, role: str, goal: str, backstory: str, model: str = "llama3:8b", tools: dict = None):
        self.name = name
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.model = model
        self.tools = tools or {}
        
        self.system_prompt = f"""Role: {role}
Goal: {goal}
Backstory: {backstory}

CRITICAL INSTRUCTIONS:
1. Always explain your thinking step-by-step.
2. When you need to write files, use this EXACT format:
   TOOL: file_writer(file_path='folder/filename.ext', content='your content here')
3. To read files, use: TOOL: file_reader(file_path='path/to/file')
4. To list directories, use: TOOL: directory_lister(dir_path='folder')
5. Always use forward slashes in paths, never backslashes.
6. Provide COMPLETE, PRODUCTION-READY code. No placeholders.

Available tools: {', '.join(self.tools.keys())}
"""

    async def run(self, prompt: str, manager=None) -> str:
        """Run the agent with the given prompt."""
        try:
            # Notify manager that agent is thinking
            if manager:
                await manager.broadcast({
                    "from": self.name,
                    "to": None,
                    "message": f"🤔 Analyzing: {prompt[:80]}...",
                    "type": "thinking",
                    "timestamp": datetime.utcnow().isoformat()
                })

            # Call Ollama synchronously in a thread to avoid blocking
            response = await asyncio.to_thread(
                self._call_ollama,
                prompt
            )

            # Process the response and execute any tools
            final_response = await self._process_response(response)

            # Broadcast final response
            if manager:
                await manager.broadcast({
                    "from": self.name,
                    "to": None,
                    "message": final_response,
                    "type": "response",
                    "timestamp": datetime.utcnow().isoformat()
                })

            return final_response

        except Exception as e:
            error_msg = f"❌ Error: {str(e)}"
            print(f"DEBUG {self.name}: {error_msg}")
            if manager:
                await manager.broadcast({
                    "from": self.name,
                    "to": None,
                    "message": error_msg,
                    "type": "error",
                    "timestamp": datetime.utcnow().isoformat()
                })
            return error_msg

    def _call_ollama(self, prompt: str) -> str:
        """Call Ollama synchronously."""
        try:
            response = ollama.chat(
                model=self.model,
                messages=[
                    {'role': 'system', 'content': self.system_prompt},
                    {'role': 'user', 'content': prompt}
                ]
            )
            return response['message']['content']
        except Exception as e:
            print(f"DEBUG: Ollama call failed for {self.name}: {e}")
            raise

    async def _process_response(self, content: str) -> str:
        """Parse and execute any tool calls in the response."""
        result = content
        executed_tools = []

        # Find all TOOL: calls using regex
        # Pattern: TOOL: function_name(key='value', key='value')
        tool_pattern = r"TOOL:\s*(\w+)\((.*?)\)"
        
        for match in re.finditer(tool_pattern, content, re.DOTALL):
            tool_name = match.group(1)
            args_str = match.group(2)

            if tool_name not in self.tools:
                result += f"\n\n⚠️  Tool '{tool_name}' not available."
                continue

            # Parse arguments: key='value' or key="value"
            args = {}
            try:
                arg_pattern = r"(\w+)\s*=\s*['\"](.+?)['\"]"
                for arg_match in re.finditer(arg_pattern, args_str, re.DOTALL):
                    args[arg_match.group(1)] = arg_match.group(2)

                if args:
                    print(f"DEBUG {self.name}: Executing {tool_name} with args: {list(args.keys())}")
                    tool_result = self.tools[tool_name](**args)
                    result += f"\n\n{tool_result}"
                    executed_tools.append(tool_name)
            except Exception as e:
                result += f"\n\n❌ Error executing {tool_name}: {str(e)}"

        if executed_tools:
            print(f"DEBUG {self.name}: Successfully executed tools: {executed_tools}")

        return result
