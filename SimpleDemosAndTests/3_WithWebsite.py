from openai import OpenAI

from SetupEnvironment import *
SetEnvironemnt()
apiKey = GetAPIKey()
client = OpenAI(api_key=apiKey)
response = client.responses.create(input="""system: You are a wikipedia afficinado. \
                                   For your response your only source of knowledge is https://en.wikipedia.org. \
                                   user: Please name me all the kings and queens who are related to the house of york. \
                                   Provide the names and years of reign and format the list as a HTML table. \
                                   In a second step, provide the list of english kungs and queens sorted by their house and \\
                                   year of reign in one JSON formatted reply. \\
                                   In a third step, provide the headlines of all publications of Albert Einstein and sort it by year of release. \
                                   For each section add the list of html links as a reference.""",
                                   model="gpt-4.1")

print(response.output_text)