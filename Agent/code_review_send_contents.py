import os
import asyncio
import ollama
from ollama import chat, Client, AsyncClient
from ollama import ChatResponse
from typing import List

from Tools.ollama_rest_client import OllamaRestClient


def file_content(project_root: str, file_path: str) -> str:
    output: str = f'FILE: {file_path.replace(project_root, "")}\n<code>\n'
    with open(file_path, 'r') as file:
        output += file.read() + '\n<code>\n\n'
    return output


def enum_project_files(project_root: str, src_dir: str) -> str:
    start_path: str = os.path.join(project_root, src_dir)
    items: List[str] = os.listdir(start_path)
    buffer: str = ''
    for item in items:
        item_path: str = os.path.join(start_path, item)
        if os.path.isdir(item_path):
            if '__pycache__' in item_path:
                continue
            buffer += enum_project_files(project_root, os.path.join(src_dir, item))
        else:
            buffer += file_content(project_root, item_path)
            pass
    return buffer


if __name__ == '__main__':
    proj_root_dir: str = '/home/andtokm/DiskS/LLM/TestProject'
    src_path: str = 'src'
    model_name: str = "llama3"

    codebase: str = enum_project_files(project_root=proj_root_dir, src_dir=src_path)
    setup: str = '''
You are a senior software engineer performing a strict code review.

Focus on:
- correctness
- edge cases
- concurrency issues
- memory safety
- performance
- security

Rules:
- Do NOT rewrite code
- Do NOT guess missing context
- If something is unclear — say "uncertain"
- Be precise and critical

Language: Python
    '''

    client: OllamaRestClient = OllamaRestClient(base_url="http://localhost:11434")

    # res = client.generate(model=model_name, prompt=setup)
    # print(res)

    # res = client.generate(model=model_name, prompt='Review the following codebase:\n' + codebase)
    # print(res)

    res = client.generate(model=model_name, prompt='Create a UnitTests for codebase:\n' + codebase)
    print(res)

    client.close()
