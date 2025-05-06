import sqlite3
import numpy as np

def create_audio_feature_db():
    conn = sqlite3.connect("audio_features.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS audio_features (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT UNIQUE,
            mfcc TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_audio_feature(filename, mfcc):
    conn = sqlite3.connect("audio_features.db")
    c = conn.cursor()
    mfcc_str = ','.join(map(str, mfcc.flatten()))
    c.execute("INSERT OR REPLACE INTO audio_features (filename, mfcc) VALUES (?, ?)", (filename, mfcc_str))
    conn.commit()
    conn.close()

def get_all_features():
    conn = sqlite3.connect("audio_features.db")
    c = conn.cursor()
    c.execute("SELECT filename, mfcc FROM audio_features")
    rows = c.fetchall()
    conn.close()
    return [(filename, np.fromstring(mfcc, sep=",")) for filename, mfcc in rows]
