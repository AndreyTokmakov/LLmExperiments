from langchain.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.utils import Output
from langchain_ollama import ChatOllama
from langchain_core.messages import ToolMessage


# 1. Наш калькулятор
@tool
def add(a: float, b: float) -> float:
    """Add two numbers"""
    print(f"Add two numbers {a} + {b}")
    return a + b


@tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers"""
    print(f"Multiply two numbers: {a} * {b}")
    return a * b


tools = [add, multiply]

# 2. LLM (Ollama)
llm = ChatOllama(model="qwen2.5",
                 temperature=0)

# 3. Prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a calculator. Use tools for math."),
    ("human", "{input}")
])

llm_with_tools = llm.bind_tools(tools)

if __name__ == '__main__':
    messages = "What is (3 + 5) * 2?"

    while True:
        response: Output = llm_with_tools.invoke(messages)
        if not response.tool_calls:
            print(response.content)
            break

        tool_messages = []
        for call in response.tool_calls:
            if call["name"] == "add":
                result = add.invoke(call["args"])
            elif call["name"] == "multiply":
                result = multiply.invoke(call["args"])

            tool_messages.append(ToolMessage(content=str(result), tool_call_id=call["id"]))

        messages = [response, *tool_messages]