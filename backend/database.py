import sqlite3
from config import DB_PATH
from datetime import datetime

def init_db():
    """Initialize the database with messages table."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_from TEXT,
                agent_to TEXT,
                message TEXT,
                timestamp DATETIME,
                message_type TEXT DEFAULT 'chat'
            )
        ''')
        conn.commit()
        conn.close()
        print(f"✅ Database initialized at {DB_PATH}")
    except Exception as e:
        print(f"❌ Database init error: {e}")

def save_message(agent_from: str, agent_to: str, message: str, timestamp: str = None, msg_type: str = 'chat'):
    """Save a message to the database."""
    try:
        if not timestamp:
            timestamp = datetime.utcnow().isoformat()
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO messages (agent_from, agent_to, message, timestamp, message_type) VALUES (?, ?, ?, ?, ?)',
            (agent_from, agent_to, message, timestamp, msg_type)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"❌ Error saving message: {e}")

def get_messages(limit: int = 100) -> list:
    """Retrieve messages from database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM messages ORDER BY timestamp DESC LIMIT ?', (limit,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    except Exception as e:
        print(f"❌ Error retrieving messages: {e}")
        return []
