import sqlite3

def create_audio_file_db():
    conn = sqlite3.connect("audio_files.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS audio_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT UNIQUE,
            data BLOB
        )
    ''')
    conn.commit()
    conn.close()

def insert_audio_file(filename, file_bytes):
    conn = sqlite3.connect("audio_files.db")
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO audio_files (filename, data) VALUES (?, ?)", (filename, file_bytes))
    conn.commit()
    conn.close()

def get_audio_file(filename):
    conn = sqlite3.connect("audio_files.db")
    c = conn.cursor()
    c.execute("SELECT data FROM audio_files WHERE filename = ?", (filename,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None
