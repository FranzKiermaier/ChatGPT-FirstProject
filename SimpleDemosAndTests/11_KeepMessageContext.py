from openai import OpenAI
from SetupEnvironment import *

SetEnvironemnt()
apiKey = GetAPIKey()
client = OpenAI(api_key=apiKey)

responseId = ""
while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        break
    
    # Get model response with full context
    if responseId == "":
        response = client.responses.create(
            input=user_input, 
            model="gpt-4.1"
        )
    else:
        response = client.responses.create(
            input=user_input, 
            model="gpt-4.1", previous_response_id=responseId
        )
    responseId = response.id
    assistant_reply = response.output_text
    print(f"Assistant: {assistant_reply}")
