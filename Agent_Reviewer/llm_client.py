from langchain_ollama import ChatOllama
from tools import list_files, read_file

# Инициализация LLM (Ollama)
llm = ChatOllama(model="qwen2.5", temperature=0)

# Биндим инструменты
tools = [list_files, read_file]
llm_with_tools = llm.bind_tools(tools)