CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    firstname TEXT,
    telephone_number TEXT UNIQUE,
    email TEXT UNIQUE,
    password TEXT,
    role TEXT,
    created_at DATETIME,
    parent_id INTEGER,
    FOREIGN KEY (parent_id) REFERENCES Users(id)
);
