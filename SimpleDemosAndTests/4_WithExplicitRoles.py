from openai import OpenAI

from SetupEnvironment import *
SetEnvironemnt()
apiKey = GetAPIKey()
client = OpenAI(api_key=apiKey)
response = client.responses.create(input = 
                                   [
                                       {
                                           "role": "system",
                                            "content": "You are an equal to Stephen Hawking and have deep understanding of the universe and physics. You explain things about physics, that an average person with an IQ of 100 can understand it."
                                       },
                                       {
                                            "role": "user",
                                            "content": """According to physic laws, Is there any way to change the past?"""
                                       }
                                   ], model="gpt-4.1")

print(response.output_text)