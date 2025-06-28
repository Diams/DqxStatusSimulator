import sqlite3
import TkEasyGUI as sg

DB_PATH = "dqx_status_sim.db"
COMBO_KEY = "-DROPDOWN-"
TABLE_KEY = "-TABLE-"
# フィールドと表示名（順序）
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
    rows = conn.execute("SELECT job_name FROM job").fetchall()
    conn.close()
    return [r[0] for r in rows]


def load_job_stats(job_name, db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    row = conn.execute(
        '''
        SELECT hp, mp, strength, resilience, agility, deftness,
               "magical-might", "magical-mending", charm, weight
        FROM job WHERE job_name = ?
        ''', (job_name,)
    ).fetchone()
    conn.close()
    keys = [f[0] for f in STATS_FIELDS]
    return dict(zip(keys, row)) if row else {}


def main():
    job_names = load_job_names()
    if not job_names:
        sg.popup_error("ジョブがロードされませんでした。DBパスを確認してください。")
        return

    # コンボ行
    combo_row = [
        sg.Text("ジョブを選択：", size=(12, 1)),
        sg.Combo(
            job_names,
            default_value=job_names[0],
            key=COMBO_KEY,
            size=(20, 1),
            enable_events=True
        )
    ]

    # 初期テーブルデータ
    stats = load_job_stats(job_names[0])
    table_data = [[label, stats.get(key, "")] for key, label in STATS_FIELDS]

    # テーブルウィジェット
    table = sg.Table(
        values=table_data,
        headings=["ステータス", "値"],
        key=TABLE_KEY,
        auto_size_columns=True,
        justification='left',  # 全体左揃えデフォルト
        enable_events=False,
        expand_x=True,
        expand_y=True
    )

    layout = [
        combo_row,
        [table],
        [sg.Button("閉じる")]
    ]

    # Windowを生成してTreeview設定
    window = sg.Window("ステータス表示", layout, resizable=True, finalize=True)
    tree = window[TABLE_KEY].Widget
    cols = tree["columns"]
    # 値列（2列目）のセルは右揃え
    tree.column(cols[1], anchor='e')
    # 値列のヘッダーは中央揃え
    tree.heading(cols[1], anchor='center')

    while True:
        event, values = window.read()
        if event in (sg.WINDOW_CLOSED, "閉じる"):
            break
        if event == COMBO_KEY:
            stats = load_job_stats(values[COMBO_KEY])
            new_data = [[label, stats.get(key, "")]
                        for key, label in STATS_FIELDS]
            window[TABLE_KEY].update(values=new_data)

    window.close()


if __name__ == "__main__":
    main()
