import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Gemini Client (automatically picks up os.getenv("GEMINI_API_KEY"))
client = genai.Client()

# Define file paths
INPUT_FILE = "data/sample_tickets.json"
OUTPUT_FILE = "output/triaged_tickets.json"

SYSTEM_PROMPT = """
You are an expert IT Support Triage Agent. Your job is to analyze incoming support tickets and output your decision in strict JSON format.

For each ticket, you must determine:
1. category: Choose from ["Technical Issue", "Billing", "Account Access", "Feature Request", "Unclear"]
2. urgency: Choose from ["Critical", "High", "Medium", "Low"]
3. confidence_score: A float between 0.0 and 1.0 indicating how confident you are in this classification.
4. routing: Choose the team to route to ["Engineering", "Billing Support", "Customer Success", "Product Team", "Human Review"]
5. reasoning: One short sentence explaining your decision.

DECISION BOUNDARY RULES:
- If the system is completely down or causing revenue loss, Urgency is 'Critical' and route to 'Engineering'.
- If the issue is vague or confusing, set Confidence Score below 0.5, category to 'Unclear', and route to 'Human Review'.
- Passwords/login issues go to 'Account Access' -> 'Customer Success'.

Respond ONLY with a valid JSON object matching this structure:
{
  "category": "...",
  "urgency": "...",
  "confidence_score": 0.0,
  "routing": "...",
  "reasoning": "..."
}
"""

def process_ticket(ticket):
    """Sends a single ticket to the Gemini LLM and returns the structured response."""
    print(f"Processing {ticket['id']}: {ticket['subject']}...")
    
    prompt = f"Subject: {ticket['subject']}\nBody: {ticket['body']}"
    
    try:
        # Construct parameters matching the new GenAI client configuration structure
        config = types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0.0, # 0.0 ensures deterministic, consistent output
            response_mime_type="application/json" # Forces strict JSON return string
        )
        
        # Call the lightweight, fast gemini-2.5-flash model
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=config
        )
        
        result_text = response.text
        result_json = json.loads(result_text)
        
        # Merge the original ticket data with the AI's triage decisions
        return {**ticket, "triage_result": result_json}
        
    except Exception as e:
        print(f"Error processing {ticket['id']}: {e}")
        return {**ticket, "triage_result": {"error": str(e)}}

def main():
    # 1. Load input data
    with open(INPUT_FILE, "r") as f:
        tickets = json.load(f)
        
    processed_tickets = []
    
    # 2. Process each ticket
    for ticket in tickets:
        triaged_ticket = process_ticket(ticket)
        processed_tickets.append(triaged_ticket)
        
    # 3. Save output data
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        json.dump(processed_tickets, f, indent=4)
        
    print(f"\nSuccess! {len(tickets)} tickets triaged. Results saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
