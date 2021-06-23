import os
import requests
from datetime import datetime

GENDER = "male"
WEIGHT_KG = 88
HEIGHT_CM = 182
AGE = 24

# Nutritionixe api credentials

APP_ID = os.environ.get("APP_ID")
API_KEY = os.environ.get("API_KEY")

# Sheety api credentials

SHEETY_TOKEN = os.environ.get("SHEETY_TOKEN")
SHEETY_USERNAME = os.environ.get("SHEETY_USERNAME")


exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
exercise_text = input("Tell me which exercises you did: ")

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

parameters = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

exercise_response = requests.post(url=exercise_endpoint, json=parameters, headers=headers)
exercise_response.raise_for_status()

exercise_result = exercise_response.json()

exercise = exercise_result["exercises"][0]["name"]
duration = exercise_result["exercises"][0]["duration_min"]
calories = exercise_result["exercises"][0]["nf_calories"]

today = datetime.now()
date = today.strftime("%d/%m/%Y")
time = today.strftime("%H:%M:%S")

sheety_endpoint = f"https://api.sheety.co/{SHEETY_USERNAME}/myWorkouts/workouts"

headers = {
    "Authorization": f"Bearer {SHEETY_TOKEN}"
}

body = {
    "workout": {
        "date": date,
        "time": time,
        "exercise": exercise.title(),
        "duration": duration,
        "calories": calories
    }
}

sheety_response = requests.post(url=sheety_endpoint, json=body, headers=headers)
sheety_response.raise_for_status()

sheety_result = sheety_response.json()
