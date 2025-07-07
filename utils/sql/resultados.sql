CREATE TABLE IF NOT EXISTS resultados (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    resposta TEXT NOT NULL,
    id_dados INTEGER NOT NULL,
    id_solicitacao INTEGER NOT NULL,
    data TEXT DEFAULT (datetime('now'))
);