# setup_db.py 
# This script initializes the SQLite database and creates necessary tables.

import sqlite3
from src.constants import DATABASE_PATH

def init_db():
    """Initialize the SQLite database with necessary tables."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Create the conversations table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id TEXT PRIMARY KEY,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create the feedback table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id TEXT NOT NULL,
            feedback INTEGER NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (conversation_id) REFERENCES conversations (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def save_conversation(conversation_id, question, answer):
    """Save a conversation to the database."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO conversations (id, question, answer) VALUES (?, ?, ?)
    ''', (conversation_id, question, answer))
    
    conn.commit()
    conn.close()

def save_feedback(conversation_id, feedback):
    """Save feedback to the database."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO feedback (conversation_id, feedback) VALUES (?, ?)
    ''', (conversation_id, feedback))
    
    conn.commit()
    conn.close()

def get_recent_conversations(limit=5, relevance=None):
    """Retrieve recent conversations from the database."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    query = 'SELECT * FROM conversations ORDER BY timestamp DESC LIMIT ?'
    params = [limit]
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    
    # Convert rows to dictionaries for easier access
    conversations = []
    for row in rows:
        conversation = {
            'id': row[0],
            'question': row[1],
            'answer': row[2],
            'timestamp': row[3]
        }
        conversations.append(conversation)
    
    return conversations

def get_feedback_stats():
    """Retrieve feedback statistics from the database."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Count positive feedback
    cursor.execute('''
        SELECT COUNT(*) FROM feedback WHERE feedback = 1
    ''')
    thumbs_up = cursor.fetchone()[0]
    
    # Count negative feedback
    cursor.execute('''
        SELECT COUNT(*) FROM feedback WHERE feedback = -1
    ''')
    thumbs_down = cursor.fetchone()[0]
    
    conn.close()
    
    return {
        'thumbs_up': thumbs_up,
        'thumbs_down': thumbs_down
    }

if __name__ == "__main__":
    init_db()
    print("Database initialized and tables created.")
