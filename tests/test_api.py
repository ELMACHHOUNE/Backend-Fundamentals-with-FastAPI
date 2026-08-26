import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


class TestHealthEndpoint:
    @pytest.mark.anyio
    async def test_health_endpoint_returns_200(self, client):
        response = await client.get("/health")
        assert response.status_code == 200

    @pytest.mark.anyio
    async def test_health_endpoint_response_structure(self, client):
        response = await client.get("/health")
        data = response.json()
        
        assert "status" in data
        assert "version" in data
        assert "timestamp" in data
        
        assert data["status"] == "healthy"
        assert data["version"] == "1.0.0"


class TestChatEndpoint:
    @pytest.mark.anyio
    async def test_chat_valid_request(self, client):
        response = await client.post("/chat", json={"message": "Hello, world!"})
        assert response.status_code == 200
        
        data = response.json()
        assert "answer" in data
        assert data["answer"] == "Echo: Hello, world!"

    @pytest.mark.anyio
    async def test_chat_empty_message_returns_422(self, client):
        response = await client.post("/chat", json={"message": ""})
        assert response.status_code == 422

    @pytest.mark.anyio
    async def test_chat_message_too_long_returns_422(self, client):
        long_message = "x" * 2001
        response = await client.post("/chat", json={"message": long_message})
        assert response.status_code == 422


class TestQuizEndpoint:
    @pytest.mark.anyio
    async def test_quiz_valid_request(self, client):
        response = await client.post("/quiz", json={"topic": "python", "num_questions": 2})
        assert response.status_code == 200
        
        data = response.json()
        assert "questions" in data
        assert len(data["questions"]) == 2
        
        for q in data["questions"]:
            assert "question" in q
            assert "options" in q
            assert "correct_answer" in q
            assert isinstance(q["options"], list)
            assert len(q["options"]) >= 2

    @pytest.mark.anyio
    async def test_quiz_invalid_topic_empty(self, client):
        response = await client.post("/quiz", json={"topic": "", "num_questions": 3})
        assert response.status_code == 422

    @pytest.mark.anyio
    async def test_quiz_num_questions_out_of_bounds(self, client):
        response = await client.post("/quiz", json={"topic": "python", "num_questions": 25})
        assert response.status_code == 422


class TestSummariseEndpoint:
    @pytest.mark.anyio
    async def test_summarise_valid_request(self, client):
        text = "This is a test sentence. This is another test sentence. And a third one."
        response = await client.post("/summarise", json={"text": text, "max_bullets": 2})
        assert response.status_code == 200
        
        data = response.json()
        assert "summary" in data
        assert "original_length" in data
        assert "summary_length" in data
        assert len(data["summary"]) <= 2
        assert data["original_length"] == len(text)

    @pytest.mark.anyio
    async def test_summarise_text_too_short(self, client):
        response = await client.post("/summarise", json={"text": "short", "max_bullets": 3})
        assert response.status_code == 422

    @pytest.mark.anyio
    async def test_summarise_max_bullets_out_of_bounds(self, client):
        text = "This is a test sentence. Another sentence here."
        response = await client.post("/summarise", json={"text": text, "max_bullets": 15})
        assert response.status_code == 422