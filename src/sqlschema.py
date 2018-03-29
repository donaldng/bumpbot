from environment.config import *
import sqlite3, records

def createDB():
	db = records.Database('sqlite:///{}'.format(dbname))

	db.query("""
	CREATE TABLE `user` (
		`user_id`	INTEGER PRIMARY KEY AUTOINCREMENT,
		`username`	TEXT UNIQUE,
		`password`	TEXT,
		`firsttime`	INTEGER DEFAULT 1,
		`created_at`	DATETIME DEFAULT 0
	);
	CREATE TABLE `post` (
		`post_id`	INTEGER,
		`title`	TEXT,
		`url`	TEXT,
		`count`	INTEGER DEFAULT 0,
		`status`	INTEGER DEFAULT 1,
		`deleted`	INTEGER DEFAULT 0,
		`user_id`	INTEGER,
		`next_execution`	INTEGER DEFAULT 0,
		`created_at`	INTEGER,
		`updated_at`	INTEGER,
		`last_bump`	INTEGER DEFAULT 0,
		PRIMARY KEY(`post_id`)
	);
	""")