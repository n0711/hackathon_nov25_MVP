# Data Schemas (CSV)

## users.csv
- user_id (str)

## items.csv
- item_id (str)
- skill_id (str)

## interactions.csv
- user_id (str)
- item_id (str)
- skill_id (str)   # denormalized for speed
- correct (int)    # 1 or 0
- ts (iso8601)     # optional
