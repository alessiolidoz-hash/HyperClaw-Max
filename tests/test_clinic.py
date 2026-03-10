import unittest

from hyperclaw_max.context_intel.clinic import classify_text


class ClinicTests(unittest.TestCase):
    def test_clinic_classifies_memory_drift(self) -> None:
        payload = classify_text("memory sync failed (search): openai embeddings failed: 401 provider=openai")
        self.assertEqual(payload["category"], "gateway_memory_drift")


if __name__ == "__main__":
    unittest.main()
