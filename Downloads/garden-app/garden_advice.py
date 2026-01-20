"""
Garden Advice Program
This program provides gardening advice based on the season and plant type entered by the user.
It also recommends plants suitable for the current season.
"""

def get_advice(season, plant_type):
    """
    Generates gardening advice based on season and plant type.
    
    Args:
        season (str): The current season (e.g., 'summer', 'winter').
        plant_type (str): The type of plant (e.g., 'flower', 'vegetable').
        
    Returns:
        str: A string containing the advice.
    """
    
    # Dictionary storing advice for seasons
    seasonal_advice = {
        "summer": "Water your plants regularly and provide some shade.",
        "winter": "Protect your plants from frost with covers.",
        "spring": "Prune dead branches and add compost to the soil.",
        "autumn": "Clean up fallen leaves and plant bulbs for spring."
    }
    
    # Dictionary storing advice for plant types
    plant_advice = {
        "flower": "Use fertiliser to encourage blooms.",
        "vegetable": "Keep an eye out for pests!",
        "herb": "Harvest frequently to encourage growth.",
        "tree": "Ensure deep watering for strong root systems."
    }
    
    advice = []
    
    # Get seasonal advice
    advice.append(seasonal_advice.get(season.lower(), "No specific advice for this season."))
    
    # Get plant type advice
    advice.append(plant_advice.get(plant_type.lower(), "No specific advice for this plant type."))
    
    return "\n".join(advice)

def recommend_plants(season):
    """
    Recommends plants based on the season.
    
    Args:
        season (str): The current season.
        
    Returns:
        str: A recommendation string.
    """
    recommendations = {
        "summer": "Sunflowers, Zinnias, Tomatoes, Peppers",
        "winter": "Pansies, Kale, Spinach, Garlic",
        "spring": "Tulips, Daffodils, Lettuce, Peas",
        "autumn": "Chrysanthemums, Asters, Carrots, Broccoli"
    }
    
    return recommendations.get(season.lower(), "No specific recommendations for this season.")

def main():
    """
    Main function to run the program.
    """
    print("Welcome to the Garden Advice Program!")
    
    # User interaction: Get input for season and plant type
    valid_seasons = ["summer", "winter", "spring", "autumn"]
    valid_plants = ["flower", "vegetable", "herb", "tree"]

    season = ""
    while season not in valid_seasons:
        season = input(f"Enter the current season ({', '.join(valid_seasons)}): ").strip().lower()
        if season not in valid_seasons:
            print(f"Invalid season. Please choose from: {', '.join(valid_seasons)}")

    plant_type = ""
    while plant_type not in valid_plants:
        plant_type = input(f"Enter the plant type ({', '.join(valid_plants)}): ").strip().lower()
        if plant_type not in valid_plants:
            print(f"Invalid plant type. Please choose from: {', '.join(valid_plants)}")
    
    print("\n--- Gardening Advice ---")
    advice = get_advice(season, plant_type)
    print(advice)
    
    print("\n--- Plant Recommendations ---")
    recommendation = recommend_plants(season)
    print(f"Recommended plants for {season}: {recommendation}")

if __name__ == "__main__":
    main()
