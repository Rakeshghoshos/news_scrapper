import sqlite3
from datetime import datetime
from typing import List, Dict, Set
import logging
import os

import pytz

ist = pytz.timezone('Asia/Kolkata')
ist_time = datetime.now(ist)


logging.basicConfig(
    filename=os.path.join(os.path.dirname(__file__), "..", "logs", "scraper.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class Database:
    def __init__(self, db_name: str = os.path.join(os.path.dirname(__file__), "..", "data", "news.db")):
        self.db_name = os.path.abspath(db_name)
        os.makedirs(os.path.dirname(self.db_name), exist_ok=True)
        self._init_db()

    def _init_db(self):
        """Initialize the SQLite database with news table only."""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS news (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        headline TEXT NOT NULL,
                        link TEXT NOT NULL UNIQUE,
                        source TEXT NOT NULL,
                        scraped_at TIMESTAMP NOT NULL
                    )
                """)
                conn.commit()
                logging.info(f"Database initialized successfully at {self.db_name}")
        except sqlite3.Error as e:
            logging.error(f"Error initializing database: {e}")

    def insert_news(self, headline: str, link: str, source: str) -> bool:
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM news WHERE link = ?", (link,))
                if cursor.fetchone()[0] > 0:
                    logging.debug(f"Skipped duplicate news with link: {link}")
                    return False
                cursor.execute("""
                    INSERT INTO news (headline, link, source, scraped_at)
                    VALUES (?, ?, ?, ?)
                """, (headline, link, source,  ist_time.isoformat()))
                conn.commit()
                logging.info(f"Inserted news with link: {link}")
                return True
        except sqlite3.IntegrityError:
            logging.debug(f"Duplicate news link skipped: {link}")
            return False
        except sqlite3.Error as e:
            logging.error(f"Database error during news insert: {e}")
            return False

    def get_all_news(self) -> List[Dict]:
        try:
            with sqlite3.connect(self.db_name) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM news ORDER BY scraped_at DESC")
                return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            logging.error(f"Database error during news retrieval: {e}")
            return []

    def get_existing_news_links(self) -> Set[str]:
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT link FROM news")
                return {row[0] for row in cursor.fetchall()}
        except sqlite3.Error as e:
            logging.error(f"Error retrieving existing news links: {e}")
            return set()

    def delete_all_data(self) -> bool:
        """Delete all data from the news table."""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM news")
                conn.commit()
                logging.info("Successfully deleted all news")
                return True
        except sqlite3.Error as e:
            logging.error(f"Database error during cleanup: {e}")
            return False
