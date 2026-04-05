import asyncio

import ollama
from ollama import chat, Client, AsyncClient
from ollama import ChatResponse

# model_name: str = "deepseek-r1:1.5b"
model_name: str = "llama3"


def simple_chat_test():
    response: ChatResponse = chat(
        model=model_name,
        messages=[{
            'role': 'user',
            'content': 'Why is the sky blue?',
        }],
        stream=False,
    )
    print(response['message']['content'])
    # or access fields directly from the response object
    print(response.message.content)


def custom_client_test():
    client = Client(
        host='http://localhost:11434',
        headers={'x-some-header': 'some-value'}
    )

    response: ChatResponse = client.chat(
        model=model_name,
        messages=[{
            'role': 'user',
            'content': 'Why is the sky blue?',
        }],
        stream=False,
    )
    print(response['message']['content'])
    # or access fields directly from the response object
    print(response.message.content)


def async_chat_test():
    async def chat_async():
        message = {'role': 'user', 'content': 'Why is the sky blue?'}
        response = await AsyncClient().chat(model=model_name, messages=[message])

    asyncio.run(chat_async())


# INFO: https://github.com/ollama/ollama-python
if __name__ == '__main__':
    # simple_chat_test()
    # custom_client_test()
    # async_chat_test()

    # print(ollama.list())
    # print(ollama.show(model_name))
    print(ollama.ps())
