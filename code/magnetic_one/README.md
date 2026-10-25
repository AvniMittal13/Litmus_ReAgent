# MagneticOne Scripts

## File Differences

| File | Batch Processing | Scenario Selection | Lines |
|------|-----------------|-------------------|-------|
| `run_all_magnetic_one.py` | ✅ Yes (batch_size param) | ❌ No (runs all) | 648 |
| `run_all_magnetic_one copy.py` | ❌ No | ❌ No (runs all) | 598 |
| `run_all_magnetic_one copy 2.py` | ✅ Yes (batch_size param) | ✅ Yes (select 1-5) | 705 |

## Summary

- **`run_all_magnetic_one.py`**: Base version with batch processing. Processes all scenarios automatically.

- **`run_all_magnetic_one copy.py`**: Older/simpler version without batch processing. Processes questions sequentially.

- **`run_all_magnetic_one copy 2.py`**: **Latest/most featured** - adds scenario selection UI. User can choose specific scenarios (1-5) or run all. Includes `SCENARIO_DESCRIPTIONS` display and `get_scenario_selection()` method.

## Usage

Use `run_all_magnetic_one copy 2.py` for most control over which scenarios to run.
