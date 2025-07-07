CREATE TABLE IF NOT EXISTS dados (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT DEFAULT (datetime('now')),
    titulo TEXT NOT NULL,
    dados TEXT NOT NULL
);
