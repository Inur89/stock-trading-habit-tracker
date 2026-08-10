from datetime import datetime, timedelta


class Habit:
    def __init__(self, name: str, description: str, periodicity: str):
        self.name = name
        self.description = description
        self.periodicity = periodicity
        self.created_date = datetime.now()
        self.completions = []

    def check_off(self):
        """Record a completion for right now."""
        now = datetime.now()
        self.completions.append(now)
        print(f"\u2713 Habit '{self.name}' checked off at {now.strftime('%Y-%m-%d %H:%M')}.")

    def edit(self, name=None, description=None, periodicity=None):
        """Update one or more fields. Leave an argument as None to keep it unchanged."""
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        if periodicity is not None:
            self.periodicity = periodicity

    def get_streak(self):
        """Current streak, counting back from today/this week."""
        if not self.completions:
            return 0
        sorted_dates = sorted(self.completions, reverse=True)
        if self.periodicity == "daily":
            return self._calculate_daily_streak(sorted_dates)
        else:
            return self._calculate_weekly_streak(sorted_dates)

    def _calculate_daily_streak(self, sorted_dates: list):
        today = datetime.now().date()
        streak = 0
        check_date = today
        completions_set = set(d.date() for d in sorted_dates)
        while check_date in completions_set:
            streak += 1
            check_date -= timedelta(days=1)
        return streak

    def _calculate_weekly_streak(self, sorted_dates: list):
        today = datetime.now().date()
        current_week_start = today - timedelta(days=today.weekday())
        completions_weeks = set(
            d.date() - timedelta(days=d.date().weekday()) for d in sorted_dates
        )
        streak = 0
        check_week = current_week_start
        while check_week in completions_weeks:
            streak += 1
            check_week -= timedelta(days=7)
        return streak

    def get_longest_streak(self):
        """Best streak the habit has ever had."""
        if not self.completions:
            return 0
        sorted_dates = sorted(self.completions)
        if self.periodicity == "daily":
            return self._longest_daily_streak(sorted_dates)
        else:
            return self._longest_weekly_streak(sorted_dates)

    def _longest_daily_streak(self, sorted_dates: list):
        completion_days = sorted(set(d.date() for d in sorted_dates))
        if not completion_days:
            return 0
        longest = 1
        current = 1
        for i in range(1, len(completion_days)):
            if (completion_days[i] - completion_days[i - 1]).days == 1:
                current += 1
                longest = max(longest, current)
            else:
                current = 1
        return longest

    def _longest_weekly_streak(self, sorted_dates: list):
        completion_weeks = sorted(set(
            d.date() - timedelta(days=d.date().weekday())
            for d in sorted_dates
        ))
        if not completion_weeks:
            return 0
        longest = 1
        current = 1
        for i in range(1, len(completion_weeks)):
            if (completion_weeks[i] - completion_weeks[i - 1]).days == 7:
                current += 1
                longest = max(longest, current)
            else:
                current = 1
        return longest

    def is_broken(self):
        """True if the habit has lapsed (missed a day/week)."""
        if not self.completions:
            return False
        last_completion = max(self.completions)
        today = datetime.now()
        if self.periodicity == "daily":
            return (today - last_completion).days >= 1
        else:
            return (today - last_completion).days >= 7

    def get_summary(self):
        streak = self.get_streak()
        total_completions = len(self.completions)
        status = "\U0001F534 BROKEN" if self.is_broken() else "\U0001F7E2 Active"
        return (
            f"[{self.periodicity.upper()}] {self.name}\n"
            f"  Description : {self.description}\n"
            f"  Status      : {status}\n"
            f"  Streak      : {streak} {self.periodicity} periods\n"
            f"  Total done  : {total_completions} times"
        )

    def __str__(self):
        return self.get_summary()
