import os
import openai
import weaviate

openai_key = os.getenv('OPENAI_KEY')
weaviate_key = os.getenv('WEAVIATE_KEY')
weaviate_url = os.getenv('WEAVIATE_URL')
openai.api_key = os.getenv('OPENAI_KEY')

def answer(query: str) -> str:
    res = openai.Completion.create(
        engine = 'gpt-3.5-turbo',#'text-davinci-003',#'text-curie-001'
        prompt=query,
        temperature=0,
        max_tokens=400, 
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )
    return res['choices'][0]['text'].strip()

client = weaviate.Client(
    url=weaviate_url,
    auth_client_secret=weaviate.auth.AuthApiKey(api_key=weaviate_key),
    additional_headers={
        "X-OpenAI-Api-Key": openai_key
    }
)

def get_response(query):

    limit = 5000
    # get relevant contexts
    res = (
        client.query
        .get("Personalbok", ["content"])
        .with_near_text({"concepts": [query]})
        .with_limit(10)
        .do()
    )
    contexts = [i["content"] for i in res["data"]["Get"]["Personalbok"]][::-1]
    print(contexts)

    # build our prompt with the retrieved contexts included
    prompt_start = (
        "Svar på spørsmålet basert på konteksten under.\n\n"+
        "Kontekst:\n"
    )
    prompt_end = (
        f"\n\nSpørsmål: {query}\nSvar:"
    )
    # append contexts until hitting limit
    for i in range(1, len(contexts)):
        if len("\n\n---\n\n".join(contexts[:i])) >= limit:
            prompt = (
                prompt_start +
                "\n\n---\n\n".join(contexts[:i-1]) +
                prompt_end
            )
            break
        elif i == len(contexts)-1:
            prompt = (
                prompt_start +
                "\n\n---\n\n".join(contexts) +
                prompt_end
            )
    return answer(prompt)