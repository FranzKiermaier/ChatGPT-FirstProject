from openai import OpenAI
import json
from SetupEnvironment import *

SetEnvironemnt()
apiKey = GetAPIKey()
client = OpenAI(api_key=apiKey)

faq_json = {
    "Fragen": [
        {
            "ID": "1",
            "Frage": "Was ist die lieblingsbeschäftigung von Franz Kiermaier?",
            "Antwort": "Schlafen"
        },
        {
            "ID": "2",
            "Frage": "Wo hält sich Franz Kiermaier am liebsten auf?",
            "Antwort": "In Dubai"
        },
        {
            "ID": "3",
            "Frage": "Was ist das Lieblingsgericht von Franz Kiermaier?",
            "Antwort": "Schnitzel mit Pommes"
        }
    ]
}

faq_str = json.dumps(faq_json, indent=2, ensure_ascii=False)

system_prompt = f"""
Du bist ein Assistent, der nur auf Basis der folgenden JSON-Daten antwortet. Ignoriere alles, was nicht direkt aus diesen Daten hervorgeht. Verwende die exakten Antworten, ohne zusätzliche Informationen zu erfinden.

Hier ist dein Wissen im JSON-Format:

{faq_str}
"""

# Beispiel-Frage
user_prompt = "Was ist Franz Kiermaier's Leibspeise?"



response = client.responses.create(
    model="gpt-4.1",
    input=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ],
    temperature=0
)

print(response.output_text)
