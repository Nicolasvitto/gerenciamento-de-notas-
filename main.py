from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

DB_NAME = 'alunos.db'

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS alunos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL,
                        matricula TEXT NOT NULL UNIQUE,
                        email TEXT NOT NULL
                    )''')
        c.execute('''CREATE TABLE IF NOT EXISTS notas (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        aluno_id INTEGER NOT NULL,
                        disciplina TEXT NOT NULL,
                        nota REAL NOT NULL,
                        FOREIGN KEY(aluno_id) REFERENCES alunos(id)
                    )''')
        conn.commit()

@app.route('/alunos', methods=['GET'])
def listar_alunos():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM alunos')
        alunos = [dict(id=row[0], nome=row[1], matricula=row[2], email=row[3]) for row in c.fetchall()]
    return jsonify(alunos)

@app.route('/alunos', methods=['POST'])
def cadastrar_aluno():
    data = request.get_json()
    if not all(k in data for k in ('nome', 'matricula', 'email')):
        return jsonify({'erro': 'Dados incompletos'}), 400
    try:
        with sqlite3.connect(DB_NAME) as conn:
            c = conn.cursor()
            c.execute('INSERT INTO alunos (nome, matricula, email) VALUES (?, ?, ?)',
                      (data['nome'], data['matricula'], data['email']))
            conn.commit()
        return jsonify({'mensagem': 'Aluno cadastrado com sucesso'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'erro': 'Matrícula já cadastrada'}), 400

@app.route('/notas', methods=['POST'])
def registrar_nota():
    data = request.get_json()
    if not all(k in data for k in ('aluno_id', 'disciplina', 'nota')):
        return jsonify({'erro': 'Dados incompletos'}), 400
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute('SELECT 1 FROM alunos WHERE id=?', (data['aluno_id'],))
        if not c.fetchone():
            return jsonify({'erro': 'Aluno não encontrado'}), 404
        c.execute('INSERT INTO notas (aluno_id, disciplina, nota) VALUES (?, ?, ?)',
                  (data['aluno_id'], data['disciplina'], data['nota']))
        conn.commit()
    return jsonify({'mensagem': 'Nota registrada com sucesso'}), 201

@app.route('/alunos/<int:aluno_id>/notas', methods=['GET'])
def ver_notas(aluno_id):
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute('SELECT disciplina, nota FROM notas WHERE aluno_id=?', (aluno_id,))
        notas = c.fetchall()
        if not notas:
            return jsonify({'notas': [], 'media': 0.0})
        media = sum(n[1] for n in notas) / len(notas)
        notas_dict = [{'disciplina': n[0], 'nota': n[1]} for n in notas]
    return jsonify({'notas': notas_dict, 'media': round(media, 2)})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
