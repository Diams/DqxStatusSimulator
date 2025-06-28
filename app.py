import sqlite3
import TkEasyGUI as sg

DB_PATH = "dqx_status_sim.db"
COMBO_KEY = "-DROPDOWN-"
STATS_FIELDS = [
    "strength", "resilience", "agility", "deftness",
    "magical-might", "magical-mending", "charm", "weight"
]
# キー名マッピング
FIELD_KEYS = {f: f"-{f.upper()}-" for f in STATS_FIELDS}


def load_job_names(db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT job_name FROM job")
    rows = cur.fetchall()
    conn.close()
    return [row[0] for row in rows]


def load_job_stats(job_name, db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(
        """
        SELECT strength, resilience, agility, deftness,
               "magical-might", "magical-mending", charm, weight
        FROM job
        WHERE job_name = ?
        """, (job_name,)
    )
    row = cur.fetchone()
    conn.close()
    if not row:
        return {}
    return dict(zip(STATS_FIELDS, row))


def main():
    job_names = load_job_names()
    # コンボ＋ステータス表示エリアのレイアウト
    stats_layout = []
    for field in STATS_FIELDS:
        stats_layout.append([
            sg.Text(field),
            sg.Text("", key=FIELD_KEYS[field])
        ])

    layout = [
        [
            sg.Text("選択してください："),
            sg.Combo(
                job_names,
                default_value=job_names[0] if job_names else "",
                key=COMBO_KEY,
                enable_events=True
            )
        ],
        *stats_layout,
        [sg.Button("閉じる")]
    ]

    window = sg.Window("ステータス表示", layout)
    while True:
        event, values = window.read()
        if event in (sg.WINDOW_CLOSED, "閉じる"):
            break

        if event == COMBO_KEY:
            selected = values[COMBO_KEY]
            stats = load_job_stats(selected)
            # 全フィールドを更新
            for field in STATS_FIELDS:
                key = FIELD_KEYS[field]
                window[key].update(stats.get(field, ""))

    window.close()


if __name__ == "__main__":
    main()
