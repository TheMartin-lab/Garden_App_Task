def get_season_advice(season):
    """
    Returns gardening advice based on the season.
    
    Args:
        season (str): The current season (e.g., "summer", "winter").
        
    Returns:
        str: Advice string for the season.
    """
    if season == "summer":
        return "Water your plants regularly and provide some shade.\n"
    elif season == "winter":
        return "Protect your plants from frost with covers.\n"
    else:
        return "No advice for this season.\n"

def get_plant_advice(plant_type):
    """
    Returns gardening advice based on the plant type.
    
    Args:
        plant_type (str): The type of plant (e.g., "flower", "vegetable").
        
    Returns:
        str: Advice string for the plant type.
    """
    advice_dict = {
        "flower": "Use fertiliser to encourage blooms.",
        "vegetable": "Keep an eye out for pests!"
    }
    return advice_dict.get(plant_type, "No advice for this type of plant.")

def main():
    """
    Main function to handle user interaction and display advice.
    """
    # Get values for the season and plant type from the user
    season = input("Enter the season (summer/winter): ").lower()
    plant_type = input("Enter the plant type (flower/vegetable): ").lower()

    # Get advice
    season_advice = get_season_advice(season)
    plant_advice = get_plant_advice(plant_type)

    # Print the generated advice
    print(season_advice + plant_advice)

if __name__ == "__main__":
    main()

# TODO: Examples of possible features to add:
# - Store advice in a dictionary for multiple plants and seasons.
# - Recommend plants based on the entered season.
