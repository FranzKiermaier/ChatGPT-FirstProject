from openai import OpenAI

from SetupEnvironment import *
SetEnvironemnt()
apiKey = GetAPIKey()
client = OpenAI(api_key=apiKey)
response = client.responses.create(input="""system: You are specialized in english history. \
                                   For your response you only use this article about Henry VIII on Wikipedia: https://en.wikipedia.org/wiki/Henry_VIII. \
                                   user: how many times was henry viii married? what were the names of his wifes and why did he found the english church?""",
                                   model="gpt-4.1")

print(response.output_text)

response2 = client.responses.create(input="""system: You are specialized in english history. \
                                   For your response you only use this article about Henry VIII on Wikipedia: https://en.wikipedia.org/wiki/Henry_VIII. \
                                   user: What were the greatest achievements of Albert Einstein?""",
                                   model="gpt-4.1")

print(response2.output_text)