# Antonio Marcos de Sousa Oliveira - 2412039

# Houve uso de IA para a criação deste projeto devido ao meu próprio tempo pessoal ser escasso, no entanto eu acompanhei as partes desenvolvidas e acompanhar o passo a passo do desenvolvimento. O banco de dados foi escolhido por mim, onde eu mesmo realizei a instalação, configuração e conexão do mesmo com o projeto.

# 📚 StudyManager API

API RESTful completa para gerenciamento de **Usuários**, **Cursos** e **Matrículas**, desenvolvida com **Python**, **FastAPI**, **SQLAlchemy ORM** e **PostgreSQL**, aplicando conceitos de **Clean Architecture** (Arquitetura Limpa) e princípios de **Clean Code**.

---

## 🏛️ PARTE 1 – Modelagem e Estrutura

### 1️⃣ Estrutura de Pastas

```text
testando_api/
├── app/
│   ├── controllers/            # Camada de Apresentação (Rotas HTTP / Controllers)
│   │   ├── __init__.py
│   │   ├── user_controller.py
│   │   ├── course_controller.py
│   │   └── enrollment_controller.py
│   ├── services/               # Camada de Casos de Uso / Regras de Negócio (Use Cases)
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   ├── course_service.py
│   │   └── enrollment_service.py
│   ├── repositories/           # Camada de Acesso a Dados (Abstração com ORM)
│   │   ├── __init__.py
│   │   ├── user_repository.py
│   │   ├── course_repository.py
│   │   └── enrollment_repository.py
│   ├── models/                 # Camada de Entidades de Banco de Dados (SQLAlchemy ORM)
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── course.py
│   │   └── enrollment.py
│   ├── schemas/                # DTOs e Validações de Entrada/Saída (Pydantic)
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── course.py
│   │   └── enrollment.py
│   ├── infrastructure/         # Configurações de Infraestrutura e Banco
│   │   ├── __init__.py
│   │   └── database.py
│   └── core/                   # Utilitários Globais, Configurações e Respostas
│       ├── __init__.py
│       ├── config.py
│       ├── exceptions.py
│       └── responses.py
├── tests/                      # Testes Automatizados (Pytest)
│   ├── __init__.py
│   ├── conftest.py
│   └── test_api.py
├── .env                        # Variáveis de ambiente locais
├── .env.example                # Exemplo de configuração
├── .gitignore
├── requirements.txt            # Dependências do projeto
├── main.py                     # Ponto de entrada da aplicação
└── README.md                   # Documentação do projeto
```

### 2️⃣ Justificativa da Organização (Arquitetura Limpa)

> A estrutura do projeto foi organizada com base nos princípios da Arquitetura Limpa para garantir o desacoplamento e a separação estrita de responsabilidades entre as camadas do sistema. Os **Controllers** lidam apenas com o protocolo HTTP e serialização, delegando toda a lógica para os **Services** (Casos de Uso), que orquestram as regras de negócio sem conhecer detalhes de banco de dados. Os **Repositories** encapsulam o acesso aos dados via SQLAlchemy ORM, isolando a persistência do restante da aplicação, enquanto as **Entities/Models** e **Schemas (DTOs)** definem a estrutura dos dados e garantem a integridade das entradas e saídas. Essa divisão facilita a manutenibilidade, a evolução do sistema e a testabilidade automatizada sem acoplamento a frameworks externos.

---

## 🚀 PARTE 2 – Funcionalidades e Endpoints da API

### 👤 1. CRUD de Usuários (`/users`)
- `POST /users`: Cadastra um usuário.
  - **Regra**: Valida formato do e-mail e garante unicidade (retorna `409 Conflict` se o e-mail já estiver cadastrado).
- `GET /users`: Lista todos os usuários cadastrados.
- `GET /users/{id}`: Busca um usuário específico pelo seu ID (retorna `404 Not Found` caso não exista).
- `PUT /users/{id}`: Atualiza os dados de um usuário (valida unicidade caso o e-mail seja alterado).
- `DELETE /users/{id}`: Exclui o usuário do sistema.

### 📘 2. CRUD de Cursos (`/courses`)
- `POST /courses`: Cadastra um novo curso com título, descrição e carga horária (em horas).
  - **Regra**: Carga horária (`workload`) deve ser maior que zero.
- `GET /courses`: Lista todos os cursos cadastrados.
- `GET /courses/{id}`: Busca um curso por ID (retorna `404 Not Found` caso não exista).
- `PUT /courses/{id}`: Atualiza os dados de um curso.
- `DELETE /courses/{id}`: Exclui o curso.

### 📝 3. Matrículas (`/enrollments`)
- `POST /enrollments`: Matricula um usuário em um curso.
  - **Payload**: `{ "user_id": 1, "course_id": 2 }`
  - **Regras Implementadas**:
    1. Valida se o usuário existe (retorna `404 Not Found` se inexistente).
    2. Valida se o curso existe (retorna `404 Not Found` se inexistente).
    3. Impede matrícula duplicada para o mesmo usuário no mesmo curso (retorna `409 Conflict` com mensagem descritiva).

### 🔗 4. Consulta Relacional (`/users/{id}/courses`)
- `GET /users/{id}/courses`: Retorna os dados do usuário e a lista completa dos cursos nos quais ele está matriculado.
  - Utiliza os relacionamentos bidirecionais do SQLAlchemy ORM (`joinedload`) para carregar os dados de forma performática.

---

## 🧼 PARTE 3 – Clean Code e Boas Práticas

Neste projeto foram aplicados preceitos fundamentais da obra *Clean Code* de Robert C. Martin:

1. **Nomes Claros e Significativos**:
   - Classes, métodos e variáveis possuem nomes descritivos em inglês e autoexplicativos (ex: `EnrollmentService`, `get_user_courses`, `create_user`, `is_already_enrolled`).
2. **Métodos Curtos e Responsabilidade Única (SRP)**:
   - Funções focadas em executar apenas uma tarefa bem definida, facilitando a leitura e testes.
3. **Ausência de Lógica de Negócio nos Controllers**:
   - Os controllers apenas recebem os dados da requisição HTTP, acionam o serviço apropriado e formatam a resposta. Nenhuma regra de validação de negócio ou chamada direta de banco reside no controller.
4. **Tratamento Adequado de Exceções**:
   - Exceções de domínio semânticas (`EntityNotFoundException`, `ConflictException`, `BusinessRuleException`).
   - Handlers globais no FastAPI capturam essas exceções e geram códigos HTTP semânticos (400, 404, 409, 422, 500).
5. **Padronização Consistente de Respostas**:
   - Todas as respostas da API seguem o padrão JSON exigido:

```json
{
  "success": true,
  "message": "User created successfully",
  "data": {
    "id": 1,
    "name": "Carlos Silva",
    "email": "carlos@example.com",
    "created_at": "2026-09-08T20:30:00Z"
  }
}
```

Em caso de erro:
```json
{
  "success": false,
  "message": "User not found",
  "data": null
}
```

---

## 🛠️ Como Executar o Projeto Localmente

### 1. Pré-requisitos
- Python 3.10+ instalado.
- PostgreSQL instalado e em execução em sua máquina.

### 2. Configurar o Banco de Dados no PostgreSQL
1. Abra o **pgAdmin** ou o terminal **psql**.
2. Crie um banco de dados para a aplicação:
   ```sql
   CREATE DATABASE studymanager_db;
   ```
3. Abra o arquivo `.env` na raiz do projeto e ajuste o usuário e senha com as credenciais do seu PostgreSQL local:
   ```env
   DATABASE_URL=postgresql+psycopg://postgres:SUA_SENHA_AQUI@localhost:5432/studymanager_db
   ```
   *(Substitua `SUA_SENHA_AQUI` pela senha que você definiu ao instalar o PostgreSQL, como `postgres`, `admin` ou `123456`).*

> **Nota**: As tabelas (`users`, `courses`, `enrollments`) e suas chaves estrangeiras são criadas **automaticamente** pelo SQLAlchemy assim que a aplicação inicia!

### 3. Ativar o Ambiente Virtual e Instalar Dependências
Se estiver utilizando o ambiente virtual já configurado:
```powershell
# No Windows PowerShell:
.\venv\Scripts\Activate.ps1
```

Caso queira reinstalar as dependências:
```powershell
pip install -r requirements.txt
```

### 4. Iniciar a API
Execute o servidor de desenvolvimento com o comando:
```powershell
uvicorn main:app --reload
```
A API estará rodando em: `http://localhost:8000`

---

## 📖 Documentação Interativa (Swagger / OpenAPI)

Com o servidor rodando, acesse no seu navegador:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Redoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

Pelo Swagger você pode testar diretamente no navegador todos os endpoints de Usuários, Cursos, Matrículas e Consultas Relacionais!

---

## 🧪 Executando os Testes Automatizados

Para rodar todos os testes automatizados da aplicação e validar as regras de negócio e respostas HTTP:
```powershell
pytest -v
```
Todos os 16 testes automatizados executam em memória e cobrem:
- CRUD de Usuários e Cursos
- Validação de e-mail único e formato inválido
- Validação de carga horária positiva
- Criação de matrículas
- Bloqueio de matrícula duplicada
- Bloqueio de matrícula com IDs inexistentes
- Consulta relacional de cursos do usuário
- Padronização do JSON de resposta (`success`, `message`, `data`)
