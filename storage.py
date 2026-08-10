import json
import os
from datetime import datetime

from habit import Habit

DATA_FILE = "habits.json"


def save(habits: list):
    """Save habits to JSON file."""
    data = []
    for habit in habits:
        habit_dict = {
            "name": habit.name,
            "description": habit.description,
            "periodicity": habit.periodicity,
            "created_date": habit.created_date.isoformat(),
            "completions": [c.isoformat() for c in habit.completions],
        }
        data.append(habit_dict)

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"\U0001F4BE Data saved to {DATA_FILE}")


def load():
    """Load habits from JSON file."""
    if not os.path.exists(DATA_FILE):
        print("\U0001F4C2 No data file found. Starting with empty habit list.")
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        habits = []
        for item in data:
            habit = Habit(
                name=item["name"],
                description=item["description"],
                periodicity=item["periodicity"],
            )
            habit.created_date = datetime.fromisoformat(item["created_date"])
            habit.completions = [
                datetime.fromisoformat(c) for c in item["completions"]
            ]
            habits.append(habit)

        print(f"\U0001F4C2 Loaded {len(habits)} habits from {DATA_FILE}")
        return habits

    except (json.JSONDecodeError, KeyError) as e:
        print(f"\u26a0\ufe0f  Error reading {DATA_FILE}: {e}")
        print("Starting with empty habit list.")
        return []
