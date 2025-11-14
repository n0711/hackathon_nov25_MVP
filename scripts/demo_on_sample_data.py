import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'sample_data' / 'demo_class.csv'


def load_rows():
    if not DATA.exists():
        raise SystemExit(f'Sample data not found at {DATA}')
    with DATA.open(newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)


def _to_float(row, key, default=0.0):
    try:
        return float(row.get(key, default) or default)
    except ValueError:
        return default


def main():
    rows = load_rows()
    if not rows:
        print('No rows in demo_class.csv')
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

    print('LearnTwin demo on sample_data/demo_class.csv')
    print('-' * 50)
    print(f'Students in file     : {total}')
    print(f'Average score        : {avg_score:.1f}')
    print(f'Average attendance   : {avg_att*100:.1f}%')
    print()
    print(f'Students flagged as at-risk (simple rule): {len(at_risk)}')
    for r in at_risk:
        sid = r.get('student_id', '?')
        name = r.get('student_name', '?')
        print(f'  - {sid} | {name}')


if __name__ == '__main__':
    main()
