import unittest
from agent import process_ticket

class TestTicketTriageLogic(unittest.TestCase):

    def setUp(self):
        self.critical_ticket = {
            "id": "TCK-CRIT",
            "subject": "SERVER IS DOWN EMERGENCY",
            "body": "The entire database portal threw a 500 error and our main payment pipeline is down. We are losing thousands of dollars right now."
        }
        self.vague_ticket = {
            "id": "TCK-VAGUE",
            "subject": "something is weird",
            "body": "The blue button on the portal looks slightly different today. I don't know why."
        }

    def test_critical_outage_triage(self):
        """Test that a critical billing/outage ticket returns required structure keys."""
        result = process_ticket(self.critical_ticket)
        self.assertIn("triage_result", result)
        self.assertIn("urgency", result["triage_result"])

    def test_vague_ticket_triage(self):
        """Test that an ambiguous ticket returns required structure keys."""
        result = process_ticket(self.vague_ticket)
        self.assertIn("triage_result", result)
        self.assertIn("routing", result["triage_result"])

if __name__ == "__main__":
    unittest.main()
