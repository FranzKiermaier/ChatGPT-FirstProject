from openai import OpenAI

from SetupEnvironment import *
SetEnvironemnt()
apiKey = GetAPIKey()
client = OpenAI(api_key=apiKey)
response = client.responses.create(input="system: You speak like a pirate. user: tell me a poem with three verses about a hidden treasure full of gold, silver, gems and diamonds.",
                                   model="gpt-4.1")

print(response)