import unittest
class ChangedHead(unittest.TestCase):
    def test_deliberate_failure(self):
        self.assertEqual(2 + 3, 999)
