### Support-Ticket-Triage-Agent

**Rooman AI Challenge - Junior AI Research Associate**

This project is an automated Support Ticket Triage Agent. It reads a batch of incoming support tickets, uses a Large Language Model (LLM) to analyze the text, and categorizes them by urgency, category, and department routing. It flags ambiguous tickets for human review.

### 1\. Setup Instructions

1.  **Clone the repository:**
    
    bash
    
        git clone https://github.com
        cd ticket_triage_agent
        
    
    Use code with caution.
    
2.  **Set up a Virtual Environment (Recommended):**
    
    bash
    
        python3 -m venv venv
        source venv/bin/activate
        
    
    Use code with caution.
    
3.  **Install dependencies:**
    
    bash
    
        pip install -r requirements.txt
        
    
    Use code with caution.
    
4.  **Configure API Key:**  
    Create a file named `.env` in the root directory. Add your Google Gemini API key like this:
    
    plaintext
    
        GEMINI_API_KEY=your_actual_api_key_here
        
    
    Use code with caution.
    
    *Note: The `.env` file is included in `.gitignore` to prevent secret leakage.*

### 2\. How to Run

1.  Ensure your sample tickets are located at `data/sample_tickets.json`. (A set of sample tickets is already provided).
2.  Run the agent from your terminal:
    
    bash
    
        python agent.py
        
    
    Use code with caution.
    
3.  The script will output its progress to the CLI.
4.  Check the `output/triaged_tickets.json` file to view the final, structured routing decisions.

### 3\. Agent Inputs and Outputs

*   **Input:** A JSON array of support tickets containing `id`, `subject`, and `body`.
*   **Output:** A JSON array combining the original ticket with a `triage_result` object containing: `category`, `urgency`, `confidence_score`, `routing`, and `reasoning`.

### 4\. Decision Boundaries & Logic

The system prompt strictly enforces the following decision boundaries:

*   **Critical Issues:** Any mention of system outages or revenue-blocking bugs is immediately flagged as `Critical` and routed to `Engineering`.
*   **Ambiguity Handling:** If a user submits a vague ticket (e.g., "the blue button is weird"), the agent is instructed to lower its `confidence_score` below 0.5, classify it as `Unclear`, and route it directly to `Human Review`.
*   **Standard Routing:** Billing issues go to Billing Support, password resets go to Customer Success, and feature requests go to the Product Team.

### 5\. Design Tradeoffs & Future Improvements

*   **Model Choice:** I opted for Google's `gemini-2.5-flash` model with `temperature=0.0`. This provides zero-cost developer API access, incredibly fast latency, and highly deterministic reasoning, which is essential for consistent data classification.
*   **JSON Enforcement:** I used the native Google GenAI configuration parameter `response_mime_type="application/json"`. This completely forces a strict, structurally predictable JSON return string directly from the LLM, bypassing the need for heavy external parsing frameworks.
*   **Limitations/Future Work:** Currently, the agent processes tickets synchronously (one by one in a loop). With more time, I would implement concurrent batching to process tickets at a higher scale. Additionally, I would transition this to run over an actual database (like SQLite) rather than flat JSON text files.


## 6. How I Verified the Output (Manual Testing)
I validated the core business logic of the triage system by evaluating the sample tickets:
* Verified that billing disputes are correctly categorized into `Billing` and routed to the `Billing Support` team.
* Confirmed that system-down alerts successfully escalate to `Critical` urgency.
* Verified that vague user inputs are safely caught, marked with a low confidence score, and routed to `Human Review`.
