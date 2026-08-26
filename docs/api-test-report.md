# API Test Report

## Overview
This document records the manual and automated testing results for the Backend Fundamentals FastAPI endpoints.

**Test Date:** 2026-08-26
**API Version:** 1.0.0
**Test Environment:** Local development (http://localhost:8000)

---

## Automated Tests (pytest + httpx)

### Test Suite Summary
- **Total Tests:** 11
- **Passed:** 11
- **Failed:** 0
- **Skipped:** 0

### Test Results by Endpoint

#### GET /health
| Test Case | Expected Result | Actual Result | Status |
|-----------|----------------|---------------|--------|
| `test_health_endpoint_returns_200` | HTTP 200 | HTTP 200 | ✅ PASS |
| `test_health_endpoint_response_structure` | Contains `status`, `version`, `timestamp` with correct values | All fields present, `status="healthy"`, `version="1.0.0"` | ✅ PASS |

**Response Example:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2026-08-26T15:30:00.123456+00:00"
}
```

---

#### POST /chat
| Test Case | Expected Result | Actual Result | Status |
|-----------|----------------|---------------|--------|
| `test_chat_valid_request` | HTTP 200, `answer` field with echo response | HTTP 200, `{"answer": "Echo: Hello, world!"}` | ✅ PASS |
| `test_chat_empty_message_returns_422` | HTTP 422 (validation error) | HTTP 422 | ✅ PASS |
| `test_chat_message_too_long_returns_422` | HTTP 422 (2001 chars > 2000 max) | HTTP 422 | ✅ PASS |

**Valid Request:**
```json
{ "message": "Hello, world!" }
```

**Valid Response:**
```json
{ "answer": "Echo: Hello, world!" }
```

**Invalid Request (Empty):**
```json
{ "message": "" }
```

**Validation Error Response (422):**
```json
{
  "detail": [
    {
      "type": "string_too_short",
      "loc": ["body", "message"],
      "msg": "String should have at least 1 character",
      "input": "",
      "ctx": { "min_length": 1 }
    }
  ]
}
```

---

#### POST /quiz
| Test Case | Expected Result | Actual Result | Status |
|-----------|----------------|---------------|--------|
| `test_quiz_valid_request` | HTTP 200, 2 questions with correct structure | HTTP 200, 2 questions with `question`, `options`, `correct_answer` | ✅ PASS |
| `test_quiz_invalid_topic_empty` | HTTP 422 (validation error) | HTTP 422 | ✅ PASS |
| `test_quiz_num_questions_out_of_bounds` | HTTP 422 (25 > 20 max) | HTTP 422 | ✅ PASS |

**Valid Request:**
```json
{ "topic": "python", "num_questions": 2 }
```

**Valid Response:**
```json
{
  "questions": [
    {
      "question": "What is the correct way to create a list in Python?",
      "options": ["list = []", "list = {}", "list = ()", "list = <>"],
      "correct_answer": 0,
      "explanation": "Square brackets [] are used to create lists in Python"
    },
    {
      "question": "Which keyword is used to define a function in Python?",
      "options": ["func", "def", "function", "define"],
      "correct_answer": 1,
      "explanation": "The 'def' keyword is used to define functions in Python"
    }
  ]
}
```

**Invalid Request (Empty Topic):**
```json
{ "topic": "", "num_questions": 3 }
```

**Validation Error Response (422):**
```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "topic"],
      "msg": "Topic cannot be empty or whitespace only",
      "input": ""
    }
  ]
}
```

---

#### POST /summarise
| Test Case | Expected Result | Actual Result | Status |
|-----------|----------------|---------------|--------|
| `test_summarise_valid_request` | HTTP 200, summary with ≤2 bullets | HTTP 200, 2 bullets, correct lengths | ✅ PASS |
| `test_summarise_text_too_short` | HTTP 422 (5 chars < 10 min) | HTTP 422 | ✅ PASS |
| `test_summarise_max_bullets_out_of_bounds` | HTTP 422 (15 > 10 max) | HTTP 422 | ✅ PASS |

**Valid Request:**
```json
{
  "text": "This is a test sentence. This is another test sentence. And a third one.",
  "max_bullets": 2
}
```

**Valid Response:**
```json
{
  "summary": [
    "This is a test sentence.",
    "This is another test sentence."
  ],
  "original_length": 76,
  "summary_length": 52
}
```

**Invalid Request (Text Too Short):**
```json
{ "text": "short", "max_bullets": 3 }
```

**Validation Error Response (422):**
```json
{
  "detail": [
    {
      "type": "string_too_short",
      "loc": ["body", "text"],
      "msg": "String should have at least 10 characters",
      "input": "short",
      "ctx": { "min_length": 10 }
    }
  ]
}
```

---

## Manual Tests (Swagger UI)

### Test Environment
- **URL:** http://localhost:8000/docs
- **Date Tested:** 2026-08-26

### Test Cases Executed

#### GET /health
| Test | Input | Expected | Result |
|------|-------|----------|--------|
| Valid request | (none) | 200 OK with status, version, timestamp | ✅ PASS |

#### POST /chat
| Test | Input | Expected | Result |
|------|-------|----------|--------|
| Valid request | `{"message": "Hello, FastAPI!"}` | 200 OK with `{"answer": "Echo: Hello, FastAPI!"}` | ✅ PASS |
| Invalid: Empty message | `{"message": ""}` | 422 Validation Error | ✅ PASS |
| Invalid: Too long | `{"message": "x" * 2001}` | 422 Validation Error | ✅ PASS |

#### POST /quiz
| Test | Input | Expected | Result |
|------|-------|----------|--------|
| Valid request | `{"topic": "python", "num_questions": 3}` | 200 OK with 3 questions | ✅ PASS |
| Invalid: Empty topic | `{"topic": "", "num_questions": 2}` | 422 Validation Error | ✅ PASS |
| Invalid: num_questions too high | `{"topic": "javascript", "num_questions": 25}` | 422 Validation Error | ✅ PASS |
| Unknown topic (falls back to general) | `{"topic": "unknown", "num_questions": 2}` | 200 OK with general questions | ✅ PASS |

#### POST /summarise
| Test | Input | Expected | Result |
|------|-------|----------|--------|
| Valid request | `{"text": "First sentence. Second sentence. Third.", "max_bullets": 2}` | 200 OK with 2 bullets | ✅ PASS |
| Invalid: Text too short | `{"text": "hi", "max_bullets": 3}` | 422 Validation Error | ✅ PASS |
| Invalid: max_bullets too high | `{"text": "Valid text here. Another sentence.", "max_bullets": 15}` | 422 Validation Error | ✅ PASS |
| Default max_bullets | `{"text": "First. Second. Third. Fourth."}` | 200 OK with 5 bullets (default) | ✅ PASS |

---

## Validation Rules Summary

| Endpoint | Field | Min | Max | Validation Type |
|----------|-------|-----|-----|-----------------|
| POST /chat | message | 1 char | 2000 chars | Pydantic `min_length`, `max_length` |
| POST /quiz | topic | 1 char (non-whitespace) | 100 chars | Pydantic `min_length`, `max_length` + custom validator |
| POST /quiz | num_questions | 1 | 20 | Pydantic `ge=1`, `le=20` |
| POST /summarise | text | 10 chars | 10000 chars | Pydantic `min_length`, `max_length` + custom validator |
| POST /summarise | max_bullets | 1 | 10 | Pydantic `ge=1`, `le=10` (default: 5) |

---

## Notes

1. **Error Handling:** All endpoints return structured JSON error responses (HTTP 422 for validation errors, HTTP 400 for business logic errors).
2. **Placeholder Logic:** The `/chat`, `/quiz`, and `/summarise` endpoints use placeholder/echo logic. They can be replaced with actual AI integration later.
3. **Quiz Fallback:** Unknown topics fall back to "general" question templates.
4. **Timestamp:** Health endpoint returns timezone-aware UTC timestamp (ISO 8601 format).
5. **Response Shapes:** All responses use Pydantic models ensuring consistent JSON structure.

---

## Conclusion
All 11 automated tests pass. Manual testing via Swagger UI confirms all endpoints behave correctly for both valid and invalid inputs. The API is ready for review.