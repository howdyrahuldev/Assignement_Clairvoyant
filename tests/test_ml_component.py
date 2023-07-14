import unittest
import pandas as pd
from app.ml_component import generate_model


class MLComponentTestCase(unittest.TestCase):
    def setUp(self):
        # Create a sample dataset for testing
        self.data = pd.DataFrame({
            'feature1': [1, 2, 3, 4, 5],
            'feature2': [0, 1, 0, 1, 0],
            'target': [0, 1, 0, 1, 0]
        })
        self.target_column = 'target'

    def test_generate_model(self):
        # Test the generate_model function

        # Generate the model
        model, accuracy = generate_model(self.data, self.target_column)

        # Assert the model is not None
        self.assertIsNotNone(model)

        # Assert the accuracy is within a valid range
        self.assertGreaterEqual(accuracy, 0.0)
        self.assertLessEqual(accuracy, 1.0)


if __name__ == '__main__':
    unittest.main()
