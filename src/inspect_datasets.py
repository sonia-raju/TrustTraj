"""
inspect_datasets.py  -  TrustTraj, Week 3
Load the BIRD mini-dev dataset and report basic statistics.
Standard library only (json, sqlite3, pathlib, collections).
"""
import json
import sqlite3
from pathlib import Path
from collections import Counter

DATA_DIR = Path(__file__).resolve().parent.parent / "data"   # the folder you extracted the dataset into

# Find the files no matter how deeply they're nested
question_file = next(DATA_DIR.rglob("mini_dev_sqlite.json"))
db_files = sorted(DATA_DIR.rglob("*.sqlite"))

# --- 1. Question-level statistics ---------------------------------------
with open(question_file, encoding="utf-8") as f:
    records = json.load(f)

print("Question file :", question_file)
print("Total records :", len(records))
print("Fields        :", list(records[0].keys()))

by_difficulty = Counter(r["difficulty"] for r in records)
print("\nBy difficulty:")
for tier in ("simple", "moderate", "challenging"):
    print(f"  {tier:<12}: {by_difficulty[tier]}")

by_db = Counter(r["db_id"] for r in records)
print(f"\nDistinct databases referenced: {len(by_db)}")
for db, n in sorted(by_db.items()):
    print(f"  {db:<26}: {n}")

# --- 2. Database / schema statistics ------------------------------------
print(f"\nSQLite database files on disk: {len(db_files)}")
for db_path in db_files:
    con = sqlite3.connect(db_path); cur = con.cursor()
    cur.execute("SELECT name FROM sqlite_master "
                "WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name")
    tables = [row[0] for row in cur.fetchall()]
    print(f"\n{db_path.stem}: {len(tables)} tables")
    for t in tables:
        cur.execute(f'PRAGMA table_info("{t}")'); n_cols = len(cur.fetchall())
        cur.execute(f'SELECT COUNT(*) FROM "{t}"'); n_rows = cur.fetchone()[0]
        print(f"  {t:<22} {n_cols:>3} cols, {n_rows:>8} rows")
    con.close()

# --- 3. Preprocessing / integrity checks --------------------------------
missing = [r for r in records
           if not all(k in r and r[k] is not None
                      for k in ("db_id", "question", "SQL", "difficulty"))]
print("\nIntegrity checks")
print("  records with a missing field        :", len(missing))
print("  db_ids referenced but missing on disk:",
      (set(by_db) - {p.stem for p in db_files}) or "none")
print("\nDone - datasets loaded and inspected successfully.")
