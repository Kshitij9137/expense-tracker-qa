# Expense Tracker

A command-line application for recording personal expenses, analysing spending by category, and tracking monthly budgets. Built as the Phase 3 practical implementation project of my internship.

## Features
- Add, list, update and delete expenses
- Filter by category and date range
- Totals per category and monthly totals
- Monthly budgets per category with over-budget warnings
- Export all expenses to CSV
- Input validation with clear error messages
- SQLite storage (no external dependencies)

## Requirements
Python 3.8 or newer. No third-party packages are needed.

## Quick start
```bash
git clone https://github.com/Kshitij9137/expense-tracker.git
cd expense-tracker
export PYTHONPATH=src          # Windows PowerShell: $env:PYTHONPATH="src"

python -m expense_tracker add 12.50 food -n "lunch"
python -m expense_tracker add 40 travel -d 2026-10-02 -n "bus pass"
python -m expense_tracker list
python -m expense_tracker summary
python -m expense_tracker budget food 20
python -m expense_tracker status --month 2026-10
python -m expense_tracker export my_expenses.csv
```

## Run the tests
```bash
python -m unittest discover -s tests -v
```
65 tests across six levels (unit, integration, system, user acceptance, edge case, regression) with 98% coverage. See `docs/TEST_PLAN.md`.

## Quality assurance
```bash
coverage run --branch --source=src/expense_tracker -m unittest discover -s tests
coverage report -m
python tools/generate_test_report.py   # refreshes docs/TEST_RESULTS.md
```

## Project structure
```
expense-tracker/
├── src/expense_tracker/
│   ├── cli.py        # presentation layer (argparse)
│   ├── service.py    # business logic
│   ├── database.py   # SQLite connection and schema
│   ├── models.py     # data model and validation
│   └── __main__.py   # entry point
├── tests/            # 64 tests: unit, integration, system, UAT, edge case, regression
├── tools/            # generate_test_report.py
├── docs/
│   ├── TEST_PLAN.md
│   ├── TEST_RESULTS.md
│   ├── BUG_LOG.md
│   ├── CODE_REVIEW.md
│   ├── ARCHITECTURE.md
│   └── USER_GUIDE.md
└── README.md
```

See `docs/ARCHITECTURE.md` for design decisions and `docs/USER_GUIDE.md` for all commands.

## Author
Kshitij Gupta
