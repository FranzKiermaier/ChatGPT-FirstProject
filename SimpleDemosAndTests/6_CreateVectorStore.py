from openai import OpenAI
from SetupEnvironment import *

SetEnvironemnt()
apiKey = GetAPIKey()
client = OpenAI(api_key=apiKey)

vector_store = client.vector_stores.create(name="Support")
print(vector_store)