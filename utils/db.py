import sqlite3

db = sqlite3.connect("database.db")
db.row_factory = sqlite3.Row
cur = db.cursor()


def get_db_cur():
    return db, cur


def get_sender_account(sender_id, tag, index=0) -> str:
    try:
        idx = int(index)
    except:
        idx = 0
    if idx == 0:
        cur.execute(
            "SELECT * FROM accounts WHERE qq = ? ORDER BY is_last_used DESC, steamid32 LIMIT 1", (sender_id, ))
    else:
        cur.execute(
            "SELECT * FROM accounts WHERE qq = ? ORDER BY steamid32 LIMIT %d, 1" % idx, (sender_id, ))
    row = cur.fetchone()
    if not row:
        return "ACCOUNT_NOT_EXIST"
    if tag in dict(row):
        return row[tag]
    return ''


def set_main_account(sender_id, index=0):
    try:
        idx = int(index) - 1
    except:
        idx = 0
    cur.execute("SELECT * FROM accounts WHERE qq = ? ORDER BY steamid32 LIMIT %d, 1" % idx, (sender_id, ))
    row = cur.fetchone()
    if not row:
        return None
    cur.execute("UPDATE accounts SET is_last_used = (steamid32 = ?) WHERE qq = ?", (row['steamid32'], sender_id))
    db.commit()
    return dict(row)


def get_sender_all_accounts(sender_id) -> list:
    cur.execute("SELECT * FROM accounts WHERE qq = ? ORDER BY steamid32", (sender_id, ))
    for idx, row in enumerate(cur.fetchall()):
        yield idx+1, dict(row)
