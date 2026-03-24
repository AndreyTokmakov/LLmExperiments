import json
import time
from typing import Dict, Optional, List

import requests
from requests import Response

from file_manager import FileManager

OLLAMA_URL: str = 'http://localhost:11434/api/generate'
MODEL: str = 'deepseek-coder:1.3b'

project_dir: str = '../../TestProject'

model_tools_setup: str = '''
You are an AI coding agent.

You have access to tools:

read_file(path: str)
list_files(path: str, recursive: bool = false)

When you need to use a tool, respond ONLY in JSON:

{
  "action": "tool_name",
  "arguments": {
    "param1": "value"
  }
}

Examples:

To get list of files
{
  "action": "list_files",
  "arguments": {
    "path": "src/",
    "recursive": false
  }
}

to read file
{
  "action": "read_file",
  "arguments": {
    "path": "src/main.rs"
  }
}

Important:
- Always use valid JSON
- Do not include comments
- Do not include trailing commas

OK ???

'''


def tests():
    '''
    data, err = FileManager.read_file("../../TestProject/main.py")
    if err:
        print("Error:", err)
    else:
        print(data)
    '''

    '''
    ok, err = FileManager.write_file("../../TestProject/main.py", "Hello")
    if not ok:
        print("Error:", err)
    '''

    files, err = FileManager.list_files(project_dir + "/src", recursive=True)
    if err:
        print("Error:", err)
    else:
        print(files)


def prompt(request: str) -> str:
    payload = {
        "model": MODEL,
        "prompt": request,
        "stream": False
    }

    print('-' * 120, '\n', payload, '\n', '-' * 120)

    response: Response = requests.post(OLLAMA_URL, json=payload)
    response.raise_for_status()

    data: Dict = response.json()

    print('*' * 120, '\n', data, '\n', '*' * 120)
    return data["response"]


def handle_response(response: str):
    try:
        model_response = json.loads(response)
        action: str = model_response["action"]
        arguments: Dict = model_response["arguments"]

        if action == "read_file":
            data = read_file(arguments)
            return data
        elif action == "list_files":
            data = list_files(arguments)
            return data

    except json.decoder.JSONDecodeError as exc:
        print(exc)
        return None


def read_file(args: Dict):
    try:
        path: str = args["path"]
        content, err = FileManager.read_file(project_dir + '/' + path)
        if err:
            print("Error:", err)
            return None
        else:
            return content
    except Exception as exc:
        print(exc)
        return None


def list_files(args: Dict):
    try:
        path: str = args["path"]
        files, err = FileManager.list_files(project_dir + "/src", recursive=True)
        if err:
            print("Error:", err)
            return None
        else:
            return files
    except Exception as exc:
        print(exc)
        return None


if __name__ == '__main__':
    '''
    response = prompt(model_tools_setup)
    response = prompt('review code in the /src directory')
    response = prompt('Language: Python, director: src')

    while True:
        out = handle_response(response)
        response = prompt(out)
        time.sleep(1)
    '''

    setup = '''
    You are a senior software engineer performing a code review.

You have access to tools:

1. list_files(path: str, recursive: bool = False)
   - returns list of files

2. read_file(path: str)
   - returns file content

Rules:

- ALWAYS explore the repository before answering
- Use list_files to understand project structure
- Use read_file to inspect relevant files
- NEVER assume file contents without reading them
- You can call tools multiple times

Tool usage format:

When you want to call a tool, respond ONLY with JSON:

{
  "tool": "tool_name",
  "arguments": { ... }
}

Do NOT add any text outside JSON when calling a tool.

When you have enough information, provide final answer in plain text.

Focus on:
- bugs
- performance issues
- readability
- architecture
- security
    '''


    start ='''its in /src folder '''

    # response = prompt(setup)
    # print(response)

    response = prompt(start)
    print(response)