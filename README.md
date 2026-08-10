# Stock Trading Habit Tracker

The app lets users define daily or weekly trading-related habits (e.g.
'Check Portfolio', for example), and then check them off, edit or delete them, and analyse their consistency. 
This includes information such as current streaks, longest streaks ever achieved, and which habits are currently broken.

## Features

- Create, **edit**, **delete**, and check off habits (daily or weekly periodicity)
- Automatic streak tracking, respecting each habit's periodicity
- A **functional-programming** analytics module (`analytics.py`) using
  `map()`, `filter()`, and `max()` — no manual loops, no mutation of inputs
- JSON-based persistence between sessions (`habits.json`)
- 5 predefined demo habits with 4 weeks (28 days) of hand-crafted example data
- 33 passing pytest unit tests covering habit creation, check-off, editing,
  deletion, streak logic, broken-habit detection, storage, fixtures, and
  every analytics function

## Requirements

- Python 3.7 or later (developed and tested on Python 3.13)
- [pytest](https://pytest.org) to run the test suite: `pip install pytest`

No other third-party libraries are required — only the standard library
(`json`, `os`, `datetime`) is used.

## Installation

```bash
git clone https://github.com/<your-username>/stock-trading-habit-tracker.git
cd stock-trading-habit-tracker
pip install pytest   # only needed to run the unit tests
```

## Running the app

```bash
python cli.py
```

You'll see an interactive menu:

```
==================================================
   📈  STOCK TRADING HABIT TRACKER
==================================================
  [1]  Show all my habits
  [2]  Add a new habit
  [3]  Check off a habit (mark as done)
  [4]  Delete a habit
  [5]  Edit a habit
  [6]  View analytics report
  [7]  Load example trading habits (demo data)
  [0]  Exit
==================================================
```

A good first run: choose **7** to load 5 predefined habits with 4 weeks of
realistic example data, then **6** to see the analytics report, or **1** to
list every habit with its current status.

Habits are stored in `habits.json` in the project folder and are
automatically reloaded the next time you start the app.

### Creating a habit
Choose **2**, then provide a name, description, and a periodicity of
`daily` or `weekly`.

### Editing a habit
Choose **5**, pick the habit by number, then type new values — or leave
any field blank to keep it unchanged.

### Deleting a habit
Choose **4**, pick the habit by number, then confirm by typing `yes`.

## Running the tests

```bash
python -m pytest -v
```

All 33 tests should pass. The suite is organised into: `TestHabitCreation`,
`TestCheckOff`, `TestEditHabit`, `TestDeleteHabit`, `TestDailyStreak`,
`TestWeeklyStreak`, `TestIsBroken`, `TestStorage`, `TestFixtures`, and
`TestAnalytics`.

## Architecture

`cli.py` is the only module that interacts with the user directly —
every other module is a plain function/class library it calls into.

| Module | Responsibility |
|---|---|
| `habit.py` | The `Habit` class: creation, `check_off()`, `edit()`, `is_broken()`, `get_streak()`, `get_longest_streak()`. |
| `storage.py` | Saves/loads a list of habits to/from `habits.json`, handling a missing or corrupted file gracefully. |
| `analytics.py` | Functional-programming analysis of a list of habits (`map`/`filter`/`max`, no mutation). |
| `fixtures.py` | Builds 5 predefined demo habits with 28 days of example data, each with a different completion pattern. |
| `cli.py` | The interactive command-line menu tying everything together. |
| `test_habits.py` | The pytest suite (33 tests). |

### Design notes

- **JSON over a database**: for a single-user CLI tool, Python's built-in
  `json` module needs no extra install, is human-readable for debugging,
  and is enough for this project's scope.
- **Streak logic**: daily streaks count backward from *today*; weekly
  streaks count backward from the current ISO week (Monday-based). A habit
  is "broken" once a full day (daily) or week (weekly) has passed without
  a check-off.
- **`edit()` design**: every field defaults to `None`, meaning "leave
  unchanged" — the same pattern used throughout the CLI's other prompts,
  so a user can update just one field without retyping everything.

## Project structure

```
.
├── cli.py            # Interactive command-line interface
├── habit.py           # Habit class (OOP core)
├── storage.py          # JSON persistence
├── analytics.py        # Functional-programming analytics
├── fixtures.py         # Predefined habits + 4-week example data
├── test_habits.py      # Pytest suite (33 tests)
├── Habit_Tracker.ipynb  # Same logic as a step-by-step Jupyter notebook
├── .gitignore
└── README.md
```

## Author

Aynur Rzayeva-Karabulut · Matriculation No. UPS10746239 · IU Internationale
Hochschule
