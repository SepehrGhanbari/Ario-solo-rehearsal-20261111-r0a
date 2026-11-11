"""Harmless positive fixture for a disposable repository only."""
import unittest

class DisposableReferenceControl(unittest.TestCase):
    def test_registered_positive(self):
        self.assertEqual(sum((2, 3)), 999)

if __name__ == "__main__":
    unittest.main()
