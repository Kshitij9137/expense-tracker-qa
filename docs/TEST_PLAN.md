# Test Plan - Expense Tracker

## 1. Purpose and scope
Show that the Expense Tracker is correct, robust and reliable. In scope: input validation, CRUD, filtering, analysis, budgets, CSV export, CLI behaviour, error handling, persistence and performance. Out of scope: GUI (none exists), multi-user concurrency, network features.

## 2. Test levels
| Level | Prefix | Question answered | File(s) | Count |
|---|---|---|---|---|
| Unit | UT | Does each function work in isolation? | `tests/test_models.py` | 13 |
| Integration | IT | Do layers share data correctly (CLI -> service -> SQLite)? | `tests/test_service.py`, `tests/test_cli.py` | 15 |
| System | ST | Does the whole program work as a separate process? | `tests/test_system.py` | 7 |
| User acceptance | UAT | Can a user complete real tasks? | `tests/test_uat.py` | 6 |
| Edge case / error | EC | Does it cope with unusual or hostile input? | `tests/test_edge_cases.py` | 17 |
| Regression | REG | Do fixed bugs stay fixed? | `tests/test_regression.py` | 7 |
| **Total** | | | | **65** |

## 3. Techniques used
- **Boundary value analysis**: 0.01 and 10,000,000,000.00 accepted; 0.004 and 10,000,000,000.01 rejected; category length 30 vs 31; leap day.
- **Equivalence partitioning**: valid / non-numeric / zero / negative / non-finite amounts.
- **Error guessing**: SQL injection text, `NaN`, `1e400`, unicode, 5,000-character descriptions, unwritable export path.
- **Exploratory testing**: running the program by hand with odd input; this found BUG-001 to BUG-008.
- **State and persistence testing**: data must survive separate process runs.

## 4. Tools
| Tool | Use |
|---|---|
| unittest | Test framework |
| coverage.py (`--branch`) | Statement and branch coverage |
| cProfile / time.perf_counter | Performance analysis |
| `tools/generate_test_report.py` | Produces `docs/TEST_RESULTS.md` |
| Python traceback + `python -m pdb` | Debugging failures |

## 5. How to run
```bash
export PYTHONPATH=src
python -m unittest discover -s tests -v                 # run all tests
coverage run --branch --source=src/expense_tracker -m unittest discover -s tests
coverage report -m                                      # coverage summary
python tools/generate_test_report.py                    # refresh docs/TEST_RESULTS.md
```

## 6. Entry and exit criteria
- Entry: code compiles and basic smoke test (`add`, `list`) works.
- Exit: 100% of tests pass, no open critical/high bugs, coverage of at least 90%.

## 7. Results summary
- 65 of 65 tests pass (see `docs/TEST_RESULTS.md`).
- Coverage: 98% (243 statements, 56 branches). The subprocess-based system tests are not included in coverage collection, so the entry point and CLI fallback branches remain uncovered.
- 8 bugs found and fixed (see `docs/BUG_LOG.md`); each has a regression test.
- Performance: 5,000 single inserts 0.12 s vs 0.016 s in one transaction (about 7x faster) - implemented as `add_many()`.
- Independent usability try-out: not conducted; no real participant tried the program, so no external user feedback is claimed.

## 8. Known issues and limitations
1. Multi-process concurrent writes were not tested.
2. Tested on Linux with Python 3.12 only; Windows and macOS not tested here.
3. Amounts support 2 decimal places only; extra digits are rounded.
4. Month filters use `LIKE 'YYYY-MM-%'`; a date-range query would be more index-friendly (see `docs/CODE_REVIEW.md`).
5. `list_expenses` and `total_by_category` contain duplicated date-filter code (technical debt).

## 9. Peer review
- **Attribution:** Draft peer/mentor review; not an independent external review
- **Date:** 2026-10-23

The review praised the exact integer-cent money handling, parameterised SQL, clear separation of layers, and broad test coverage. It identified an error-handling gap: database connection setup happened before the CLI error handler, so an invalid or unwritable `--db` path could produce a traceback. It also recommended consolidating duplicated date-filter logic and replacing month `LIKE` queries with date ranges to make better use of the date index.

**Response:** Database connection errors are now reported clearly, with a system regression test for an invalid database path (ST-07). The two query/maintainability suggestions remain open in `docs/CODE_REVIEW.md`.
