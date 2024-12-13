import sqlite3

# Cria o banco de dados e a tabela de usuários, se não existir
conn = sqlite3.connect('usuarios.db')

conn.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL
)
''')

conn.close()
print("Banco de dados inicializado com sucesso!")
