from openai import OpenAI
from SetupEnvironment import *

SetEnvironemnt()
apiKey = GetAPIKey()
client = OpenAI(api_key=apiKey)

allMyVector_stores = client.vector_stores.list()
print(allMyVector_stores)