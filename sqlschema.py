from environment.config import *
import sqlite3, records

def createDB():
	db = records.Database('sqlite:///{}'.format(dbname))

	db.query("""
	CREATE TABLE IF NOT EXISTS `user` (
		`user_id`	INTEGER PRIMARY KEY AUTOINCREMENT,
		`username`	TEXT UNIQUE,
		`password`	TEXT
	);
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