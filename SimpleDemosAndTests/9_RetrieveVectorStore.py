from openai import OpenAI
from SetupEnvironment import *

SetEnvironemnt()
apiKey = GetAPIKey()
client = OpenAI(api_key=apiKey)
myVectorStore = client.vector_stores.retrieve(vector_store_id="vs_683205431df8819197744175de57c9f1")
fileCounts = myVectorStore.file_counts

print(fileCounts)