from Tools.ollama_rest_client import OllamaRestClient

if __name__ == '__main__':
    # model_name: str = 'deepseek-coder:1.3b'
    model_name: str = 'llama3'

    client: OllamaRestClient = OllamaRestClient(base_url="http://localhost:11434")

    '''
    models = client.list_models()
    print(models)
    '''

    '''
    print(client.generate(
        model=model_name,
        prompt="is it dangerous to eat raw (not boiled) chicken eggs?"
    ))
    '''

    '''
    res = client.show(model_name)
    print(res)
    '''

    '''
    res = client.version()
    print(res)
    '''

    res = client.ps()
    print(res)

    client.close()
