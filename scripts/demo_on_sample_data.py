import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / 'sample_data'
DEFAULT_NAME = 'demo_class.csv'


def find_data_file() -> Path:
    # Return a CSV path under sample_data/, or exit with a clear message.
    if not DATA_DIR.exists():
        raise SystemExit(f'sample_data/ directory not found at {DATA_DIR}')

    candidate = DATA_DIR / DEFAULT_NAME
    if candidate.exists():
        return candidate

    csv_files = sorted(DATA_DIR.glob('*.csv'))
    if not csv_files:
        raise SystemExit(f'No CSV files found under {DATA_DIR}')

    # Fall back to the first CSV we find
    print(f'[{DEFAULT_NAME} not found] Using {csv_files[0].name} instead.')
    return csv_files[0]


def load_rows(path: Path):
    with path.open(newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)


def _to_float(row, key, default=0.0):
    try:
        return float(row.get(key, default) or default)
    except ValueError:
        return default


def main():
    data_path = find_data_file()
    rows = load_rows(data_path)
    if not rows:
        print(f'No rows in {data_path}')
        return

    total = len(rows)
    avg_score = sum(_to_float(r, 'avg_score') for r in rows) / total
    avg_att = sum(_to_float(r, 'attendance_rate') for r in rows) / total

    at_risk = []
    for r in rows:
        score = _to_float(r, 'avg_score')
        att = _to_float(r, 'attendance_rate')
        last = _to_float(r, 'last_activity_days_ago')
        if score < 60 or att < 0.8 or last > 14:
            at_risk.append(r)

    print('LearnTwin demo on sample data')
    print('-' * 50)
    print(f'File used           : {data_path.relative_to(ROOT)}')
    print(f'Students in file    : {total}')
    print(f'Average score       : {avg_score:.1f}')
    print(f'Average attendance  : {avg_att*100:.1f}%')
    print()
    print(f'Students flagged as at-risk (simple rule): {len(at_risk)}')
    for r in at_risk:
        sid = r.get('student_id', '?')
        name = r.get('student_name', '?')
        print(f'  - {sid} | {name}')


if __name__ == '__main__':
    main()
