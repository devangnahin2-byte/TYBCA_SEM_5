import sqlite3

def check_db():
    try:
        conn = sqlite3.connect(r"d:\TYBCA 2026\TYBCA_SEM_5\TYBCA_SEM_5\auth.db")
        cursor = conn.cursor()
        cursor.execute("SELECT username, email, role FROM users")
        rows = cursor.fetchall()
        print(f"Users in DB: {len(rows)}")
        for r in rows:
            print(r)
        conn.close()
    except Exception as e:
        print(f"DB Error: {e}")

if __name__ == "__main__":
    check_db()
