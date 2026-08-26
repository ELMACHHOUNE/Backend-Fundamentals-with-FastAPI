from fastapi import APIRouter, HTTPException
from app.models import QuizRequest, QuizResponse, QuizQuestion

router = APIRouter(prefix="/quiz", tags=["quiz"])


QUIZ_TEMPLATES = {
    "python": [
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
        },
        {
            "question": "What does 'len()' function return?",
            "options": ["Length of object", "Last element", "First element", "Type of object"],
            "correct_answer": 0,
            "explanation": "len() returns the number of items in an object"
        }
    ],
    "javascript": [
        {
            "question": "How do you declare a variable in JavaScript?",
            "options": ["var x = 5", "variable x = 5", "v x = 5", "declare x = 5"],
            "correct_answer": 0,
            "explanation": "var, let, or const are used to declare variables in JavaScript"
        },
        {
            "question": "Which operator is used for strict equality in JavaScript?",
            "options": ["==", "===", "=", "!="],
            "correct_answer": 1,
            "explanation": "=== checks both value and type equality"
        }
    ],
    "general": [
        {
            "question": "What does API stand for?",
            "options": ["Application Programming Interface", "Advanced Programming Interface", "Automated Programming Interface", "Application Process Interface"],
            "correct_answer": 0,
            "explanation": "API stands for Application Programming Interface"
        },
        {
            "question": "What is JSON?",
            "options": ["JavaScript Object Notation", "Java Standard Output Network", "Joint Script Object Notation", "JavaScript Ordered Notation"],
            "correct_answer": 0,
            "explanation": "JSON stands for JavaScript Object Notation"
        }
    ]
}


@router.post("", response_model=QuizResponse)
async def generate_quiz(request: QuizRequest) -> QuizResponse:
    topic_lower = request.topic.lower().strip()
    
    template = QUIZ_TEMPLATES.get(topic_lower, QUIZ_TEMPLATES["general"])
    
    num_questions = min(request.num_questions, len(template))
    selected = template[:num_questions]
    
    questions = [
        QuizQuestion(**q) for q in selected
    ]
    
    if not questions:
        raise HTTPException(status_code=400, detail="No questions available for this topic")
    
    return QuizResponse(questions=questions)