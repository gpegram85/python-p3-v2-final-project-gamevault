import sqlite3

CONN = sqlite3.connect('vault.db')
CURSOR = CONN.cursor()