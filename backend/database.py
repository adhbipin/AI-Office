import sqlite3

def init_db():
    conn = sqlite3.connect('/Users/bipin/programming/projects/AI office System/ai-office/workspace/ai_office.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agent_from TEXT,
            agent_to TEXT,
            message TEXT,
            timestamp DATETIME
        )
    ''')
    conn.commit()
    conn.close()

def save_message(agent_from, agent_to, message, timestamp):
    conn = sqlite3.connect('/Users/bipin/programming/projects/AI office System/ai-office/workspace/ai_office.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO messages (agent_from, agent_to, message, timestamp) VALUES (?, ?, ?, ?)', 
                   (agent_from, agent_to, message, timestamp))
    conn.commit()
    conn.close()
