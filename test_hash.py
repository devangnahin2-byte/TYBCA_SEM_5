import sqlite3
import hashlib

def test_login():
    conn = sqlite3.connect(r"d:\TYBCA 2026\TYBCA_SEM_5\TYBCA_SEM_5\auth.db")
    cursor = conn.cursor()
    
    # Check what hash is stored
    cursor.execute("SELECT password FROM users WHERE username='Vipul'")
    res = cursor.fetchone()
    if res:
        stored_hash = res[0]
        print(f"Stored hash: {stored_hash}")
        
        test_pw = "vipul@123"
        computed_hash = hashlib.sha256(test_pw.encode()).hexdigest()
        print(f"Computed hash: {computed_hash}")
        
        if stored_hash == computed_hash:
            print("Password matches!")
        else:
            print("Password does NOT match! The user might have typed something else during registration.")
    else:
        print("User Vipul not found.")
    conn.close()

if __name__ == "__main__":
    test_login()
