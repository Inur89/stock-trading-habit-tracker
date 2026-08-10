from habit import Habit
from storage import save, load
from fixtures import create_fixtures
from analytics import get_habits_by_period, get_longest_streak_all, get_longest_streak_for, print_analytics_report


def show_menu():
    """Print the main menu to the screen."""
    print("\n" + "=" * 50)
    print("   \U0001F4C8  STOCK TRADING HABIT TRACKER")
    print("=" * 50)
    print("  [1]  Show all my habits")
    print("  [2]  Add a new habit")
    print("  [3]  Check off a habit (mark as done)")
    print("  [4]  Delete a habit")
    print("  [5]  Edit a habit")
    print("  [6]  View analytics report")
    print("  [7]  Load example trading habits (demo data)")
    print("  [0]  Exit")
    print("=" * 50)


def show_all_habits(habits: list):
    """Display all habits with their current status."""
    if not habits:
        print("\n\u26a0\ufe0f  You have no habits yet. Add one or load demo data.")
        return

    print(f"\n\U0001F4CB YOUR HABITS ({len(habits)} total):\n")
    for i, h in enumerate(habits, start=1):
        print(f"  {i}. {h}")
        print()


def add_habit(habits: list) -> list:
    print("\n\u2500\u2500 ADD NEW HABIT \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500")

    while True:
        name = input("  Habit name (e.g. 'Read Market News'): ").strip()
        if name:
            break
        print("  \u26a0\ufe0f  Name cannot be empty. Try again.")

    description = input("  Description: ").strip()
    if not description:
        description = "No description provided."

    while True:
        period = input("  Periodicity [daily / weekly]: ").strip().lower()
        if period in ("daily", "weekly"):
            break
        print("  \u26a0\ufe0f  Please type exactly 'daily' or 'weekly'.")

    new_habit = Habit(name=name, description=description, periodicity=period)
    habits.append(new_habit)
    save(habits)
    print(f"\n\u2705 Habit '{name}' added successfully!")
    return habits


def check_off_habit(habits: list) -> list:
    if not habits:
        print("\n\u26a0\ufe0f  No habits to check off. Add some first.")
        return habits

    print("\n\u2500\u2500 CHECK OFF HABIT \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500")
    for i, h in enumerate(habits, start=1):
        streak = h.get_streak()
        print(f"  [{i}] {h.name}  (current streak: {streak})")

    while True:
        try:
            choice = int(input("\n  Enter number (0 to cancel): "))
            if choice == 0:
                return habits
            if 1 <= choice <= len(habits):
                break
            print(f"  \u26a0\ufe0f  Please enter a number between 1 and {len(habits)}.")
        except ValueError:
            print("  \u26a0\ufe0f  Please enter a valid number.")

    selected = habits[choice - 1]
    selected.check_off()
    save(habits)
    print(f"  \U0001F525 New streak: {selected.get_streak()} {selected.periodicity} periods!")
    return habits


def delete_habit(habits: list) -> list:
    if not habits:
        print("\n\u26a0\ufe0f  No habits to delete.")
        return habits

    print("\n\u2500\u2500 DELETE HABIT \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500")
    for i, h in enumerate(habits, start=1):
        print(f"  [{i}] {h.name}")

    while True:
        try:
            choice = int(input("\n  Enter number to delete (0 to cancel): "))
            if choice == 0:
                return habits
            if 1 <= choice <= len(habits):
                break
            print(f"  \u26a0\ufe0f  Enter a number between 1 and {len(habits)}.")
        except ValueError:
            print("  \u26a0\ufe0f  Please enter a valid number.")

    selected = habits[choice - 1]

    confirm = input(f"\n  Delete '{selected.name}'? [yes / no]: ").strip().lower()
    if confirm == "yes":
        habits.pop(choice - 1)
        save(habits)
        print(f"  \U0001F5D1\ufe0f  '{selected.name}' deleted.")
    else:
        print("  \u274c Deletion cancelled.")

    return habits


def edit_habit(habits: list) -> list:
    if not habits:
        print("\n\u26a0\ufe0f  No habits to edit.")
        return habits

    print("\n\u2500\u2500 EDIT HABIT \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500")
    for i, h in enumerate(habits, start=1):
        print(f"  [{i}] {h.name}")

    while True:
        try:
            choice = int(input("\n  Enter number to edit (0 to cancel): "))
            if choice == 0:
                return habits
            if 1 <= choice <= len(habits):
                break
            print(f"  \u26a0\ufe0f  Enter a number between 1 and {len(habits)}.")
        except ValueError:
            print("  \u26a0\ufe0f  Please enter a valid number.")

    selected = habits[choice - 1]

    print("  Leave a field blank to keep its current value.")
    new_name = input(f"  New name [{selected.name}]: ").strip()
    new_description = input(f"  New description [{selected.description}]: ").strip()
    new_periodicity = input(f"  New periodicity (daily/weekly) [{selected.periodicity}]: ").strip().lower()

    if new_periodicity and new_periodicity not in ("daily", "weekly"):
        print("  \u26a0\ufe0f  Periodicity must be 'daily' or 'weekly'. No changes made.")
        return habits

    selected.edit(
        name=new_name or None,
        description=new_description or None,
        periodicity=new_periodicity or None,
    )
    save(habits)
    print(f"  \u2705 '{selected.name}' updated.")
    return habits


def view_analytics(habits: list):
    """Show the full analytics report."""
    print_analytics_report(habits)

    if not habits:
        return

    print("\n\u2500\u2500 DETAILED ANALYTICS \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500")
    print("  [1] Show only daily habits")
    print("  [2] Show only weekly habits")
    print("  [3] Show habit with longest streak")
    print("  [0] Back to main menu")

    choice = input("\n  Choose: ").strip()

    if choice == "1":
        daily = get_habits_by_period(habits, "daily")
        print(f"\n\U0001F4C5 DAILY HABITS ({len(daily)}):")
        for h in daily:
            print(f"   - {h.name}  (streak: {h.get_streak()})")

    elif choice == "2":
        weekly = get_habits_by_period(habits, "weekly")
        print(f"\n\U0001F4C5 WEEKLY HABITS ({len(weekly)}):")
        for h in weekly:
            print(f"   - {h.name}  (streak: {h.get_streak()})")

    elif choice == "3":
        best = get_longest_streak_all(habits)
        if best:
            streak = get_longest_streak_for(best)
            print(f"\n\U0001F3C6 Best habit: '{best.name}'")
            print(f"   Longest streak ever: {streak} {best.periodicity} periods")


def load_demo_data(habits: list) -> list:
    if habits:
        confirm = input(
            "\n  \u26a0\ufe0f  You already have habits. Replace all with demo data? [yes / no]: "
        ).strip().lower()
        if confirm != "yes":
            print("  \u274c Cancelled.")
            return habits

    habits = create_fixtures()
    save(habits)
    print("\u2705 Demo trading habits loaded and saved!")
    return habits


def main():
    """Main loop of the application."""
    print("\n\U0001F44B Welcome to the Stock Trading Habit Tracker!")

    habits = load()

    if not habits:
        answer = input("\n  No habits found. Load 5 demo trading habits? [yes / no]: ").strip().lower()
        if answer == "yes":
            habits = load_demo_data(habits)

    while True:
        show_menu()
        choice = input("  Your choice: ").strip()

        if choice == "1":
            show_all_habits(habits)
        elif choice == "2":
            habits = add_habit(habits)
        elif choice == "3":
            habits = check_off_habit(habits)
        elif choice == "4":
            habits = delete_habit(habits)
        elif choice == "5":
            habits = edit_habit(habits)
        elif choice == "6":
            view_analytics(habits)
        elif choice == "7":
            habits = load_demo_data(habits)
        elif choice == "0":
            print("\n\U0001F44B Goodbye! Keep tracking your trading habits!\n")
            break
        else:
            print("\n  \u26a0\ufe0f  Invalid choice. Please enter a number from the menu.")


if __name__ == "__main__":
    main()
