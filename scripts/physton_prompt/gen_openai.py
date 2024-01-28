from scripts.physton_prompt.get_lang import get_lang
from scripts.physton_prompt.get_translate_apis import unprotected_translate_api_config


def gen_openai(prompt, api_config):
    import openai
    from openai import AzureOpenAI
    from distutils.version import LooseVersion
    api_config = unprotected_translate_api_config('chatgpt_key', api_config)
    print(api_config)

    if LooseVersion(openai.__version__) < LooseVersion('1.0.0'):
        raise Exception('OpenAI version 1.0.0 or higher is required. Please upgrade your OpenAI package.')
    
    print(f'openai client version: {openai.__version__}')
    
    api_key = api_config.get('api_key')
    deployment_name = api_config.get('deployment_name')
    azure_endpoint = api_config.get('azure_endpoint')

    print(f'Azure endpoint: {azure_endpoint}, deployment_name: {deployment_name}, api_key: {api_key}')
    
    if api_key is None:
        raise Exception('Please provide an API key for OpenAI')

    if deployment_name is None:
        raise Exception('Please provide a deployment name for OpenAI')
    
    if azure_endpoint is None:
        raise Exception('Please provide an Azure endpoint for OpenAI')
    
    client = AzureOpenAI(
        api_key = api_key,  
        api_version = "2023-12-01-preview",
        azure_endpoint = azure_endpoint
    )

    print(f'prompt: {prompt}')

    completion = client.chat.completions.create(
        model=deployment_name,
        messages=prompt,
        temperature=0.7,
        max_tokens=800,
        stop=None,
        timeout=60
    )

    content = completion.choices[0].message.content
    return content

