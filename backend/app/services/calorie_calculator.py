def calculate_bmr(
    weight_lbs: float,
    height_cm: float,
    age: int,
    gender: str
) -> float:

    # Convert pounds to kilograms
    weight_kg = weight_lbs / 2.20462

    # Calculate the base BMR
    bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age)

    # Apply the gender-specific constant
    if gender == "male":
        bmr += 5
    elif gender == "female":
        bmr -= 161
    else:
        raise ValueError("Unsupported gender value for BMR calculation")

    return round(bmr, 2)

def calculate_tdee(bmr: float, activity_level: str) -> float: 

    activty_multipliers = {
        "sedentary": 1.2,
        "lightly_active": 1.375,
        "moderately_active": 1.55,
        "very_active": 1.725,
        "extra_active": 1.9
    }

    multiplier = activty_multipliers.get(activity_level)

    if multiplier is None:
        raise ValueError("Invalid activity level")

    tdee = bmr * multiplier

    return round(tdee, 2)

def calculate_calorie_target(tdee: float, goal: str) -> float:

    goal_targets = {
        "lose_weight": -300,
        "maintain_weight": 0,
        "gain_weight": 300
    }

    if tdee is None:
        raise ValueError("No tdee calculated")
    if goal is None:
        raise ValueError("Invalid goal")

    target_goal = goal_targets.get(goal)

    total_calorie_target = tdee + target_goal

    return round(total_calorie_target, 2)

def calculate_macros(calorie_target: float) -> dict:

    protein_calories = calorie_target * 0.30
    carbohydrate_calores = calorie_target * 0.40
    fat_calories = calorie_target * 0.30

    # Calulate the amount of grams per macro
    protein_grams = protein_calories / 4
    carbohydrate_grams = carbohydrate_calores / 4
    fat_grams = fat_calories / 9

    return {
        "protein_grams": round(protein_grams, 2),
        "carbohydrate_grams": round(carbohydrate_grams, 2),
        "fat_grams": round(fat_grams, 2)
    }