from tools import read_file, list_files
from llm_client import llm_with_tools
from langchain_core.messages import ToolMessage

# System prompt + instructions для LLM
SYSTEM_PROMPT = f"""
You are an AI code reviewer.
You have the following tools available:

1. list_files(path: str, recursive: bool = False) -> returns a list of file names
2. read_file(filename: str) -> returns the content of a file

Instructions:
- Always explore the project using these tools.
- Return JSON when calling a tool:
{{"tool_call": {{"name": "<tool_name>", "args": {{}}}}}}
- First get list of the project files
- Then read all files with their contents using this tool
- Do not give review comments until you have read files.
"""


def run_code_review(project_path: str):
    """
    Run a code review and output all files with their contents.
    """
    messages = SYSTEM_PROMPT + f"\nStart reviewing the project at: {project_path}"

    all_files = {}
    while True:
        response = llm_with_tools.invoke(messages)

        # Если нет tool_calls → LLM готова к текстовому ответу
        if not response.tool_calls:
            print("LLM final output:\n", response.content)
            break

        tool_messages = []

        for call in response.tool_calls:
            tool_name = call["name"]
            args = call["args"]

            if tool_name == "list_files":
                result = list_files.invoke(args)
                # Сохраняем все найденные файлы
                for f in result:
                    all_files[f] = None  # пока пустое содержимое
            elif tool_name == "read_file":
                filename = args["filename"]
                content = read_file.invoke(args)
                all_files[filename] = content
                result = f"Read file: {filename}"
            else:
                result = f"Unknown tool: {tool_name}"

            tool_messages.append(ToolMessage(
                    content=str(result),
                    tool_call_id=call["id"]
                )
            )

        messages = [response, *tool_messages]

    print('=' * 100)
    print(all_files)


if __name__ == "__main__":
    src: str = '/home/andtokm/DiskS/LLM/TestProject/src'
    run_code_review(src)
