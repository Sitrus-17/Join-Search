import sqlite3
from datetime import datetime, timedelta

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # 既存のテーブルを削除
    c.execute('DROP TABLE IF EXISTS events')

    # 新しいテーブルを作成
    c.execute('''CREATE TABLE events (
        id INTEGER PRIMARY KEY,
        artist TEXT,
        place TEXT,
        date TEXT,
        time TEXT,
        work_matter TEXT,
        reserve_status TEXT
    )''')
    conn.commit()
    conn.close()

def save_data(event_list):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    for event in event_list:
        c.execute("INSERT INTO events (artist, place, date, time, work_matter, reserve_status) VALUES (?, ?, ?, ?, ?, ?)",
                  (event['アーティスト'], event['会場'], event['日付'], event['時間'], event['業務内容'], event['予約状態']))
    conn.commit()
    conn.close()

def count_events(year, month, work_matter=None, reserve_statuses=None):
    def create_date_range(year, month):
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1) - timedelta(days=1)
        else:
            end_date = datetime(year, month + 1, 1) - timedelta(days=1)
        return [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]

    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    date_range = create_date_range(year, month)
    event_counts = []

    for date in date_range:
        formatted_date = date.strftime('%Y-%m-%d')
        query = "SELECT COUNT(*) FROM events WHERE date = ?"
        params = [formatted_date]

        if work_matter:
            placeholders1 = ','.join(['?'] * len(work_matter))
            query += f" AND reserve_status IN ({placeholders1})"
            params.extend(work_matter)
        if reserve_statuses:
            placeholders2 = ','.join(['?'] * len(reserve_statuses))
            query += f" AND reserve_status IN ({placeholders2})"
            params.extend(reserve_statuses)

        c.execute(query, params)
        event_count = c.fetchone()[0]
        event_counts.append(event_count)

    conn.close()
    return event_counts

def get_data(year, month, day, work_matte=None, reserve_statuses=None):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    date = datetime(year, month, day).strftime('%Y-%m-%d')
    query = "SELECT * FROM events WHERE date = ?"
    params = [date]

    if work_matte:
        placeholders1 = ','.join(['?'] * len(work_matte))
        query += f" AND reserve_status IN ({placeholders2})"
        params.extend(work_matte)
    if reserve_statuses:
        placeholders2 = ','.join(['?'] * len(reserve_statuses))
        query += f" AND reserve_status IN ({placeholders2})"
        params.extend(reserve_statuses)

    c.execute(query, params)
    events = c.fetchall()

    conn.close()
    return events
