import unittest
from agent import process_ticket

class TestTicketTriage(unittest.TestCase):

    def setUp(self):
        # Create a mock ticket for testing the function structure
        self.mock_ticket = {
            "id": "TCK-TEST",
            "subject": "Test ticket regarding login failure",
            "body": "I cannot access my dashboard using my credentials."
        }

    def test_process_ticket_structure(self):
        """Verify that the triage output contains all expected classification fields."""
        result = process_ticket(self.mock_ticket)
        
        # Ensure the original ticket keys remain intact
        self.assertEqual(result["id"], "TCK-TEST")
        
        # Ensure the triage_result key exists
        self.assertIn("triage_result", result)
        triage = result["triage_result"]
        
        # Verify that all 5 critical fields required by your prompt are present
        expected_keys = ["category", "urgency", "confidence_score", "routing", "reasoning"]
        for key in expected_keys:
            with self.subTest(key=key):
                self.assertIn(key, triage)

if __name__ == "__main__":
    unittest.main()
