import sqlite3
import TkEasyGUI as sg


def load_job_names(db_path="job.db"):
    """
    SQLite の job テーブルから job_name をすべて取得してリストで返す
    """
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT job_name FROM job")
    rows = cur.fetchall()
    conn.close()
    # fetchall() の結果は [(name1,), (name2,), …] の形なので、[0] を取り出す
    return [row[0] for row in rows]


# 1) データベースから job_name リストを取得
job_names = load_job_names("dqx_status_sim.db")

# 2) 取得結果を元にレイアウトを定義
layout = [
    [sg.Text("選択してください：")],
    [sg.Combo(
        job_names,
        default_value=job_names[0] if job_names else "",
        key="-DROPDOWN-",
        enable_events=True
    )],
    [sg.Button("実行"), sg.Button("閉じる")]
]

# 3) ウィンドウ生成＆イベントループ
window = sg.Window("プルダウン例", layout)

while True:
    event, values = window.read()
    # ウィンドウを閉じる or 「閉じる」ボタン
    if event in (sg.WINDOW_CLOSED, "閉じる"):
        break

    # コンボボックスの選択が変わったとき
    if event == "-DROPDOWN-":
        print("新しい選択:", values["-DROPDOWN-"])

    # 「実行」ボタンが押されたとき
    if event == "実行":
        sg.popup(f"現在の選択: {values['-DROPDOWN-']}")

window.close()
