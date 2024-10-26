import json
import os
import openai

from dotenv import load_dotenv

# Load environment variables from .env file and access the api key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_data(gratitude_note):
    
    # Prompt to extract unsung heroes from the gratitude note
    prompt = (
        "You are an expert in identifying unsung heroes from gratitude notes. "
        "Given the following gratitude note, identify the groups of people with the groups in Santa Cruz and UC Santa Cruz(for example: Park Rangers, Environmental Conservationists, ...) that the author is grateful for, "
        "along with a reason for thanking, explaining description of their contributions (2-3 sentences). You can address similar groups together (group 1 and group 2):\n\n"
        f"Gratitude Note: {gratitude_note}\n\n"
        "Please format your response as a JSON object with the following structure:\n"
        "{\n"
        "  'recipient_groups': [\n"
        "    {\n"
        "      'group_name': '...',\n"
        "      'description': 'for ...'\n"
        "    },\n"
        "    ...\n"
        "  ]\n"
        "}"
    )

    client = openai.OpenAI()
        
    # Call the OpenAI API to generate the response
    response = client.chat.completions.create(
        model="gpt-3.5-turbo", 
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "Provide output in valid JSON"},
            {"role": "user", "content": prompt}],
    )
    
    # Extract the JSON response
    json_response = response.choices[0].message.content
    return json.loads(json_response)

if __name__ == "__main__":
    

    gratitude_note = (
    "To live in Santa Cruz is a blessing in and of itself, but the college campus is like the crown jewel of the city. "
    "Every time I drive up to campus for work, I almost have to pinch myself because it is hard to believe this is the place that I'm employed. "
    "I'm filled with gratitude for the wide open, rolling fields and beautiful redwoods surrounding the quaint buildings. "
    "It's the breathtaking view of the ocean and the gorgeous landscape that I'm grateful for mostly. "
    "Beyond that, there is plenty to be grateful about among my friendly and super helpful coworkers.")



    result = extract_data(gratitude_note)
    print(json.dumps(result, indent=2))