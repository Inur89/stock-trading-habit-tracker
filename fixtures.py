from datetime import datetime, timedelta

from habit import Habit


def create_fixtures():
    today = datetime.now()
    start = today - timedelta(days=28)

    # Habit 1: Read Market News (daily) - misses a handful of days
    habit1 = Habit(
        name="Read Market News",
        description="Read morning financial news before market opens",
        periodicity="daily",
    )
    habit1.created_date = start
    skip_days_habit1 = {5, 6, 13, 14, 19, 20, 21, 26, 27}
    for day_offset in range(28):
        if day_offset not in skip_days_habit1:
            completion_time = start + timedelta(days=day_offset, hours=8, minutes=15)
            habit1.completions.append(completion_time)

    # Habit 2: Check Portfolio (daily) - same missed days as habit 1
    habit2 = Habit(
        name="Check Portfolio",
        description="Review all open positions and their daily performance",
        periodicity="daily",
    )
    habit2.created_date = start
    skip_days_habit2 = {5, 6, 13, 14, 19, 20, 21, 26, 27}
    for day_offset in range(28):
        if day_offset not in skip_days_habit2:
            completion_time = start + timedelta(days=day_offset, hours=9, minutes=10)
            habit2.completions.append(completion_time)

    # Habit 3: Write Trading Journal (daily) - more gaps, broken streak
    habit3 = Habit(
        name="Write Trading Journal",
        description="Record every trade decision with its rationale and outcome",
        periodicity="daily",
    )
    habit3.created_date = start
    complete_days_habit3 = {0, 1, 2, 3, 4, 7, 8, 9, 10, 11, 12, 15, 16, 17, 18, 22, 23, 24, 25}
    for day_offset in range(28):
        if day_offset in complete_days_habit3:
            completion_time = start + timedelta(days=day_offset, hours=20, minutes=0)
            habit3.completions.append(completion_time)

    # Habit 4: Analyze Weekly Performance (weekly) - done 3 of 4 weeks
    habit4 = Habit(
        name="Analyze Weekly Performance",
        description="Full week review: P&L, what worked, and strategic adjustments",
        periodicity="weekly",
    )
    habit4.created_date = start
    weekly_completion_days_habit4 = {4, 11, 25}
    for day_offset in weekly_completion_days_habit4:
        completion_time = start + timedelta(days=day_offset, hours=18, minutes=30)
        habit4.completions.append(completion_time)

    # Habit 5: Review Risk Management Rules (weekly) - done every week
    habit5 = Habit(
        name="Review Risk Management Rules",
        description="Revisit position sizing and stop-loss rules to stay disciplined",
        periodicity="weekly",
    )
    habit5.created_date = start
    weekly_completion_days_habit5 = {3, 10, 17, 24}
    for day_offset in weekly_completion_days_habit5:
        completion_time = start + timedelta(days=day_offset, hours=17, minutes=0)
        habit5.completions.append(completion_time)

    return [habit1, habit2, habit3, habit4, habit5]
