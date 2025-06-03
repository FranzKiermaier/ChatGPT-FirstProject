import asyncio
import pyodbc
import json
from agents import Agent, WebSearchTool, set_default_openai_key, function_tool
from agents.extensions.handoff_prompt import prompt_with_handoff_instructions
from agents import Runner, trace
from SetupEnvironment import *

# --- Agent: Search Agent ---
web_search_agent = Agent(
    name="WebSearchAgent",
    instructions=(
        """You are an Agent, specialized in finding travel information on commonly known and well reated online platforms. \
            You provide input to the web search tool, based on the users information regarding desired destination and travel dates. \
            In your answers to the user you focus on the users question. If you can not perform the users request, please tell so."""
    ),
    tools=[WebSearchTool()],
)


def query_sql_server(server: str, database: str, query: str) -> str:
    try:
        #build connection string and connect to the database
        connection_string = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={server};"
            f"DATABASE={database};"
            f"TRUSTED_CONNECTION=yes"
        )
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        # Execute query
        cursor.execute(query)

        # Extract column names
        columns = [column[0] for column in cursor.description]

        # Zeilen als Dicts formatieren
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))

        # Verbindung schließen
        cursor.close()
        conn.close()

        # JSON zurückgeben
        return json.dumps(results, default=str, indent=2)

    except Exception as e:
        return json.dumps({"error": str(e)})
    
@function_tool
def FlightSearchTool(departure_airport: str, destination_airport: str, departure_date: str, return_date: str) -> dict:
    queryOutbound = f"""SELECT * FROM FlightDetails WHERE ((Departure_AirportCode='{departure_airport}'
                and Destination_AirportCode='{destination_airport}') OR 
                (Departure_AirportName='{departure_airport}'
                and Destination_AirportName='{destination_airport}')) 
                and DepartureDate >= CONVERT(datetime,'{departure_date} 00:00:00', 20)
                and DepartureDate <= CONVERT(datetime,'{departure_date} 23:59:59', 20)
                """
    resultOutbound = query_sql_server("PC04\\SQLEXPRESS", "Flights", queryOutbound)

    queryReturn = f"""SELECT * FROM FlightDetails WHERE ((Departure_AirportCode='{destination_airport}'
                and Destination_AirportCode='{departure_airport}') OR 
                (Departure_AirportName='{destination_airport}'
                and Destination_AirportName='{departure_airport}')) 
                and DepartureDate >= CONVERT(datetime,'{return_date} 00:00:00', 20)
                and DepartureDate <= CONVERT(datetime,'{return_date} 23:59:59', 20)
                """
    resultReturn = query_sql_server("PC04\\SQLEXPRESS", "Flights", queryReturn)

    
    result = {
        "result":
        {
        "resultOutbound": json.loads(resultOutbound),
        "resultReturn": json.loads(resultReturn)
        }
    }
    # result = { "departure_airport": departure_airport,
    #     "destination_airport":  destination_airport,
    #     "departure_date": departure_date,
    #     "departure_time": "10:00",
    #     "return_date": return_date,
    #     "return_time": "15:30",
    #     "price_outbound_flight": 1200,
    #     "price_return_flight": 990,
    #     "price_roundtrip": 1190
    # }
    #print(result)
    return result

travel_search_agent = Agent(
    name="TravelSearchAgent",
    instructions=(
        """You are an Agent, specialized in finding as well as booking flights based on information provided by the user.
            The user must provide at least the departure airport, destination airport, departure date and return.
            You get information from the FlightSearchTool. To initiate the search, you use the three letter airport codes.
            If you miss any information, ask the user to enter the missing information details and the continue your search."""
    ),
    tools=[FlightSearchTool],
)

triage_agent = Agent(
    name="TravelAgent",
    instructions=prompt_with_handoff_instructions("""
You are the virtual assistant for trevel planning. Welcome the user and ask how you can help.
Based on the user's intent, route to:
- WebSearchAgent for user requests that are not related to search or booking of flights and accommodation
- TravelSearchAgent for user requests regarding flight and accommodation search, reservation or booking"""),
    handoffs=[web_search_agent, travel_search_agent]
)

async def test_queries():
    previous_response_id = ""
    while True:
        user_input = input("User: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        with trace("Travel Planning Assistant"):
            if(previous_response_id == ""):
                result = await Runner.run(triage_agent, user_input)
            else:
                result = await Runner.run(triage_agent, user_input, previous_response_id=previous_response_id)
            previous_response_id = result.last_response_id
            print(f"Agent: {result.final_output}")
            print("---")

SetEnvironemnt()
#result = FlightSearchTool(departure_airport="MUC", destination_airport="CTG", departure_date="2025-12-15", return_date="2026-01-06")
#print(result)
asyncio.run(test_queries())