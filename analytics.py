def get_all_habits(habits: list):
    return list(habits)


def get_habits_by_period(habits: list, period: str):
    return list(filter(lambda h: h.periodicity == period, habits))


def get_longest_streak_all(habits: list):
    """Return the habit with the longest all-time streak."""
    if not habits:
        return None
    return max(habits, key=lambda h: h.get_longest_streak())


def get_longest_streak_for(habit):
    """Return the longest streak for one specific habit."""
    return habit.get_longest_streak()


def get_broken_habits(habits: list):
    return list(filter(lambda h: h.is_broken(), habits))


def get_habit_names(habits: list):
    return list(map(lambda h: h.name, habits))


def print_analytics_report(habits: list):
    """Print a full summary report of all habits."""
    if not habits:
        print("No habits found.")
        return

    print("\n\U0001F4CA Habit Analytics Report")
    print(f"   Total habits: {len(habits)}")

    daily = get_habits_by_period(habits, "daily")
    weekly = get_habits_by_period(habits, "weekly")
    print(f"   Daily habits  : {len(daily)}")
    print(f"   Weekly habits : {len(weekly)}")

    broken = get_broken_habits(habits)
    if broken:
        print(f"\n\u26a0\ufe0f  Broken habits ({len(broken)}):")
        for h in broken:
            print(f"   - {h.name}")
    else:
        print("\n\u2705 No broken habits \u2014 great work!")

    best = get_longest_streak_all(habits)
    if best:
        print(f"\n\U0001F3C6 Longest streak overall: {best.name} ({best.get_longest_streak()} days)")
    else:
        print("\n\U0001F3C6 No habits to analyze for longest streak.")

    print("\n\U0001F4C8 Current streaks:")
    for h in habits:
        streak = h.get_streak()
        bar = "\u2588" * streak if streak > 0 else "\u2014"
        print(f"   {h.name:<35} {streak:>3} {bar}")

    print("\n" + "=" * 55)
