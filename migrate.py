#!/usr/bin/env python3
# migrate.py

import argparse
import sqlite3
import csv
import os
import sys

# テーブルの列定義（CSVの順序に対応）
FIELDS = [
    "job_ID",
    "job_name",
    "hp",
    "mp",
    "strength",
    "resilience",
    "agility",
    "deftness",
    "magical-might",
    "magical-mending",
    "charm",
    "weight",
]


def import_jobs(csv_path: str, db_path: str, table_name: str):
    # CSVファイルの存在チェック
    if not os.path.exists(csv_path):
        print(
            f'Error: CSV file "{csv_path}" does not exist.',
            file=sys.stderr
        )
        sys.exit(1)

    # DB接続／テーブル作成
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # カラム定義を自動で生成
    cols_def = []
    for col in FIELDS:
        if col == "job_ID":
            cols_def.append("job_ID INTEGER PRIMARY KEY")
        elif col == "job_name":
            cols_def.append("job_name TEXT NOT NULL")
        elif col == "weight":
            cols_def.append("weight REAL")
        else:
            cols_def.append(f'"{col}" INTEGER')

    # テーブル作成SQLを組み立て
    sep = ",\n    "
    columns_sql = sep.join(cols_def)
    create_sql = (
        f"CREATE TABLE IF NOT EXISTS {table_name} (\n"
        f"    {columns_sql}\n"
        f");"
    )
    cur.execute(create_sql)

    # CSV読み込み & データ整形
    rows = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            values = []
            for i in range(len(FIELDS)):
                val = row[i].strip() if i < len(
                    row) and row[i].strip() else None
                values.append(val)
            rows.append(tuple(values))

    # INSERT文の生成
    placeholders = ",".join(["?"] * len(FIELDS))
    cols_list = ",".join([f'"{col}"' for col in FIELDS])
    sql = (
        'INSERT OR REPLACE INTO '
        f'{table_name} ({cols_list}) VALUES ({placeholders});'
    )
    cur.executemany(sql, rows)

    conn.commit()
    conn.close()

    print(
        f'Imported {len(rows)} rows into "{db_path}" '
        f'→ table "{table_name}".'
    )


def main():
    parser = argparse.ArgumentParser(
        description=(
            "CSV(job_ID,job_name,hp,mp,strength,resilience,"
            "agility,deftness,magical-might,magical-mending,"
            "charm,weight) を SQLite3 にインポートします"
        )
    )
    parser.add_argument(
        "--job", required=True,
        help="インポート対象のCSVファイルパス"
    )
    parser.add_argument(
        "--db", default="job.db",
        help="出力するSQLiteファイル名 (デフォルト: job.db)"
    )
    parser.add_argument(
        "--table", default="job",
        help="作成／使用するテーブル名 (デフォルト: job)"
    )
    args = parser.parse_args()

    import_jobs(args.job, args.db, args.table)


if __name__ == "__main__":
    main()
