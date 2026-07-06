# Support-Ticket-Triage-Agent
**Rooman AI Challenge - Junior AI Research Associate**

This project is an automated Support Ticket Triage Agent. It reads a batch of incoming support tickets, uses an LLM to analyze the text, and categorizes them by urgency, category, and department routing. It flags ambiguous tickets for human review.

## 1. Setup Instructions

1. **Clone the repository:**
   `git clone <your-repo-url>`
   `cd ticket_triage_agent`

2. **Install dependencies:**
   `pip install -r requirements.txt`

3. **Configure API Key:**
   Create a file named `.env` in the root directory. Add your OpenAI API key like this:
   `OPENAI_API_KEY=sk-your-secret-key`

## 2. How to Run

1. Ensure your sample tickets are located at `data/sample_tickets.json`. (A set of 5 sample tickets is already provided).
2. Run the agent from your terminal:
   `python agent.py`
3. The script will output its progress to the CLI. 
4. Check the `output/triaged_tickets.json` file to view the final, structured routing decisions.

## 3. Agent Inputs and Outputs

* **Input:** A JSON array of support tickets containing `id`, `subject`, and `body`.
* **Output:** A JSON array combining the original ticket with a `triage_result` object containing: `category`, `urgency`, `confidence_score`, `routing`, and `reasoning`.

## 4. Decision Boundaries & Logic

The system prompt strictly enforces the following decision boundaries:
* **Critical Issues:** Any mention of system outages or revenue-blocking bugs is immediately flagged as `Critical` and routed to `Engineering`.
* **Ambiguity Handling:** If a user submits a vague ticket (e.g., "the blue button is weird"), the agent is instructed to lower its `confidence_score` below 0.5, classify it as `Unclear`, and route it directly to `Human Review`. 
* **Standard Routing:** Billing issues go to Billing Support, password resets go to Customer Success, and feature requests go to the Product Team.

## 5. Design Tradeoffs & Future Improvements

* **Model Choice:** I opted for `gpt-3.5-turbo` with `temperature=0.0`. This provides the perfect balance of low latency, low cost, and highly deterministic reasoning, which is essential for consistent data classification. 
* **JSON Enforcement:** I used OpenAI's native `response_format={ "type": "json_object" }`. This bypasses the need for heavy frameworks like LangChain, keeping the codebase lightweight and less prone to dependency errors.
* **Limitations/Future Work:** Currently, the agent processes tickets synchronously (one by one in a loop). With more time, I would implement `asyncio` to process batches of tickets concurrently for higher throughput. Additionally, I would connect this to an actual mock database (like SQLite) rather than flat JSON files.
