from openai import OpenAI
from SetupEnvironment import *

SetEnvironemnt()
apiKey = GetAPIKey()
client = OpenAI(api_key=apiKey)
result = client.responses.create(model="gpt-4.1", tool_choice="required", tools=[{
      "type": "file_search",
      "vector_store_ids": ["vs_683205431df8819197744175de57c9f1"]
    }], input=
    [
                                       {
                                           "role": "system",
                                            "content": "you get your knowledge only out of the files provided to you and only answer questions about cryptos Bitcoin and Ethereum. Any questions about other crypto currencies will not be answered by you."
                                       },
                                       {
                                            "role": "user",
                                            "content": """give a comparison of bitcoin, ethereum and ripple and tell me where you found the information with a reference."""
                                       }
                                   ]
    )
print(result.output_text)