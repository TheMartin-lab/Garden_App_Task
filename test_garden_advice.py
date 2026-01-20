import unittest
from garden_advice import get_advice, recommend_plants

class TestGardenAdvice(unittest.TestCase):
    
    def test_get_advice_valid(self):
        # Test valid inputs
        advice = get_advice("summer", "flower")
        self.assertIn("Water your plants regularly", advice)
        self.assertIn("Use fertiliser", advice)
        
        advice = get_advice("winter", "vegetable")
        self.assertIn("Protect your plants", advice)
        self.assertIn("Keep an eye out for pests", advice)

    def test_get_advice_invalid(self):
        # Test invalid inputs (should return default messages)
        advice = get_advice("invalid_season", "invalid_plant")
        self.assertIn("No specific advice for this season", advice)
        self.assertIn("No specific advice for this plant type", advice)

    def test_recommend_plants_valid(self):
        # Test valid seasons
        plants = recommend_plants("summer")
        self.assertIn("Sunflowers", plants)
        
        plants = recommend_plants("winter")
        self.assertIn("Kale", plants)

    def test_recommend_plants_invalid(self):
        # Test invalid season
        plants = recommend_plants("invalid_season")
        self.assertEqual(plants, "No specific recommendations for this season.")

if __name__ == '__main__':
    unittest.main()
