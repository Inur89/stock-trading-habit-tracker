"""
test_habits.py
~~~~~~~~~~~~~~~
Tests for YOUR notebook's implementation (habit.py, storage.py, fixtures.py,
analytics.py, cli.py). Run with:  python -m pytest -v
"""

from datetime import datetime, timedelta

import analytics
from fixtures import create_fixtures
from habit import Habit
from storage import load, save


class TestHabitCreation:
    def test_create_daily_habit(self):
        habit = Habit("Check Portfolio", "desc", "daily")
        assert habit.name == "Check Portfolio"
        assert habit.periodicity == "daily"
        assert habit.completions == []

    def test_create_weekly_habit(self):
        habit = Habit("Research New Stock", "desc", "weekly")
        assert habit.periodicity == "weekly"

    def test_get_summary_contains_key_fields(self):
        habit = Habit("Check Portfolio", "Review positions", "daily")
        summary = habit.get_summary()
        assert "Check Portfolio" in summary
        assert "Review positions" in summary
        assert "DAILY" in summary


class TestCheckOff:
    def test_check_off_records_a_completion(self):
        habit = Habit("Check Portfolio", "desc", "daily")
        habit.check_off()
        assert len(habit.completions) == 1

    def test_multiple_check_offs_are_all_recorded(self):
        habit = Habit("Check Portfolio", "desc", "daily")
        habit.check_off()
        habit.check_off()
        assert len(habit.completions) == 2


class TestEditHabit:
    def test_edit_name_only(self):
        habit = Habit("Old Name", "desc", "daily")
        habit.edit(name="New Name")
        assert habit.name == "New Name"
        assert habit.periodicity == "daily"  # unchanged

    def test_edit_description_and_periodicity(self):
        habit = Habit("Habit", "old desc", "daily")
        habit.edit(description="new desc", periodicity="weekly")
        assert habit.description == "new desc"
        assert habit.periodicity == "weekly"

    def test_edit_with_no_arguments_leaves_everything_unchanged(self):
        habit = Habit("Habit", "desc", "daily")
        habit.edit()
        assert (habit.name, habit.description, habit.periodicity) == ("Habit", "desc", "daily")

    def test_edit_does_not_touch_completions(self):
        habit = Habit("Habit", "desc", "daily")
        habit.check_off()
        habit.edit(name="Renamed")
        assert len(habit.completions) == 1


class TestDailyStreak:
    def test_streak_is_zero_when_today_not_checked_off(self):
        habit = Habit("Check Portfolio", "desc", "daily")
        # Checked off yesterday, but NOT today -> current streak is 0
        habit.completions.append(datetime.now() - timedelta(days=1))
        assert habit.get_streak() == 0

    def test_streak_counts_consecutive_days_ending_today(self):
        habit = Habit("Check Portfolio", "desc", "daily")
        now = datetime.now()
        habit.completions = [now, now - timedelta(days=1), now - timedelta(days=2)]
        assert habit.get_streak() == 3

    def test_longest_streak_survives_a_later_break(self):
        habit = Habit("Check Portfolio", "desc", "daily")
        start = datetime(2024, 1, 1)
        for i in range(4):
            habit.completions.append(start + timedelta(days=i))
        habit.completions.append(start + timedelta(days=10))  # big gap
        assert habit.get_longest_streak() == 4


class TestWeeklyStreak:
    def test_streak_counts_this_week(self):
        habit = Habit("Research New Stock", "desc", "weekly")
        habit.completions.append(datetime.now())
        assert habit.get_streak() == 1

    def test_streak_counts_two_consecutive_weeks(self):
        habit = Habit("Research New Stock", "desc", "weekly")
        now = datetime.now()
        habit.completions = [now, now - timedelta(weeks=1)]
        assert habit.get_streak() == 2

    def test_longest_weekly_streak_over_history(self):
        habit = Habit("Research New Stock", "desc", "weekly")
        start = datetime(2024, 1, 1)  # a Monday
        for i in range(3):
            habit.completions.append(start + timedelta(weeks=i))
        assert habit.get_longest_streak() == 3


class TestIsBroken:
    def test_daily_not_broken_within_a_day(self):
        habit = Habit("Check Portfolio", "desc", "daily")
        habit.completions.append(datetime.now() - timedelta(hours=2))
        assert habit.is_broken() is False

    def test_daily_broken_after_a_full_day_gap(self):
        habit = Habit("Check Portfolio", "desc", "daily")
        habit.completions.append(datetime.now() - timedelta(days=1, hours=1))
        assert habit.is_broken() is True

    def test_weekly_not_broken_within_the_week(self):
        habit = Habit("Research New Stock", "desc", "weekly")
        habit.completions.append(datetime.now() - timedelta(days=3))
        assert habit.is_broken() is False

    def test_weekly_broken_after_a_full_week_gap(self):
        habit = Habit("Research New Stock", "desc", "weekly")
        habit.completions.append(datetime.now() - timedelta(days=7, hours=1))
        assert habit.is_broken() is True

    def test_new_habit_with_no_completions_is_not_broken(self):
        habit = Habit("Check Portfolio", "desc", "daily")
        assert habit.is_broken() is False


class TestStorage:
    def test_save_creates_a_file(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        import storage
        storage.DATA_FILE = "habits.json"
        save([Habit("A", "", "daily")])
        assert (tmp_path / "habits.json").exists()

    def test_save_then_load_round_trip(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        original = Habit("Check Portfolio", "desc", "daily")
        original.check_off()
        save([original])
        reloaded = load()
        assert len(reloaded) == 1
        assert reloaded[0].name == "Check Portfolio"
        assert len(reloaded[0].completions) == 1

    def test_load_with_no_file_returns_empty_list(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        assert load() == []


class TestFixtures:
    def test_create_fixtures_returns_five_habits(self):
        habits = create_fixtures()
        assert len(habits) == 5

    def test_fixtures_have_expected_names(self):
        names = [h.name for h in create_fixtures()]
        assert "Check Portfolio" in names
        assert "Review Risk Management Rules" in names


class TestAnalytics:
    def setup_method(self):
        self.habits = create_fixtures()

    def test_get_all_habits_returns_every_habit(self):
        assert len(analytics.get_all_habits(self.habits)) == 5

    def test_get_habits_by_period_daily(self):
        daily = analytics.get_habits_by_period(self.habits, "daily")
        assert len(daily) == 3

    def test_get_habits_by_period_weekly(self):
        weekly = analytics.get_habits_by_period(self.habits, "weekly")
        assert len(weekly) == 2

    def test_get_longest_streak_all_returns_a_habit(self):
        best = analytics.get_longest_streak_all(self.habits)
        assert best is not None

    def test_get_longest_streak_for_matches_habit_method(self):
        habit = self.habits[0]
        assert analytics.get_longest_streak_for(habit) == habit.get_longest_streak()

    def test_get_habit_names_returns_strings(self):
        names = analytics.get_habit_names(self.habits)
        assert all(isinstance(n, str) for n in names)


class TestDeleteHabit:
    def test_delete_removes_habit_from_list(self):
        habits = [Habit("A", "", "daily"), Habit("B", "", "weekly")]
        habits.pop(0)
        assert len(habits) == 1
        assert habits[0].name == "B"

    def test_delete_then_save_persists_removal(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        habits = [Habit("A", "", "daily"), Habit("B", "", "weekly")]
        save(habits)
        habits.pop(0)
        save(habits)
        reloaded = load()
        assert [h.name for h in reloaded] == ["B"]
