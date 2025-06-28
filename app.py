import sqlite3
import TkEasyGUI as sg

DB_PATH = "dqx_status_sim.db"
COMBO_KEY = "-DROPDOWN-"
# 表示するフィールドと表示名（順序）
STATS_FIELDS = [
    ("hp", "HP"),
    ("mp", "MP"),
    ("strength", "ちから"),
    ("resilience", "みのまもり"),
    ("agility", "すばやさ"),
    ("deftness", "きようさ"),
    ("magical-might", "こうげき魔力"),
    ("magical-mending", "かいふく魔力"),
    ("charm", "みりょく"),
    ("weight", "おもさ"),
]


def load_job_names(db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT job_name FROM job")
    rows = cur.fetchall()
    conn.close()
    return [r[0] for r in rows]


def load_job_stats(job_name, db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(
        '''
        SELECT hp, mp, strength, resilience, agility, deftness,
               "magical-might", "magical-mending", charm, weight
        FROM job WHERE job_name = ?
        ''', (job_name,)
    )
    row = cur.fetchone()
    conn.close()
    return dict(zip([f[0] for f in STATS_FIELDS], row)) if row else {}


def main():
    job_names = load_job_names()
    if not job_names:
        sg.popup("ジョブがロードされませんでした。DBパスを確認してください.")
        return

    # コンボとステータス行を作成
    layout = [
        [
            sg.Text("ジョブを選択：", size=(12, 1)),
            sg.Combo(
                job_names,
                default_value=job_names[0],
                key=COMBO_KEY,
                size=(20, 1),
                enable_events=True
            )
        ]
    ]
    # 各ステータス行の Text 要素を用意し、区切り線を追加
    line_width = 12 + 10  # label幅12 + value幅10
    for key, label in STATS_FIELDS:
        layout.append([
            sg.Text(label, size=(12, 1)),
            sg.Text("", size=(10, 1), key=f"-{key.upper()}-")
        ])
        # 区切り線
        layout.append([
            sg.Text("─" * line_width, size=(line_width, 1))
        ])
    layout.append([sg.Button("閉じる")])

    window = sg.Window("ステータス表示", layout)

    # 初期表示値設定
    stats = load_job_stats(job_names[0])
    for f, _ in STATS_FIELDS:
        window[f"-{f.upper()}-"].update(stats.get(f, ""))

    # イベントループ
    while True:
        ev, vals = window.read()
        if ev in (sg.WINDOW_CLOSED, "閉じる"):
            break
        if ev == COMBO_KEY:
            stats = load_job_stats(vals[COMBO_KEY])
            for f, _ in STATS_FIELDS:
                window[f"-{f.upper()}-"].update(stats.get(f, ""))

    window.close()


if __name__ == "__main__":
    main()
