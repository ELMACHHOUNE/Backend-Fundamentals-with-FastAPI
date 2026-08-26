# Backend Fundamentals with FastAPI

A simple FastAPI backend exposing four beginner-friendly endpoints.

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI application entry point
│   ├── models.py         # Pydantic models for request/response validation
│   └── routers/
│       ├── __init__.py
│       ├── health.py     # GET /health
│       ├── chat.py       # POST /chat
│       ├── quiz.py       # POST /quiz
│       └── summarise.py  # POST /summarise
├── tests/
│   └── test_api.py       # Automated tests with pytest and httpx
├── docs/
│   └── api-test-report.md
├── requirements.txt
└── README.md
```

## Endpoints

### GET /health
Returns service health status, version, and timestamp.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2026-08-26T15:30:00.000000"
}
```

### POST /chat
Receives a message and returns a structured answer.

**Request:**
```json
{
  "message": "Hello, world!"
}
```

**Response:**
```json
{
  "answer": "Echo: Hello, world!"
}
```

**Validation:** Message must be 1-2000 characters.

### POST /quiz
Generates quiz questions for a given topic.

**Request:**
```json
{
  "topic": "python",
  "num_questions": 3
}
```

**Response:**
```json
{
  "questions": [
    {
      "question": "What is the correct way to create a list in Python?",
      "options": ["list = []", "list = {}", "list = ()", "list = <>"],
      "correct_answer": 0,
      "explanation": "Square brackets [] are used to create lists in Python"
    }
  ]
}
```

**Validation:** Topic 1-100 chars, num_questions 1-20.

### POST /summarise
Summarises text into bullet points.

**Request:**
```json
{
  "text": "This is a long text that needs to be summarised. It has multiple sentences. Each sentence will become a bullet point.",
  "max_bullets": 3
}
```

**Response:**
```json
{
  "summary": [
    "This is a long text that needs to be summarised.",
    "It has multiple sentences.",
    "Each sentence will become a bullet point."
  ],
  "original_length": 105,
  "summary_length": 95
}
```

**Validation:** Text 10-10000 chars, max_bullets 1-10.

## Running the Application

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
uvicorn app.main:app --reload
```

3. Access Swagger UI at: http://localhost:8000/docs

## Running Tests

```bash
pytest tests/ -v
```

## Manual Testing in Swagger UI

1. Open http://localhost:8000/docs
2. Test each endpoint with valid and invalid inputs

### Example Valid Requests

**Health:** GET `/health`

**Chat:** POST `/chat` with `{"message": "Hello"}`

**Quiz:** POST `/quiz` with `{"topic": "python", "num_questions": 2}`

**Summarise:** POST `/summarise` with `{"text": "This is a test. Another sentence.", "max_bullets": 2}`

### Example Invalid Requests

**Chat:** POST `/chat` with `{"message": ""}` (empty message)

**Quiz:** POST `/quiz` with `{"topic": "", "num_questions": 5}` (empty topic)

**Summarise:** POST `/summarise` with `{"text": "short", "max_bullets": 3}` (text too short)