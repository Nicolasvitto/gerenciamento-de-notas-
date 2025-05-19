from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client, Client
from dotenv import load_dotenv
import os

# Carrega variáveis do .env
load_dotenv()
print(os.getenv("SUPABASE_URL"))
print(os.getenv("SUPABASE_KEY"))

app = Flask(__name__)
CORS(app)

# Conexão com o Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Criar aluno
@app.route('/alunos', methods=['POST'])
def criar_aluno():
    data = request.json
    res = supabase.table("aluno").insert({
        "nome": data['nome'],
        "matricula": data['matricula'],
        "email": data['email']
    }).execute()
    return jsonify({'mensagem': 'Aluno criado com sucesso', 'resposta': res.data})

# Listar alunos
@app.route('/alunos', methods=['GET'])
def listar_alunos():
    res = supabase.table("aluno").select("*").execute()
    return jsonify(res.data)

# Registrar nota
@app.route('/notas', methods=['POST'])
def registrar_nota():
    data = request.json
    res = supabase.table("nota").insert({
        "aluno_id": data['aluno_id'],
        "disciplina": data['disciplina'],
        "nota": data['nota']
    }).execute()
    return jsonify({'mensagem': 'Nota registrada com sucesso', 'resposta': res.data})

# Ver notas de um aluno
@app.route('/alunos/<int:aluno_id>/notas', methods=['GET'])
def ver_notas(aluno_id):
    res = supabase.table("nota").select("*").eq("aluno_id", aluno_id).execute()
    notas = res.data
    if not notas:
        return jsonify({'notas': [], 'media': 0.0})
    media = round(sum(n['nota'] for n in notas) / len(notas), 2)
    return jsonify({
        'notas': [{'disciplina': n['disciplina'], 'nota': n['nota']} for n in notas],
        'media': media
    })

if __name__ == '__main__':
    app.run(debug=True)
