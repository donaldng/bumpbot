import sqlite3, records

db = records.Database('sqlite:///haha.db')

db.query("""
CREATE TABLE IF NOT EXISTS `user` (
	`user_id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`username`	TEXT UNIQUE,
	`password`	TEXT
);
""")

db.query("""
CREATE TABLE IF NOT EXISTS `post` (
	`post_id`	INTEGER,
	`title`	TEXT,
	`url`	TEXT,
	`count`	INTEGER DEFAULT 0,
	`status`	INTEGER DEFAULT 1,
	`user_id`	INTEGER,
	`created_at`	INTEGER,
	`updated_at`	INTEGER,
	PRIMARY KEY(`post_id`)
);
""")