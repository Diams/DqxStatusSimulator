#!/usr/bin/env python3
# migrate.py

import argparse
import sqlite3
import csv
import os
import sys


def import_jobs(csv_path: str, db_path: str, table_name: str):
    # CSV ファイルチェック
    if not os.path.exists(csv_path):
        print(f'Error: CSV file "{csv_path}" does not exist.', file=sys.stderr)
        sys.exit(1)

    # DB 接続／テーブル作成
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            job_ID   INTEGER PRIMARY KEY,
            job_name TEXT NOT NULL
        );
    ''')

    # CSV 読み込み & インサート
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = []
        for row in reader:
            if not row:
                continue
            # row[0] → job_ID, row[1] → job_name
            job_id = row[0].strip()
            job_name = row[1].strip() if len(row) > 1 else ''
            rows.append((job_id, job_name))

    cur.executemany(
        f'INSERT OR REPLACE INTO {table_name} (job_ID, job_name) VALUES (?, ?);',
        rows
    )
    conn.commit()
    conn.close()

    print(
        f'Imported {len(rows)} rows into "{db_path}" → table "{table_name}".')


def main():
    parser = argparse.ArgumentParser(
        description='CSV(job_ID,job_name) を SQLite3 にインポートします'
    )
    parser.add_argument(
        '--job',
        required=True,
        help='インポート対象のCSVファイルパス'
    )
    parser.add_argument(
        '--db',
        default='job.db',
        help='出力するSQLiteファイル名 (デフォルト: job.db)'
    )
    parser.add_argument(
        '--table',
        default='job',
        help='作成／使用するテーブル名 (デフォルト: job)'
    )
    args = parser.parse_args()

    import_jobs(args.job, args.db, args.table)


if __name__ == '__main__':
    main()
