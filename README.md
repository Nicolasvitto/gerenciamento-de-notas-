# Gestão de Notas

Sistema web para cadastro de alunos e gerenciamento de notas, utilizando Python (Flask) no backend e HTML/JavaScript no frontend.

## Funcionalidades

- Cadastro de alunos (nome, matrícula, e-mail)
- Listagem de alunos cadastrados
- Registro de notas por disciplina para cada aluno
- Visualização das notas e média de cada aluno

## Tecnologias Utilizadas

- **Backend:** Python 3, Flask, Flask-CORS, SQLite
- **Frontend:** HTML, CSS, JavaScript

## Instalação e Execução

1. **Clone o repositório:**
   ```sh
   git clone https://github.com/Nicolasvitto/gerenciamento-de-notas-.git
   cd gerenciamento-de-notas-
   ```

2. **Crie um ambiente virtual (opcional, mas recomendado):**
   ```sh
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Instale as dependências:**
   ```sh
   pip install flask flask-cors
   ```

4. **Execute o backend:**
   ```sh
   python main.py
   ```
   O servidor Flask será iniciado em `http://localhost:5000`.

5. **Abra o frontend:**
   - Abra o arquivo `index.html` no seu navegador.

## Estrutura dos Arquivos

- `main.py`: Código do backend Flask e banco de dados SQLite.
- `index.html`: Interface web para interação com a API.
- `alunos.db`: Banco de dados SQLite (criado automaticamente ao rodar o backend).

## Endpoints da API

Abaixo estão os principais endpoints disponíveis na sua aplicação Flask:

### Alunos

- **Listar alunos**
  - `GET /alunos`
  - Retorna uma lista de todos os alunos cadastrados.

- **Cadastrar aluno**
  - `POST /alunos`
  - Recebe um JSON com os campos `nome`, `matricula` e `email` para cadastrar um novo aluno.
  - Exemplo de body:
    ```json
    {
      "nome": "João",
      "matricula": "456",
      "email": "joao@email.com"
    }
    ```

### Notas

- **Registrar nota**
  - `POST /notas`
  - Recebe um JSON com os campos `aluno_id`, `disciplina` e `nota` para registrar uma nota para um aluno.
  - Exemplo de body:
    ```json
    {
      "aluno_id": 1,
      "disciplina": "Matemática",
      "nota": 8.5
    }
    ```

- **Ver notas de um aluno**
  - `GET /alunos/<aluno_id>/notas`
  - Retorna todas as notas e a média do aluno especificado pelo `aluno_id`.

---

Esses endpoints são utilizados pelo frontend (`index.html`) para cadastrar, listar alunos e registrar/consultar notas.

## Observações

- O banco de dados é criado automaticamente ao rodar o backend.
- O frontend faz requisições para o backend usando `fetch`.
- O projeto é didático e pode ser expandido conforme a necessidade.

---

Desenvolvido para fins educacionais.