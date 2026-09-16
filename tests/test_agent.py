import unittest
from src.agent import decide

HISTORY = [{"message": "I was charged twice for Premium", "reply": "Please check your payment history."}]

class AgentTests(unittest.TestCase):
    def test_low_risk_billing_can_auto_handle(self):
        result = decide("Spotify charged me twice for Premium", HISTORY)
        self.assertEqual(result.intent, "billing")
        self.assertEqual(result.action, "auto_handle")

    def test_sensitive_message_is_escalated(self):
        result = decide("My card payment is failing", HISTORY)
        self.assertEqual(result.action, "escalate")

    def test_refund_is_escalated(self):
        result = decide("Please refund my Premium charge", HISTORY)
        self.assertEqual(result.intent, "refund")
        self.assertEqual(result.action, "escalate")

if __name__ == "__main__":
    unittest.main()
