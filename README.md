# CodeGuard AI

> AI-powered code review, testing, and fixing.

[![Live Demo](https://img.shields.io/badge/Live%20Demo-CodeGuard%20AI-blue)](https://codeguard-ai-ten.vercel.app/)
[![Backend](https://img.shields.io/badge/Backend-Render-46E3B7)](https://codeguard-ai-yzwk.onrender.com/)
[![Frontend](https://img.shields.io/badge/Frontend-Vercel-black)](https://codeguard-ai-ten.vercel.app/)
[![Python](https://img.shields.io/badge/Python-3.12-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-19-61DAFB)](https://react.dev/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED)](https://www.docker.com/)

CodeGuard AI is an AI-powered developer productivity platform that analyzes Python code, identifies potential issues, explains them, generates tests, proposes fixes, validates those fixes, and measures code-quality improvement.

Instead of stopping at **"here is a problem in your code,"** CodeGuard AI follows a complete workflow:

**Analyze → Explain → Test → Fix → Validate → Measure**

---

## 🚀 Live Demo

### Application

https://codeguard-ai-ten.vercel.app/

### Backend Health Check

https://codeguard-ai-yzwk.onrender.com/health

Try the following example in the live application:

```python
def divide(a, b):
    return a / b
```

CodeGuard AI can identify the division-by-zero risk, explain the issue, generate tests, propose a fix, validate the corrected implementation, and show the resulting quality improvement.

---

## 🎯 Problem

Developers often rely on multiple tools to improve code quality:

- Static analysis tools for detecting issues
- Documentation or search for understanding problems
- Testing frameworks for validating behavior
- Manual debugging for fixing failures
- Code review for evaluating improvements

This creates a fragmented workflow.

A developer may know that something is wrong without having a clear explanation of:

- Why the issue matters
- What behavior should be tested
- How the code should be fixed
- Whether the proposed fix actually works

---

## 💡 Solution

CodeGuard AI combines these steps into a single workflow.

A developer provides Python source code and CodeGuard AI:

1. Analyzes the code using AST-based analysis and Ruff
2. Identifies potential bugs and code-quality issues
3. Uses AI to explain detected issues
4. Generates pytest tests for the expected behavior
5. Executes the tests against the original code
6. Generates an AI-powered correction
7. Re-runs the tests against the corrected code
8. Re-analyzes the fixed code
9. Calculates a before-and-after quality score

This creates a closed-loop developer productivity workflow:

```text
Source Code
     ↓
Code Analysis
     ↓
Issue Detection
     ↓
AI Explanation
     ↓
Test Generation
     ↓
Original Test Run
     ↓
AI Fix
     ↓
Validation
     ↓
Quality Score
```

---

## ✨ Key Features

### 🔍 Intelligent Code Analysis

CodeGuard AI combines:

- Python AST analysis
- Ruff static analysis
- Rule-based detection
- AI-powered reasoning

The current MVP detects issues including:

- Division-by-zero risks
- Unsafe dictionary key access
- Mutable default arguments
- Ruff-detected issues
- Subprocess configuration issues

---

### 🤖 AI-Powered Explanations

For every detected issue, CodeGuard AI explains:

- What the problem is
- Why it matters
- Potential impact
- How it should be addressed

The goal is to help developers understand the issue rather than simply presenting an error message.

---

### 🧪 Automatic Test Generation

CodeGuard AI generates pytest tests based on the detected issue and expected corrected behavior.

Generated tests are executed automatically against the original implementation.

This allows the system to demonstrate that the problematic behavior is actually captured by the tests.

---

### 🔧 AI-Powered Fixes

After identifying an issue, CodeGuard AI generates a corrected version of the source code.

The fix is generated using the detected issue and expected behavior as context.

---

### ✅ Fix Validation

AI-generated fixes are not blindly accepted.

CodeGuard AI executes the generated tests against the corrected code.

```text
Original Code
     ↓
Generated Tests
     ↓
❌ Failure
     ↓
AI Fix
     ↓
Generated Tests
     ↓
✅ Passed
```

This creates a validation loop around AI-generated code changes.

---

### 📊 Code Quality Score

CodeGuard AI calculates a quality score based on:

- Detected issue severity
- Test results
- Fix validation

The application displays:

```text
Before Score
     ↓
After Score
     ↓
Improvement
```

This gives developers a simple way to visualize the impact of the correction.

---

## 🏗️ Architecture

```text
                         ┌──────────────────────┐
                         │      Developer       │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   React + TypeScript │
                         │       Frontend       │
                         └──────────┬───────────┘
                                    │
                                    │ HTTPS
                                    ▼
                         ┌──────────────────────┐
                         │       FastAPI        │
                         │       Backend        │
                         └──────────┬───────────┘
                                    │
                   ┌────────────────┼────────────────┐
                   │                │                │
                   ▼                ▼                ▼
              ┌─────────┐      ┌─────────┐      ┌─────────┐
              │   AST   │      │  Ruff   │      │  Groq   │
              │Analysis │      │Analysis │      │   AI    │
              └────┬────┘      └────┬────┘      └────┬────┘
                   │                │                │
                   └────────────────┼────────────────┘
                                    ▼
                         ┌──────────────────────┐
                         │   Analysis Engine    │
                         └──────────┬───────────┘
                                    │
                         ┌──────────┴──────────┐
                         │                     │
                         ▼                     ▼
                ┌────────────────┐    ┌────────────────┐
                │ Issue Analysis │    │ Test Generator │
                └────────────────┘    └───────┬────────┘
                                              │
                                              ▼
                                        ┌───────────┐
                                        │   pytest  │
                                        └─────┬─────┘
                                              │
                                              ▼
                                      ┌──────────────┐
                                      │ Fix Generator│
                                      └──────┬───────┘
                                             │
                                             ▼
                                      ┌──────────────┐
                                      │ Fix Validator│
                                      └──────┬───────┘
                                             │
                                             ▼
                                      ┌──────────────┐
                                      │Quality Score │
                                      └──────────────┘

                         ┌──────────────────────┐
                         │      Supabase        │
                         │     PostgreSQL       │
                         └──────────────────────┘
```

---

## 🛠️ Tech Stack

### Frontend

- React
- TypeScript
- Vite
- Tailwind CSS
- Monaco Editor

### Backend

- Python
- FastAPI
- Pydantic
- Uvicorn

### AI

- Groq
- `openai/gpt-oss-120b`

### Code Analysis

- Python AST
- Ruff

### Testing

- pytest

### Database

- Supabase
- PostgreSQL

### Infrastructure

- Docker
- Docker Compose
- Nginx
- Vercel
- Render

---

## 📁 Project Structure

```text
codeguard-ai/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/
│   │   │       └── analysis.py
│   │   │
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   └── supabase.py
│   │   │
│   │   ├── models/
│   │   │   └── __init__.py
│   │   │
│   │   ├── schemas/
│   │   │   └── analysis.py
│   │   │
│   │   ├── services/
│   │   │   ├── analyzer.py
│   │   │   ├── ai_service.py
│   │   │   ├── test_generator.py
│   │   │   ├── test_runner.py
│   │   │   ├── ai_fix_service.py
│   │   │   ├── fix_validator.py
│   │   │   ├── quality_scorer.py
│   │   │   └── database.py
│   │   │
│   │   └── main.py
│   │
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   └── App.tsx
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── package.json
│   └── ...
│
├── .dockerignore
├── .gitignore
├── docker-compose.yml
├── .env.example
├── LICENSE
└── README.md
```

---

## ⚙️ Running Locally

### Prerequisites

Make sure you have:

- Python 3.12+
- Node.js
- npm
- Docker Desktop
- A Groq API key
- A Supabase project

---

## 🔐 Environment Variables

### Backend

Create:

```text
backend/.env
```

Add:

```env
GROQ_API_KEY=your_groq_api_key
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

Never commit `.env` files or API keys to GitHub.

---

### Frontend

For local development, create:

```text
frontend/.env
```

Add:

```env
VITE_API_URL=http://localhost:8000
```

For production, configure:

```env
VITE_API_URL=https://codeguard-ai-yzwk.onrender.com
```

through the deployment platform.

---

## 🐳 Running with Docker

CodeGuard AI is fully containerized.

From the project root:

```bash
docker compose build
```

Then:

```bash
docker compose up
```

The application will be available at:

```text
Frontend:
http://localhost:5173

Backend:
http://localhost:8000

Backend Health:
http://localhost:8000/health
```

To stop the containers:

```bash
docker compose down
```

---

## 💻 Running Without Docker

### Backend

Navigate to the backend:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv .venv
```

Windows:

```powershell
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start FastAPI:

```bash
uvicorn app.main:app --reload
```

The backend will run at:

```text
http://localhost:8000
```

---

### Frontend

Open another terminal:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The frontend will run at:

```text
http://localhost:5173
```

---

## 🔄 Example Workflow

Given:

```python
def divide(a, b):
    return a / b
```

CodeGuard AI can identify the potential division-by-zero problem.

The workflow becomes:

```text
1. Analyze Code
        ↓
2. Detect DIVISION issue
        ↓
3. Explain the problem with AI
        ↓
4. Generate pytest tests
        ↓
5. Run tests against original code
        ↓
6. Original implementation fails
        ↓
7. Generate corrected implementation
        ↓
8. Run tests against corrected code
        ↓
9. Tests pass
        ↓
10. Re-analyze corrected code
        ↓
11. Calculate final quality score
```

A corrected implementation may look like:

```python
def divide(a, b):
    if b == 0:
        raise ValueError("Denominator cannot be zero.")
    return a / b
```

---

## 🗄️ Data Persistence

CodeGuard AI uses Supabase PostgreSQL to persist analysis data.

The application stores:

- Projects
- Analyses
- Detected issues
- Test runs
- Generated fixes

This provides structured persistence for the CodeGuard analysis workflow.

---

## 🔌 API

### Analyze Code

```http
POST /analysis
```

Request:

```json
{
  "code": "def divide(a, b):\n    return a / b"
}
```

The response contains:

- Detected issues
- AI explanations
- Before quality score
- Generated tests
- Original test results
- AI-generated fix
- Fixed test results
- Fix validation status
- After quality score

---

### Health Check

```http
GET /health
```

Response:

```json
{
  "status": "healthy"
}
```

---

## ☁️ Deployment

CodeGuard AI uses a split deployment architecture.

### Frontend

**Vercel**

https://codeguard-ai-ten.vercel.app/

### Backend

**Render**

https://codeguard-ai-yzwk.onrender.com

### Database

**Supabase PostgreSQL**

### AI

**Groq**

The frontend communicates with the deployed FastAPI backend through the `VITE_API_URL` environment variable.

---

## 🏆 Hackathon Track

### Developer Productivity

CodeGuard AI is designed to improve developer productivity by reducing the time required to:

- Find code issues
- Understand why they occur
- Create tests
- Implement fixes
- Validate fixes
- Measure improvement

Instead of providing only an AI-generated suggestion, CodeGuard AI creates a validation loop around the suggestion.

---

## 🔮 Future Improvements

Potential future improvements include:

- GitHub repository integration
- Pull request analysis
- Multi-language support
- More security vulnerability detection
- Deeper performance analysis
- Automatic patch generation
- Improved test coverage analysis
- Historical code-quality tracking
- Team and project dashboards
- CI/CD integration
- Authentication
- Multi-user workspaces

---

## 🔒 Security Notes

CodeGuard AI processes source code for analysis and testing.

For production deployments:

- Never commit API keys or secrets
- Keep credentials in environment variables
- Never expose backend credentials to the frontend
- Restrict CORS origins appropriately
- Execute untrusted code in isolated environments
- Apply resource and execution limits to test execution
- Validate AI-generated code before accepting it

The current MVP executes generated tests inside temporary isolated directories and applies a test execution timeout.

For a production-grade code execution service, stronger sandboxing and resource isolation would be required.

---

## 📄 License

This project is licensed under the MIT License.

See the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Praveena Pawar**

GitHub:

https://github.com/praveena-pawar

---

## ⭐ Support

If you find CodeGuard AI useful or interesting, consider giving the repository a ⭐ on GitHub.

---

## 💬 Final Thought

> **CodeGuard AI — Don't just find the bug. Understand it. Test it. Fix it. Prove it.**
