from openai import OpenAI
from SetupEnvironment import *

SetEnvironemnt()
apiKey = GetAPIKey()
client = OpenAI(api_key=apiKey)
newVectorStoreFile = client.vector_stores.files.create(vector_store_id="vs_683205431df8819197744175de57c9f1", file_id="file-5wifrWPMVfvVAJZPyrFjFo")
vectorStoreFiles = client.vector_stores.files.list(vector_store_id="vs_683205431df8819197744175de57c9f1")
print(vectorStoreFiles)